import cProfile
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
from time import sleep
import time
import traceback
from bs4 import BeautifulSoup
import numpy as np
from augraphy import AugraphyPipeline
from unoserver import client
import requests
from tqdm import tqdm
from PIL import ImageDraw
import cv2 
import threading

from src.augmentations import get_augmentation_phases
from src.docx_document import DocxDocument


def profileit(func):
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + ".profile" # Name the data file sensibly
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        return retval

    return wrapper

class DocumentGenerator:
    def __init__(self, image_size, docx_config, out_folder, port, uno_port):
        self.image_size = image_size
        self.out_folder = out_folder
        self.docx_config = docx_config
        self.port = port
        self.uno_port = uno_port

        self.doc = None
        self.image_counter = 0
        
        self.debug_mode = False

        command = f"/usr/bin/python3 -m unoserver.server --port {port} --uno-port {uno_port}"
        #self.process = subprocess.Popen('pkill -f uno', shell=True)
        print('START SERVER', port, uno_port)
        self.process = subprocess.Popen(command, shell=True)
        self.uno_client = client.UnoClient(port=port)

    def generate_(self, urls):
        print('Start Document Generator...')
        for i, url in tqdm(enumerate(urls)):
            try:
                self.create_doc(url, i)
            except Exception as e:
                print(traceback.format_exc())
    
    def generate(self, urls):
        print('Start Document Generator...')
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_doc_, url, i) for i, url in enumerate(urls)]
            for future in futures:
                future.result()
    
    def create_doc_(self, url, i):
        try:
            self.create_doc(url, i)
        except Exception as e:
            print(traceback.format_exc())

    #@profileit
    def create_doc(self, url, i):
        self.doc = DocxDocument(self.docx_config, self.uno_client)
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Bad Response: {response}")
            return
        
        # create colored docx document
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', "table"]):
            if element.name.startswith('h'):
                self.doc.add_heading(element)
            elif element.name == "table":
                self.doc.add_table(element)
            else:
                self.doc.add_text(element)
                
            if self.doc.get_num_words() > self.docx_config["max_words"]:
                break
            
        # extract annotations from colored images
        colored_images = self.doc.get_images(dpi=200, image_size=1500)
        annotations = self.get_bboxes(colored_images)  # bboxes are normalized to [0,1]
        self.doc.convert_to_uncolored_docx()
        images = self.doc.get_images(dpi=200, image_size=1024)  # get images for augmentation stage
        
        for i, image in enumerate(images):
            # unnormalize bboxes to augmentation image size
            bounding_boxes = np.array(annotations[i]["bboxes"])
            bounding_boxes[:, 0] = bounding_boxes[:, 0] * image.size[0]
            bounding_boxes[:, 1] = bounding_boxes[:, 1] * image.size[1]
            bounding_boxes[:, 2] = bounding_boxes[:, 2] * image.size[0] 
            bounding_boxes[:, 3] = bounding_boxes[:, 3] * image.size[1]

            # perform augmentation
            augmentation_pipeline = AugraphyPipeline(bounding_boxes=bounding_boxes,
                                                     log=False, **get_augmentation_phases())
            augmented_cv2, _, _, augmented_bounding_boxes = augmentation_pipeline(np.array(image)[:, :, ::-1])
            
            # resize image to final dataset size and save 
            augmented_cv2 = cv2.resize(augmented_cv2, (self.image_size, self.image_size))
            cv2.imwrite(str(self.out_folder / f"im_{self.image_counter}.png"), augmented_cv2)
            if self.debug_mode:
                colored_images[i].save(self.out_folder / f"im_{self.image_counter}_colored.png")
            
            # convert booxes to (x, y, w, h) format and normalize to [0,1]
            augmented_bounding_boxes = np.array(augmented_bounding_boxes).astype(int)
            x1, y1, x2, y2 = augmented_bounding_boxes[:, 0], augmented_bounding_boxes[:, 1], \
                             augmented_bounding_boxes[:, 2], augmented_bounding_boxes[:, 3]
            width, height = image.size
            x = x1 / width
            y = y1 / height
            w = (x2 - x1) / width
            h = (y2 - y1) / height
            annotations[i]["bboxes"] = np.column_stack((x, y, w, h)).tolist()

            # save annotation
            with open(self.out_folder/ f"im_{self.image_counter}.png.json", "w") as f:
                json.dump(annotations[i], f)
            self.image_counter += 1       
  
    def get_bboxes(self, images):
        annotations = []
        for image_pil in images:
            draw = ImageDraw.Draw(image_pil)
            width, height = image_pil.size
            image_annotations = {"words": [], "bboxes": []}
            image = np.asarray(image_pil)

            thr = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            thr = cv2.threshold(thr, 254, 255, cv2.THRESH_BINARY_INV)[1]
            cnts = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

            for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.015 * peri, True)

                if len(approx) == 4:
                    x, y, w, h = cv2.boundingRect(approx)
                    if self.debug_mode:
                        bbox = (x, y, x + w, y + h)
                        draw.rectangle(bbox, outline="red")

                    rgb_color = image_pil.getpixel((x+1, y+1))
                    color = '#%02x%02x%02x' % (rgb_color)
                    if color in self.doc.color2word:
                        word = self.doc.color2word[color]
                        image_annotations['words'].append(word)
                        image_annotations["bboxes"].append(
                            (
                                x / width, 
                                y / height, 
                                (x + w) / width, 
                                (y + h) / height)
                             )
                       # (x / width, y / height, w / width, h / height)
            annotations.append(image_annotations)
        return annotations

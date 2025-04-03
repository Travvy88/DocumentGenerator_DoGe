from PIL import Image, ImageDraw
import cv2
import numpy as np


def convert_xywh_to_x1y1x2y2(bboxes):
    if isinstance(bboxes, list):
        return [[bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]] for bbox in bboxes]
    if isinstance(bboxes, np.ndarray):
        x1 = bboxes[:, 0]
        x2 = bboxes[:, 1]
        x3 = bboxes[:, 0] + bboxes[:, 2]
        x4 = bboxes[:, 1] + bboxes[:, 3]
        return np.column_stack((x1, x2, x3, x4))


def convert_x1y1x2y2_to_xywh(bboxes):
    if isinstance(bboxes, list):
        return [[bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]] for bbox in bboxes]
    if isinstance(bboxes, np.ndarray):
        x = bboxes[:, 0]
        y = bboxes[:, 1]
        w = bboxes[:, 2] - bboxes[:, 0]
        h = bboxes[:, 3] - bboxes[:, 1]
        return np.column_stack((x, y, w, h))


def normalize_bboxes(bboxes, width, height):
    if isinstance(bboxes, list):
        return [[bbox[0] / width, bbox[1] / height, bbox[2] / width, bbox[3] / height] for bbox in bboxes]
    if isinstance(bboxes, np.ndarray):
        el1 = bboxes[:, 0] / width
        el2 = bboxes[:, 1] / height
        el3 = bboxes[:, 2] / width
        el4 = bboxes[:, 3] / height
        return np.column_stack((el1, el2, el3, el4))


def unnormalize_bboxes(bboxes, width, height):
    if isinstance(bboxes, list):
        return [[bbox[0] * width, bbox[1] * height, bbox[2] * width, bbox[3] * height] for bbox in bboxes]
    if isinstance(bboxes, np.ndarray):
        el1 = bboxes[:, 0] * width
        el2 = bboxes[:, 1] * height
        el3 = bboxes[:, 2] * width
        el4 = bboxes[:, 3] * height
        return np.column_stack((el1, el2, el3, el4))

def draw_bboxes_pil(image, bboxes, words=None):
    draw = ImageDraw.Draw(image)
    for bbox, word in zip(bboxes, words):
        x1, y1, x2, y2 = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        # Draw rectangle with red color and 2px thickness
        draw.rectangle([(x1, y1), (x2, y2)], outline="red", width=2)
        # Optionally add text labels above the boxes
        draw.text((x1, y1-15), word, fill="red")
    return image

def draw_bboxes(image, bboxes, words=None):
    # bboxes in x1, y1, x2, y2 format
    if words is None:
        words = [""] * len(bboxes)
    
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
        image = draw_bboxes_pil(image, bboxes, words)
        image = np.array(image)
    elif isinstance(image, Image.Image):
        image = draw_bboxes_pil(image, bboxes, words)
    else:
        raise ValueError(f"Unsupported image type: {type(image)}")
        
    return image

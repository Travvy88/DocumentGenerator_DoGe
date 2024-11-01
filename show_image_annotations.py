import argparse
import json
from PIL import Image, ImageDraw, ImageFont

parser = argparse.ArgumentParser()
parser.add_argument('path')

args = parser.parse_args()

image = Image.open(args.path)
height, width = image.size

with open(args.path + '.json', 'r') as f:
    annotations = json.load(f)

draw = ImageDraw.Draw(image)
font = ImageFont.truetype('arial.ttf', size=8)
for word, bbox in zip(annotations['words'], annotations['bboxes']):
    x, y, w, h = bbox  
    

    

    if w < 0:
        x = x - w
        w = w * -1
    if h < 0:
        y = y - h
        h = h * -1

    x1 = int(x * width)
    y1 = int(y * height)
    x2 = int((x + w) * width)
    y2 = int((y + h) * height)

    print([x, y, w, h])
    print([x1, y1, x2, y2])

    draw.rectangle([x1, y1, x2, y2], outline="blue", width=1)
    draw.text((x1, y1 - 10), word, fill="red", font=font, )  # Adjust position as needed

output_image_path = 'show_anno.png'
image.save(output_image_path)

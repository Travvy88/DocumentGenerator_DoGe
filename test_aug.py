import random
import numpy as np
from src.augmentations import get_augmentation_phases
import augraphy
from PIL import Image, ImageDraw


ink_phase = [augraphy.OneOf([
        augraphy.AugmentationSequence([
        augraphy.NoiseTexturize(sigma_range=(3, 10), turbulence_range=(2, 5), texture_width_range=(300, 500), texture_height_range=(300, 500), p=1),
        augraphy.BrightnessTexturize(texturize_range=(0.9, 0.99), deviation=0.03, p=1),
]),
        augraphy.AugmentationSequence([
        augraphy.BrightnessTexturize(texturize_range=(0.9, 0.99), deviation=0.03, p=1),
        augraphy.NoiseTexturize(sigma_range=(3, 10), turbulence_range=(2, 5), texture_width_range=(300, 500), texture_height_range=(300, 500), p=1),
]), 
], p=0.1)]

spatial = [
    augraphy.BookBinding(p=0.2),
    augraphy.Folding(p=0.2),
    augraphy.Geometric(p=0.2),
    augraphy.GlitchEffect(p=0.2),
    augraphy.InkShifter(p=0.2),
    augraphy.PageBorder(p=0.2),
    augraphy.SectionShift(p=0.2),
    augraphy.Squish(p=0.2),
]

spatial = [augraphy.Squish(
                    squish_direction="random",
                    squish_location="random",
                    squish_number_range=(5, 10),
                    squish_distance_range=(5, 7),
                    squish_line="random",
                    squish_line_thickness_range=(1, 1),
                    p=1
                ),]


image  = Image.open('image_16.png')

bounding_boxes = [
    [250, 1443, 612, 1500],
    [256, 1574, 1025, 1640]
]
pipeline = augraphy.AugraphyPipeline(ink_phase=ink_phase, bounding_boxes=bounding_boxes)

output = pipeline.augment(np.array(image))
print(output.keys())
augmented_image = output['output']
augmented_boxes = output['bounding_boxes']

augmented_image = Image.fromarray(augmented_image)
height, width = 1, 1
print(bounding_boxes)
print(augmented_boxes)

if len(augmented_boxes) > len(bounding_boxes):
    augmented_boxes = [bbox for i, bbox in enumerate(augmented_boxes) if i % 2 == 0]
    print('after supr', augmented_boxes)

draw = ImageDraw.Draw(augmented_image)
for bbox in augmented_boxes:
    x1, y1, x2, y2 = bbox  
    ''' if w < 0:
        x = x - w
        w = w * -1
    if h < 0:
        y = y - h
        h = h * -1

    x1 = int(x * width)
    y1 = int(y * height)
    x2 = int((x + w) * width)
    y2 = int((y + h) * height)'''

    #print([x, y, w, h])
    #print([x1, y1, x2, y2])
    
    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    draw.rectangle([x1, y1, x2, y2], outline="blue", width=1)

output_image_path = 'show_anno__.png'
augmented_image.save(output_image_path)

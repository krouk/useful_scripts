# -*- coding: utf-8 -*-
import glob
import numpy as np
from PIL import Image, ImageDraw

# Crop PNG-картинок в эллипс, который максимально можно вписать в квадрат исходного изображения
# Соответственно, если размеры картинки не одинаковые по ширине и длине, то будет не окружность, а эллипс
# На основе: https://stackoverflow.com/questions/51486297/cropping-an-image-in-a-circular-way-using-python
dirname = 'GEOlogo_110x110'

# For all png files in the directory
for fname in glob.glob('./' + dirname + '/*.png'):
    # Open the input image as numpy array, convert to RGB
    img = Image.open(fname).convert("RGB")
    npImage = np.array(img)
    h, w = img.size

    print('Файл \'{}\'. Размеры: h={}, w={}'.format(fname.split('/')[-1], h, w))

    # Create same size alpha layer with circle
    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([0, 0, h, w], 0, 360, fill=255)

    # Convert alpha Image to numpy array
    npAlpha = np.array(alpha)
    # Add alpha layer to RGB
    npImage = np.dstack((npImage, npAlpha))

    # Save with alpha
    new_fname = fname[:-4] + '_circle_crop.png'
    Image.fromarray(npImage).save(new_fname)
    print('Результат \'{}\''.format(new_fname))

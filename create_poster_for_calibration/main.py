import numpy as np
import matplotlib.pyplot as plt
import imageio

from PIL import Image
from numpy import asarray
#import os, sys
#for i in range(587):
#    os.system(f'wget https://media.githubusercontent.com/media/duckietown/duckietown-world/daffy/src/duckietown_world/data/tag36h11/tag36_11_{i:05}.png')
#exit()
# load the image

# T/F px is 0.8 cm or 8 mm
# the whole april tag including border is 8cm x 8cm or 80x80mm
# bump to 100 x 100?
def load_image(index):
    image = Image.open(f'tag36h11/tag36_11_{index:05}.png')

    # convert image to numpy array
    data = asarray(image)
    return np.sum(data, axis=2) > 0


def embed_image(index):
    binary = load_image(index)

    img = np.ones([80, 80])
    for i in range(80):
        for j in range(80):

            img[i,j] = 1*binary[i//8, j//8]

    frame = np.ones([100, 100])
    frame[10:90, 10:90] = img

    return frame


#printing on paper 42 inches wide.
#using working with dim 40in x 98in. -> 1010 mm x 2490 mm so using 100 cm x 250 cm
# 293 per grid
def create_grid(tag_index=0):
    w = 2500
    h = 1067 #this is so it is (almost) exactly 42 inches
    arr = np.ones((w, h))

    for i in range(25):
        i *= 100
        for j in range(10):
            j *= 100

            arr[i:i+100, j:j+100] = embed_image(tag_index)
            tag_index += 1

    return arr

def convert_to_png(image):

    #image = -1*image + 1
    png = np.zeros([image.shape[0], image.shape[1], 3])
    for i in range(3):
        png[:,:, i] = image*255

    png = png.astype(np.uint8)

    return Image.fromarray(png)

def save_png(img,name):
    img.save(name, dpi=(25.4, 25.4))




if __name__ == '__main__':
    a = create_grid(tag_index=0)
    a = convert_to_png(a)
    save_png(a, 'grid1.png')

    a = create_grid(tag_index=250)
    a = convert_to_png(a)
    save_png(a, 'grid2.png')
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

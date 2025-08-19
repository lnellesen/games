"""Fruit size configurator."""
import numpy as np
from skimage.transform import resize
from skimage import color
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
import pygame

LIST_PLAYERS = ["watermelone_upgrade.jpeg",
                "dragonfruit_upgrade.jpeg",
                "orange_upgrade.jpeg",
                "apple_upgrade.jpeg",
                "lemon_upgrade.jpeg",
                "kiwi_upgrade.jpeg",
                "strawberry_upgrade.jpeg",
                "cherry_upgrade.jpeg",
                "raspberry_upgrade.jpeg",
                "blueberry_upgrade.jpeg"]

def reshape_player(file: str):
    im = plt.imread(file)
    resized = resize(im, (im.shape[0]*0.8, im.shape[1]*0.8))
    gray_image = color.rgb2gray(resized)
    mask = gray_image >0.95
    resized[mask] = [0.098,0.098,0.098]
    plt.imsave('resized_image' + file[:-5] + '.jpg', (resized * 255).astype(np.uint8))
    return pygame.image.load('resized_image' + file[:-5] + '.jpg')


for file in LIST_PLAYERS:
     resized_image = reshape_player(file)
     #plt.imsave('resized_image'+file[:-5]+'.jpg', (resized_image * 255).astype(np.uint8))

     #plt.show()


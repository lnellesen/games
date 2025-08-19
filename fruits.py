"""Fruit size configurator."""
import numpy as np
from skimage.transform import resize
from skimage import color
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

def reshape_player(file: str)-> pygame.Surface:
    """

    :param file:
    :return:
    """
    im = plt.imread(file)
    resized = resize(im, (im.shape[0]*0.6, im.shape[1]*0.6))
    gray_image = color.rgb2gray(resized)
    mask = gray_image >0.95
    resized[mask] = [0.098,0.098,0.098]
    plt.imsave('resized_image' + file[:-5] + '.jpg', (resized * 255).astype(np.uint8))
    return pygame.image.load('resized_image' + file[:-5] + '.jpg')


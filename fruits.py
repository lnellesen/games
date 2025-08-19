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


def resize_player(image:np.array)->np.array:
    """
    Resize the fruit player.
    :param image: the image to resize
    :return:resized image
    """
    return resize(image, (image.shape[0]*0.6, image.shape[1]*0.6))


def recolor_player(image:np.array)->np.array:
    """
    Recolor the fruit player.
    :param image: the image to recolor
    :return:recolored fruit image
    """
    gray_image = color.rgb2gray(image)
    mask = gray_image >0.95
    image[mask] = [0.098,0.098,0.098]
    return image


def remodel_player(fruit: str)-> pygame.Surface:
    """
    Remodel the fruit player.
    :param fruit: the file name of the fruit image
    :return:resized and recolored fruit image
    """
    im = plt.imread(fruit)
    resized = resize_player(im)
    im_color = recolor_player(resized)
    plt.imsave('resized_image' + fruit[:-5] + '.jpg', (im_color * 255).astype(np.uint8))
    return pygame.image.load('resized_image' + fruit[:-5] + '.jpg')




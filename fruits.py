# module name is usually singular
"""Fruit size configurator."""
import numpy as np  # missing requirement
from skimage.transform import resize  # missing requirement
from skimage import color  # missing requirement
import matplotlib.pyplot as plt  # missing requirement
import pygame

# list of fruit images?
LIST_PLAYERS = [
    "watermelone_upgrade.jpeg",
    "dragonfruit_upgrade.jpeg",
    "orange_upgrade.jpeg",
    "apple_upgrade.jpeg",
    "lemon_upgrade.jpeg",
    "kiwi_upgrade.jpeg",
    "strawberry_upgrade.jpeg",
    "cherry_upgrade.jpeg",
    "raspberry_upgrade.jpeg",
    "blueberry_upgrade.jpeg"
]

# why is a player function in fruits module?
def resize_player(image: np.array) -> np.array:
    """
    Resize the fruit player.

    :param image: the image to resize
    :return:resized image
    """
    return resize(image, (image.shape[0]*0.6, image.shape[1]*0.6))  # constant, for all three values, what does 0 or 1 mean?, 0.6  seems to be the scaling factor?

# why is a player function in fruits module?
def recolor_player(image: np.array) -> np.array:
    """
    Recolor the fruit player.

    :param image: the image to recolor
    :return:recolored fruit image
    """
    gray_image = color.rgb2gray(image)
    mask = gray_image > 0.95  # constant
    image[mask] = [0.098,0.098,0.098]  # constant
    return image

# was replaced by other code, I guess
# def reshape_player(file: str):
#     im = plt.imread(file)
#     resized = resize(im, (im.shape[0]*0.8, im.shape[1]*0.8))
#     gray_image = color.rgb2gray(resized)
#     mask = gray_image >0.95
#     resized[mask] = [0.098,0.098,0.098]
#     plt.imsave('resized_image' + file[:-5] + '.jpg', (resized * 255).astype(np.uint8))
#     return pygame.image.load('resized_image' + file[:-5] + '.jpg')

# why is a player function in fruits module?
def remodel_player(fruit: str) -> pygame.Surface:
    """
    Remodel the fruit player.

    :param fruit: the file name of the fruit image
    :return:resized and recolored fruit image
    """
    image = plt.imread(fruit)  # use full length variable im could also be "imaginary" or something else
    resized = resize_player(image)
    color = recolor_player(resized)
    # use fstring, and decide if you want to use single or double quotes as string marker
    # why -5? -> constant
    file_name = f'resized_image{fruit[:-5]}.jpg'
    plt.imsave(file_name, (color*255).astype(np.uint8))  # multiplication was without whitespaces further up, decide on style
    return pygame.image.load(file_name)




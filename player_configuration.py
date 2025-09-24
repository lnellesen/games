"""Player loading and size configurator that are needed before the init of the class PLayer."""
import numpy as np
from skimage.transform import resize
from skimage import color
import matplotlib.pyplot as plt

LIST_PLAYER_FILES = ["blueberry_upgrade.jpeg",
                    "raspberry_upgrade.jpeg",
                    "cherry_upgrade.jpeg",
                    "strawberry_upgrade.jpeg",
                    "kiwi_upgrade.jpeg",
                    "lemon_upgrade.jpeg",
                    "apple_upgrade.jpeg",
                    "orange_upgrade.jpeg",
                    "dragonfruit_upgrade.jpeg",
                    "watermelone_upgrade.jpeg",
                ]
SCALE_FACTOR = 0.6
GRAY_FILTER = 0.95
COLOR_MASK = [0.098,0.098,0.098]
FILENAME_CUTOFF = -5

def resize_player(image:np.array)->np.array:
    """
    Resize the fruit player.
    :param image: the image to resize
    :return:resized image
    """
    return resize(image, (image.shape[0]*SCALE_FACTOR, image.shape[1]*SCALE_FACTOR))


def recolor_player(image:np.array)->np.array:
    """
    Recolor the fruit player.
    :param image: the image to recolor
    :return:recolored fruit image
    """
    gray_image = color.rgb2gray(image)
    mask = gray_image > GRAY_FILTER
    image[mask] = COLOR_MASK
    return image


def remodel_player(player: str):
    """
    Remodel and save the fruit player.
    :param player: the file name of the fruit image
    """
    image = plt.imread(fr"original_pictures\{player}")
    resized_image = resize_player(image)
    image_color = recolor_player(resized_image)
    plt.imsave(fr"resized_pictures\resized_image_{LIST_PLAYER_FILES.index(player)}{player[:FILENAME_CUTOFF]}.jpeg",
               (image_color*255).astype(np.uint8))

if __name__ == "__main__":
    for player in LIST_PLAYER_FILES:
        remodel_player(player)




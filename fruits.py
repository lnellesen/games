"""Fruit size configurator."""
import numpy as np
from skimage.transform import resize
import matplotlib.pyplot as plt

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

def reshape_player(file: str)-> np.ndarray:
    im = plt.imread(file)
    res = resize(im, (im.shape[1]*0.9, im.shape[0]*0.9))
    return res


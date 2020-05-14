# add_noise
import random
import scipy.interpolate as spi
import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie
import numpy as np


def add_noise(y_list):
    for i in range(1, len(y_list)):
        rad = random.randint(1, 50)
        if random.random() <= 0.5:
            rad *= -1
        if i % 129 == 0:
            y_list[i] += rad

    return y_list


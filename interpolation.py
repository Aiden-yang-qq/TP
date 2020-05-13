# interpolation

import matplotlib.pyplot as plt
import matplotlib.image as mp_img
import numpy as np
import scipy.interpolate as spi
import Image_extraction as Ie


def interpolation(x_old, y_old):
    x_new = np.linspace(0, x_old[-1], x_old[-1] + 1)
    for kind in ['slinear', 'quadratic', 'cubic']:
        f = spi.interp1d(x_old, y_old, kind=kind)
        y_new = f(x_new)
        plt.plot(x_new, y_new, label=str(kind))
    return x_new, y_new


if __name__ == '__main__':
    pic_4 = mp_img.imread('pic4.jpg')
    xList, yList = Ie.extraction(pic_4)
    x_arr = np.array(xList)
    y_arr = np.array(yList)

    plt.plot(x_arr, y_arr, 'ro')
    x, y = interpolation(x_arr, y_arr)

    plt.legend(loc='lower right')
    plt.show()

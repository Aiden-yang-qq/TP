# interpolate

import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi
from add_noise import noise
import Image_extraction as Ie


def interpolate(x_old, y_old):
    try:
        x_new = np.linspace(0, x_old[-1] - 1, x_old[-1])
        for kind in ['slinear', 'quadratic', 'cubic']:
            f = spi.interp1d(x_old, y_old, kind=kind)
            y_new = f(x_new)
            plt.plot(x_new, y_new, label=str(kind))
        plt.legend(loc='lower right')
        plt.show()
        return x_new, y_new
    except IOError as err:
        print('Error!:', err)


if __name__ == '__main__':
    # pic = mp_img.imread('pic4.jpg')
    pic = mp_img.imread('Figure_1.jpg')
    # plt.imshow(pic)
    # plt.show()

    xList, yList = Ie.extraction(pic)
    yListNew = noise(yList, 10)

    # x_arr = np.array(xList)
    # y_arr = np.array(yList)

    # plt.plot(x_arr, y_arr, 'ro')
    # x, y = interpolate(xList, yList)
    # x, y = interpolate(x_arr, y_arr)

    # plt.legend(loc='lower right')
    # plt.show()
    plt.figure()
    plt.plot(xList, yList, 'ro')
    plt.plot(xList, yListNew, 'g-.')
    plt.grid()

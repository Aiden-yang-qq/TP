# interpolate

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate as spi


def interpolate(x_old, y_old):
    try:
        x_new = np.arange(x_old[0], x_old[-1] + 1)
        for kind in ['slinear', 'quadratic', 'cubic']:
            f = spi.interp1d(x_old, y_old, kind=kind)  # interp1d的插值范围要在原x_old的范围之内
            y_new = f(x_new)
            plt.plot(x_new, y_new, label=str(kind))
        plt.legend(loc='lower right')
        plt.show()
        return x_new, y_new
    except IOError as err:
        print('Error!:', err)


if __name__ == '__main__':
    import matplotlib.image as mp_img
    import Image_extraction as Ie
    from add_noise import noise

    # pic_ = mp_img.imread('Figure_1.jpg')
    pic_ = mp_img.imread('pic4.jpg')
    plt.imshow(pic_)
    plt.grid()
    plt.show()

    x, y = Ie.extraction(pic_, 60)
    xarr = np.array(x)
    yarr = np.array(y)

    y_n = noise(yarr, 5)

    # plt.figure()
    plt.plot(x, y, 'ro')
    # plt.plot(x, y_n)
    # plt.grid()
    xnew, ynew = interpolate(x, y)

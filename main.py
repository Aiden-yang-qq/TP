import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mp_img
from Algorithm import Image_extraction as Ie
from Algorithm.interpolation import interpolate
from Algorithm.add_noise import noise, noise_all


if __name__ == '__main__':
    pic_ = mp_img.imread('pic4.jpg')
    # pic_ = mp_img.imread('Figure_1.jpg')

    pic_gray = Ie.gray_scale(pic_)
    xList, yList = Ie.extraction(pic_, 60)
    y_noise = noise(yList, 5)
    y_noise_all = noise_all(yList)
    y_nn = np.array(yList) + y_noise_all

    plt.imshow(pic_)
    xnew, ynew = interpolate(xList, y_nn)

    plt.plot(xList, y_nn, '.')

    plt.grid()
    plt.show()

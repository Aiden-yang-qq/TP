import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie
import numpy as np
from add_noise import noise, noise_all
from interpolation import interpolate

if __name__ == '__main__':
    pic_ = mp_img.imread('pic4.jpg')
    # pic_ = mp_img.imread('Figure_1.jpg')

    pic_gray = Ie.gray_scale(pic_)
    xList, yList = Ie.extraction(pic_, 60)
    y_noise = noise(yList, 5)
    y_noise_all = noise_all(yList)
    y_nn = np.array(yList) + y_noise_all

    # plt.figure()
    plt.imshow(pic_)
    # xnew, ynew = interpolate(xList, y_noise)
    xnew, ynew = interpolate(xList, y_nn)

    # plt.plot(xList, yList, 'r')
    # plt.plot(xList, y_noise, 'g.')
    plt.plot(xList, y_nn, '.')

    plt.grid()
    plt.show()

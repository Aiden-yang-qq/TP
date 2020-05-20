import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie
from add_noise import noise
from interpolation import interpolate
import cv2
from PIL import Image

if __name__ == '__main__':
    pic_ = mp_img.imread('pic4.jpg')
    # pic_ = mp_img.imread('Figure_1.jpg')

    pic_gray = Ie.gray_scale(pic_)
    xList, yList = Ie.extraction(pic_, 60)
    y_noise = noise(yList, 5)

    # plt.figure()
    plt.imshow(pic_)
    xnew, ynew = interpolate(xList, y_noise)

    # plt.plot(xList, yList, 'r')
    plt.plot(xList, y_noise, 'g.')

    plt.grid()
    plt.show()

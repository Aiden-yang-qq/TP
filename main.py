import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie
from add_noise import add_noise
from interpolation import interpolation
import cv2
from PIL import Image

if __name__ == '__main__':
    # pic_ = mp_img.imread('pic4.jpg')
    pic_ = mp_img.imread('Figure_1.jpg')
    # plt.imshow(pic_)
    # plt.show()

    xList, yList = Ie.extraction(pic_)
    yListNew = add_noise(yList)

    xnew, ynew = interpolation(xList, yListNew)

    # I = Image.open('Figure_1.jpg')
    # # I = Image.open('pic4.jpg')
    # I.show()
    # L = I.convert('L')
    # L.show()

    plt.figure()
    plt.plot(xList, yList, 'r')
    plt.plot(xList, yListNew, 'g.')
    plt.imshow(pic_)
    plt.grid()
    plt.show()

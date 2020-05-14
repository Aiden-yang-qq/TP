import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie
from add_noise import add_noise
from interpolation import interpolation
import cv2
from PIL import Image

if __name__ == '__main__':
    pic_4 = mp_img.imread('pic4.jpg')
    xList, yList = Ie.extraction(pic_4)
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
    plt.imshow(pic_4)
    plt.grid()
    plt.show()

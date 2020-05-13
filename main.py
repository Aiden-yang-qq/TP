import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie

if __name__ == '__main__':
    pic_4 = mp_img.imread('pic4.jpg')
    xList, yList = Ie.extraction(pic_4)

    plt.figure()
    plt.plot(xList, yList, 'r.')
    plt.imshow(pic_4)
    plt.grid()
    plt.show()

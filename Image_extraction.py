# 曲线提取 curve extraction
import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import numpy as np


def extraction(pic_):
    """
    将图片矩阵中的曲线提取出来
    :param pic_: 图片矩阵
    :return: 曲线的横纵坐标
    """
    count = 0
    x_list = []
    y_list = []
    pic__ = gray_scale(pic_)
    pic_new = np.swapaxes(pic__, 1, 0)
    shape_i = pic_new.shape[0]
    shape_j = pic_new.shape[1]
    for i in range(shape_i):
        for j in range(shape_j):
            # if int(pic_new[i][j][0]) == int(pic_new[i][j][1]) == int(pic_new[i][j][2]) == 0:  # RGB=[0,0,0]
            if int(pic_new[i][j][0]) == 0:
                count += 1
                x_list.append(i)
                y_list.append(j)
                break
    return x_list, y_list


def gray_scale(pic_):
    """
    将图片中的曲线灰度化
    :param pic_: 图片矩阵
    :return: 灰度化后的图片矩阵
    """
    pic__ = np.array(pic_)
    pic__.flags.writeable = True  # 将矩阵读写置为可读
    shape_i = pic__.shape[0]
    shape_j = pic__.shape[1]
    for i in range(shape_i):
        for j in range(shape_j):
            if pic__[i][j][0] <= 60 and pic__[i][j][1] <= 120 and pic__[i][j][2] <= 160:
                pic__[i][j] = np.array([0, 0, 0], dtype='uint8')
            else:
                pic__[i][j] = np.array([255, 255, 255], dtype='uint8')
    return pic__


if __name__ == '__main__':
    # pic = mp_img.imread('pic4.jpg')
    pic = mp_img.imread('Figure_1.jpg')
    pic_n = gray_scale(pic)
    # plt.imshow(pic_n)

    xList, yList = extraction(pic)
    x_arr = np.array(xList)
    y_arr = np.array(yList)

    plt.imshow(pic)
    plt.plot(x_arr, y_arr, 'ro')
    plt.show()

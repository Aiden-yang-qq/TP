# 曲线提取 curve extraction
import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import numpy as np


def extraction(pic_, n_dot=20):
    """
    将图片矩阵中的曲线提取出来
    :param pic_:图片矩阵
    :param n_dot: 想要提取的点数数量（默认从曲线上提取20个点）
                  一般提取出的点数量会小于n_dot，因为在程序中会筛选掉一部分不合要求的点
    :return: 曲线的横纵坐标
    """
    count = 0
    x_list = []
    y_list = []
    pic__ = gray_scale(pic_)
    pic_new = np.swapaxes(pic__, 1, 0)
    shape_i = pic_new.shape[0]
    shape_j = pic_new.shape[1]
    gap = shape_i // n_dot
    print(shape_i, n_dot, gap)
    for i in range(shape_i):  # 扫x轴
    # for i in range(0, shape_i, gap):  # 扫x轴
        for j in range(shape_j):  # 扫y轴
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
            # if pic__[i][j][0] <= 60 and pic__[i][j][1] <= 120 and pic__[i][j][2] <= 160:
            if int(pic__[i][j][0]) + int(pic__[i][j][1]) + int(pic__[i][j][2]) <= 340:
                pic__[i][j] = np.array([0, 0, 0], dtype='uint8')
            else:
                pic__[i][j] = np.array([255, 255, 255], dtype='uint8')
    return pic__


if __name__ == '__main__':
    pic = mp_img.imread('pic4.jpg')
    # pic = mp_img.imread('Figure_1.jpg')
    pic_n = gray_scale(pic)
    plt.imshow(pic_n)

    xList, yList = extraction(pic, 10)
    x_arr = np.array(xList)
    y_arr = np.array(yList)

    # plt.imshow(pic)
    plt.plot(x_arr, y_arr, 'r.')
    plt.show()

# 曲线提取 curve extraction
import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import numpy as np


def extraction(pic_):
    count = 0
    x_list = []
    y_list = []
    pic_new = np.swapaxes(pic_, 1, 0)
    shape_i = pic_new.shape[0]
    shape_j = pic_new.shape[1]
    for i in range(0, shape_i):
        for j in range(5, shape_j, 5):
            if int(pic_new[i][j - 5][0]) - int(pic_new[i][j][0]) > 195:
                if int(pic_new[i][j - 5][1]) - int(pic_new[i][j][1]) > 135:
                    if int(pic_new[i][j - 5][2]) - int(pic_new[i][j][2]) > 100:
                        count += 1
                        x_list.append(i)
                        y_list.append(j)
                        break
    return x_list, y_list


if __name__ == '__main__':
    # pic = mp_img.imread('pic4.jpg')
    pic = mp_img.imread('Figure_1.jpg')
    # plt.imshow(pic)
    # plt.show()

    xList, yList = extraction(pic)
    x_arr = np.array(xList)
    y_arr = np.array(yList)

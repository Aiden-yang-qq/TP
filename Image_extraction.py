# 曲线提取 curve extraction
import numpy as np
import cv2


def extraction(pic_):
    count = 0
    # pic_b = 255
    x_list = []
    y_list = []
    pic = np.swapaxes(pic_, 1, 0)
    shape_i = pic.shape[0]
    shape_j = pic.shape[1]
    for i in range(0, shape_i, 2):
        for j in range(1, shape_j):
            # if pic[i][j][0] <= 100 and pic[i][j][1] <= 150 and pic[i][j][2] <= 220:  # 选择想要的颜色区间
            # if pic[i][j][0] + pic[i][j][1] + pic[i][j][2] - pic[i][j - 1][0] - pic[i][j - 1][1] - pic[i][j - 1][2] > 500:
            if int(pic[i][j-1][0]) - int(pic[i][j][0]) > 200:
                count += 1
                x_list.append(i)
                # y_list.append(-1 * j)
                y_list.append(j)
                # print(i, j)
                # pic_b = 255
                break
            # pic_b = pic[i][j][0]
    return x_list, y_list

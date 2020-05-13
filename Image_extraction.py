import numpy as np


def extraction(pic_):
    count = 0
    x_list = []
    y_list = []
    pic = np.swapaxes(pic_, 1, 0)
    shape_i = pic.shape[0]
    shape_j = pic.shape[1]
    for i in range(0, shape_i, 5):
        for j in range(shape_j):
            if pic[i][j][0] <= 10 and pic[i][j][1] <= 10 and pic[i][j][2] >= 245:
                count += 1
                x_list.append(i)
                y_list.append(-1 * j)
                # print(i, j)
                break
    return x_list, y_list

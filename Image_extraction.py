import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

pic_4 = mpimg.imread('pic4.jpg')
shape_i = pic_4.shape[0]
shape_j = pic_4.shape[1]

# pic_4_1 = pic_4[0]
# pic_4_1_1 = pic_4[0][0]
#
plt.imshow(pic_4)
# # plt.axis('off')
plt.show()


def extraction():
    count = 0
    x_list = []
    y_list = []
    for i in range(shape_i):
        for j in range(shape_j):
            if pic_4[i][j][0] != 255 or pic_4[i][j][1] != 255 or pic_4[i][j][2] != 255:
                count += 1
                x_list.append(i)
                y_list.append(j)
                # print(i, j)
    return count, x_list, y_list


if __name__ == '__main__':
    cou, xlist, ylist = extraction()
    print('Done!', cou)

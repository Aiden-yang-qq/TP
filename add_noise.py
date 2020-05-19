# add noise
# 目前加噪的点只能小于10个
import random
import sys


def noise(y_data, n):
    y_data_len = len(y_data)
    count = int(y_data_len / (n + 1))
    try:
        for i in range(count, y_data_len-2, count):
            if i < y_data_len:
                rad = random.randint(20, 50)
                if random.random() <= 0.5:
                    rad *= -1
                y_data[i] = y_data[i] + rad
        return y_data
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mp_img
    from Image_extraction import gray_scale, extraction

    # x = np.arange(-2 * np.pi, 2 * np.pi, 0.1 * np.pi)
    # y = np.sin(x)
    pic = mp_img.imread('Figure_1.jpg')
    # pic_n = gray_scale(pic)
    plt.imshow(pic)

    xList, yList = extraction(pic)
    x_arr = np.array(xList)
    y_arr = np.array(yList)

    y_new_arr = np.array(y_arr)
    y_new_arr.flags.writeable = True
    y_n = noise(y_new_arr, 5)

    # plt.figure()
    plt.plot(x_arr, y_arr, 'ro')
    plt.grid()
    plt.plot(x_arr, y_n)

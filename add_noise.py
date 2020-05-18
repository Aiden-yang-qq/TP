# add noise
# 目前加噪的点只能小于10个
import random
import sys


def noise(y_data, n):
    # y_data_n = [y_data[0]]
    y_data_n = []
    y_data_len = len(y_data)
    count = int(y_data_len / (n + 1))
    try:
        for i in range(y_data_len):
            if i % count == 0:
                rad = random.randint(20, 50)
                if random.random() <= 0.5:
                    rad *= -1
                y_data_n.append(y_data[i] + rad)
            else:
                y_data_n.append(y_data[i])
        # y_data_n.append(y_data[-1])
        return y_data_n
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

    y_n = noise(y_arr, 5)

    # plt.figure()
    plt.plot(x_arr, y_arr, 'ro')
    plt.grid()
    plt.plot(x_arr, y_n)

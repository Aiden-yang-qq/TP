# add noise
# 目前加噪的点只能小于10个
import random
import sys


def noise(y_data, n):
    y_data_n = [y_data[0]]
    try:
        for i in range(1, len(y_data) - 1):
            if i % int((len(y_data) - 1) / n) == 0:
                rad = random.randint(20, 50)
                if random.random() <= 0.5:
                    rad *= -1
                y_data_n.append(y_data[i] + rad)
            else:
                y_data_n.append(y_data[i])
        y_data_n.append(y_data[-1])
        return y_data_n
    except:
        print('Unexpected error:', sys.exc_info()[0])
        raise


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.arange(-2 * np.pi, 2 * np.pi, 0.1 * np.pi)
    y = np.sin(x)
    y_n = noise(y, 9)

    plt.figure()
    plt.plot(x, y, 'ro')
    plt.grid()
    # y_n = noise(y, 3)
    plt.plot(x, y_n)

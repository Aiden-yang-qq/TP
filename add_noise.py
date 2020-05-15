# add noise
import random


def noise(y_list, n):
    for i in range(1, len(y_list)):
        if i % int(len(y_list) / n) == 0:
            rad = random.randint(20, 50)
            if random.random() <= 0.5:
                rad *= -1
            y_list[i] += rad
    return y_list

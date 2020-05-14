# add_noise
import random


def add_noise(y_list):
    for i in range(1, len(y_list)):
        rad = random.randint(20, 50)
        if random.random() <= 0.5:
            rad *= -1
        if i % 129 == 0:
            y_list[i] += rad

    return y_list


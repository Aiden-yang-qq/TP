# data_splitting_integration.py 数据分割、整合模块
from matplotlib import pyplot as plt


def data_normalization(wheel_data):
    nor_data_list = []
    wd_max = max(wheel_data)
    wd_min = min(wheel_data)
    for d in wheel_data:
        nor_data = round((d - wd_min) / (wd_max - wd_min), 4)
        nor_data_list.append(nor_data)
    return nor_data_list


def wheel_data_integration(txt_list):
    left_optical = []
    if len(txt_list) == 6:
        for i, j, k in zip(txt_list[2][1], txt_list[4][1], txt_list[3][1]):
            left_sum = round((i + j + k), 4)
            left_optical.append(left_sum)
    return txt_list[2][0], left_optical


def wheel_data_splitting(txt_list):
    wheel_all_data = []
    for each_optical in txt_list:
        each_wheel_data = []
        dividing_line = round(sum(each_optical[1]) / len(each_optical[1]) + 0.65, 4)
        print('dividing_line:', dividing_line)
        plt.figure()
        plt.plot(each_optical[0], each_optical[1])
        plt.plot(each_optical[0], [dividing_line] * len(each_optical[0]))
        plt.grid()
        plt.show()
        for i in range(1, len(each_optical[1])):
            if each_optical[1][i] >= dividing_line:
                if each_optical[1][i - 1] <= each_optical[1][i] and each_optical[1][i] > each_optical[1][i + 1]:
                    if i < 20:
                        wheel_optical = each_optical[1][:i + 20]
                        each_wheel_data.append(wheel_optical)
                    elif 20 <= i <= len(each_optical[1]) - 20:
                        wheel_optical = each_optical[1][i - 20:i + 20]
                        each_wheel_data.append(wheel_optical)
                    else:
                        wheel_optical = each_optical[1][i - 20:]
                        each_wheel_data.append(wheel_optical)
                    i += 20
        wheel_all_data.append(each_wheel_data)
    return wheel_all_data

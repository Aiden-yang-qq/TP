# algorithm_main.py 算法主程序，仅供数据采集后的程序调用
# Algorithm文件夹下的程序均由此文件调用

import datetime
import numpy as np
import matplotlib.pyplot as plt


def read_txt(txt_name):
    with open(txt_name, 'r') as f:
        txt_list = f.readlines()
    return txt_list


def data_avg(average, length):
    avg_list = [average]
    avg_list *= length
    return avg_list


def main(file):
    date_time_list = []
    data_list = []
    datetime_list = []

    file_list = read_txt(file)

    for file in file_list:
        date_time = file[:23]
        data = file[30:39]
        date_time_type = datetime.datetime.fromisoformat(date_time)
        date_time_list.append(date_time)
        data_list.append(float(data))
        datetime_list.append(date_time_type)

    # 根据时间整理坐标系（时间——x轴）
    x_data = []
    start_datetime = datetime_list[0]
    for signal_time in datetime_list:
        time_delay = signal_time - start_datetime
        x_time = time_delay.seconds + time_delay.microseconds / 10 ** 6
        x_data.append(x_time)

    avg = np.mean(data_list, dtype=float)
    a_list = data_avg(avg, len(data_list))

    noise = np.array(data_list) - np.array(a_list)

    plt.figure()
    plt.plot(x_data, data_list)
    # plt.plot(x_data, noise)
    # plt.ylim(-0.01, 0.01)
    plt.grid()
    return data_list


if __name__ == '__main__':
    fl = 'D:\\jaysk\\Desktop\\TP\\dcs数据格式.txt'
    data = main(fl)

import collections
from datetime import datetime, timedelta
from logging import info

from Function.func_collection import read_txt
from Function.func_collection import writelines_txt
from matplotlib import pyplot as plt
import numpy as np
from Config import ConfigInfo

conf = ConfigInfo()


def read_fiber_data(rfd_data):
    """
    分析Data_***.txt文件
    :param rfd_data:
    :return:
    """
    data_all = []
    for d in rfd_data:
        wave_list = []
        d = d.replace('\t', ' ').split('|')
        for wave in d:
            if wave != ' \n':
                wave = wave.split()
                wave_list.append(wave)
        data_all.append(wave_list)
    return data_all


def read_fiber_data_simple(rfds_data):
    data_all = []
    for d in rfds_data:
        fiber_data_list = []
        d = d.replace('\t', ' ').split('|')
        date_time_temp = d[0].split()
        date_time = datetime.fromisoformat(date_time_temp[0].replace(',', ' '))
        temperature = float(date_time_temp[1])
        fiber_data = d[3].split()[:6]
        for i in fiber_data:
            # fiber_data_list.append(float(i))
            # TODO 修改数据格式，float小数点后保留4位小数
            fiber_data_list.append(float(i))

        data_all.append([date_time, temperature, fiber_data_list])
    return data_all


def time_temp_wave(ttw_data):
    datetime_list = []
    temp_list = []
    wave_list = []
    for d in ttw_data:
        datetime_list.append(d[0])
        temp_list.append(d[1])
        wave_list.append(d[2])

    # 时间重置到100000microsecond
    counter = 0
    datetime_new_list = []
    time_microsecond = timedelta(microseconds=100000)  # 默认采集频率是10Hz
    if datetime_list[100] - datetime_list[0] == timedelta(seconds=1):  # 采集频率是100Hz
        time_microsecond = timedelta(microseconds=10000)
    elif datetime_list[2000] - datetime_list[0] == timedelta(seconds=1):  # 采集频率是2kHz
        time_microsecond = timedelta(microseconds=500)

    for i in range(len(datetime_list) - 1):
        if datetime_list[i + 1] - datetime_list[i] == timedelta(seconds=1):
            counter = i + 1
            break
    original_datetime = datetime_list[counter]
    for j in range(-1 * counter, len(datetime_list) - counter):
        new_datetime = original_datetime + j * time_microsecond
        datetime_new_list.append(new_datetime)
    return datetime_new_list, temp_list, wave_list


def wave_collection(wave_list):
    wave_1 = []
    wave_2 = []
    wave_3 = []
    wave_4 = []
    wave_5 = []
    wave_6 = []
    for w in wave_list:
        wave_1.append(w[0])
        wave_2.append(w[1])
        wave_3.append(w[2])
        wave_4.append(w[3])
        wave_5.append(w[4])
        wave_6.append(w[5])
    return [wave_1, wave_2, wave_3, wave_4, wave_5, wave_6]


def time_wave(tw_time, tw_wave):
    try:
        tw_all_list = []
        for wave in tw_wave:
            if len(tw_time) == len(wave):
                tw_list = []
                for i in range(len(tw_time)):
                    tw_time_str = str(tw_time[i])
                    wave_str = str(wave[i])
                    if len(tw_time_str) == 19:
                        tw_time_str += '.000'
                    elif len(tw_time_str) == 26:
                        tw_time_str = tw_time_str[:23]
                    if len(wave_str) != 9:
                        wave_str += (9 - len(wave_str)) * '0'
                    # 数据格式：'2020-07-01 16:02:41.600 1534.2053\n'（二者取其一）
                    tw_list.append(tw_time_str.replace('.', ':') + ',' + wave_str + '\n')
                    # 数据格式：'2020-03-02 11:27:38:041,1,8,1,1550.2507,\n'（二者取其一）
                    # tw_time_str = tw_time_str.replace('.', ':')
                    # tw_list.append(tw_time_str + ',1,8,1,' + wave_str + ',\n')

                tw_all_list.append(tw_list)
        return tw_all_list
    except Exception as e:
        info('optical_fiber:', e)


def data_integration(tw_time, tw_wave):
    try:
        tw_all_list = []
        wave_max_set = []
        new_tw_wave = []

        car_weight_data = conf.weight_data()
        # tw_all_list.append(tw_time)
        optical_order = [2, 0, 4, 1, 3, 5]
        for i_oo in optical_order:
            new_tw_wave.append(tw_wave[i_oo] * 4)
        new_tw_wave *= 2
        for wave in new_tw_wave:
            if len(wave) != 0:
                # wave_str = [tw_time + '\n']
                wave_str = []
                for w in wave:
                    # w_str = str(int(w * 10000)) + '\n'
                    w_str = int(w * 10000)
                    wave_str.append(w_str)

                wave_dict = dict(collections.Counter(wave_str))
                wave_max = max(wave_dict, key=wave_dict.get)
                wave_max_set.append(wave_max)
                tw_all_list.append(wave_str)

        new_wave = []
        tw_arr = np.array(tw_all_list)
        if len(tw_arr) == len(wave_max_set):
            for i, j in zip(tw_arr, wave_max_set):
                tw_single = i - j
                new_wave.append(tw_single)

        wave_display(new_wave)
        return tw_all_list
    except Exception as e:
        info('optical_fiber:', e)


def wave_display(new_wave):
    plt.figure()
    plt.subplot(231)
    plt.plot(new_wave[0])
    plt.grid()
    plt.subplot(232)
    plt.plot(new_wave[2])
    plt.grid()
    plt.subplot(233)
    plt.plot(new_wave[4])
    plt.grid()
    plt.subplot(234)
    plt.plot(new_wave[1])
    plt.grid()
    plt.subplot(235)
    plt.plot(new_wave[3])
    plt.grid()
    plt.subplot(236)
    plt.plot(new_wave[5])
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # p = 'D:\\jaysk\\Desktop\\TP\\optical_fiber_data\\2020-07-01\\Available\\Data_20200701_160241.txt'
    p = 'D:\\jaysk\\Desktop\\TP\\optical_fiber_data\\2020-07-01\\Available\\Data_20200701_171736.txt'
    data = read_txt(p)
    d_a = read_fiber_data_simple(data)
    ttw_date_list, ttw_temp_list, ttw_wave_list = time_temp_wave(d_a)
    wave_all = wave_collection(ttw_wave_list)

    start_time = str(ttw_date_list[0])[:-7]
    # tw_txt = time_wave(ttw_date_list, wave_all)
    tw_txt = data_integration(start_time, wave_all)

    # 将6个传感器的数据保存成txt
    # save_path = 'D:\\jaysk\\Desktop\\TP\\optical_fiber_data\\2020-07-01\\Available\\Data_20200701_160241'
    save_path = 'D:\\jaysk\\Desktop\\TP\\optical_fiber_data\\2020-07-01\\Available\\Data_20200701_171736'
    for i in range(len(tw_txt)):
        writelines_txt(save_path + '\\%s.txt' % str(i + 1), tw_txt[i])

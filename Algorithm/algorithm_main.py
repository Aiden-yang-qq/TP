# algorithm_main.py 算法主程序，仅供数据采集后的程序调用
# Algorithm文件夹下的程序均由此文件调用
from datetime import datetime as dt
from Function.func_collection import read_txt


def data_avg(average, length):
    avg_list = [average]
    avg_list *= length
    return avg_list


def al_main(file):
    date_time_list = []
    data_list = []
    datetime_list = []

    file_list = read_txt(file)

    # 提取时间和数据
    for file in file_list:
        data = 0.0
        file_date_data = file.strip().split(',')
        date_time = file_date_data[0]
        if len(file_date_data) == 6:
            data = file_date_data[4]
        elif len(file_date_data) == 2:
            data = file_date_data[1]
        date_time_type = dt.fromisoformat(date_time)
        date_time_list.append(date_time)
        data_list.append(float(data))
        datetime_list.append(date_time_type)

    # 根据时间整理坐标系（时间——x轴）
    x_data = []
    start_datetime = datetime_list[0]
    for signal_time in datetime_list:
        time_delay = signal_time - start_datetime
        x_time = 24 * 3600 * time_delay.days + time_delay.seconds + (time_delay.microseconds / 10 ** 6)
        x_data.append(x_time)
    return x_data, data_list

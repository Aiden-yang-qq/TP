# -*- coding: utf-8 -*-
from logging import info
from os import getcwd
from time import time, sleep, ctime

# from matplotlib import pyplot as plt
from Algorithm.data_splitting_integration import optical_data_splitting, optical_data_to_wheel
from Config import ConfigInfo
from Database.data_storage import car_json_integration, write_json
from Database.data_collection import format_conversion
from Database.scanning_interface import database_creation


def main_exe():
    # 配置文件的信息读取
    conf = ConfigInfo()
    o_f_frequency = int(conf.get_optical_fiber_frequency())
    print('当前采样频率:%sHz' % o_f_frequency)

    # 主程序路径读取
    main_path = getcwd()
    # main_path = path.realpath(getcwd())
    # main_path = path.dirname(path.realpath(argv[0]))

    # 数据预处理
    format_conversion(main_path)

    all_wheel_data = []
    try:
        info('---------------------------------------')
        info(ctime())
        print('数据正在处理，请稍等……')
        a = time()

        # 检测数据库中txt和AEI文件并读取
        json_file_name, folders, all_car_aei = database_creation(main_path)

        # 数据库中有txt文件后，对folders读取，并做车轮数据提取整合，然后保存成json文件
        optical_fiber_data = optical_data_splitting(folders, o_f_frequency)
        # all_wheel_data的输出格式:三维列表[32个车轮×2个车轮车×3600个数据][32×2×3600]的矩阵
        x_wheel_data, all_wheel_data = optical_data_to_wheel(optical_fiber_data, o_f_frequency)

        # 将车轮数据保存成json文件
        if len(json_file_name) != 0:
            all_car_set_json = car_json_integration(json_file_name, x_wheel_data, all_wheel_data, all_car_aei)
            write_json(json_file_name, all_car_set_json)

        b = time()
        print('数据处理耗时:%.4fs，程序结束！' % (b - a))
        sleep(1)
        info('本次数据处理已完成，共耗时%.4fs:' % (b - a))
        info('---------------------------------------')
    except Exception as e:
        info('main_error:', e)

    # info('---------------------------------------')
    # info(ctime())
    # print('数据正在处理，请稍等……')
    # a = time()
    # main_path = getcwd()
    # folders = database_creation(main_path)
    # b = time()
    # print('数据处理耗时:%.4fs，程序结束！' % (b - a))
    # sleep(3)
    # info('本次数据处理已完成，共耗时%.4fs:' % (b - a))
    # info('---------------------------------------')
    return all_wheel_data


if __name__ == '__main__':
    main_exe()

    # plt.figure()
    # plt.plot(x_wheel_data, all_wheel_data[0][0])
    # plt.grid()
    # plt.show()

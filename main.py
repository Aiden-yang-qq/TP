# -*- coding: utf-8 -*-
from logging import info
from os import getcwd
from time import time, sleep, ctime

from Algorithm.data_splitting_integration import optical_data_splitting, optical_data_to_wheel
from Database.data_storage import car_json_integration, write_json
from Database.scanning_interface import database_creation


def main_exe():
    # folders = {}
    all_wheel_data = []
    try:
        info('---------------------------------------')
        info(ctime())
        print('数据正在处理，请稍等……')
        a = time()
        main_path = getcwd()
        json_file_name, folders, all_car_aei = database_creation(main_path)

        # TODO 数据库中有txt文件后，对folders读取，并做车轮数据提取整合，然后保存成json文件
        optical_fiber_data = optical_data_splitting(folders, 100)
        x_wheel_data, all_wheel_data = optical_data_to_wheel(optical_fiber_data, 100)

        # 将车轮数据保存成json文件
        # json_file = read_json()
        all_car_set_json = car_json_integration(json_file_name, x_wheel_data, all_wheel_data, all_car_aei)
        write_json(json_file_name, all_car_set_json)

        b = time()
        print('数据处理耗时:%.4fs，程序结束！' % (b - a))
        sleep(3)
        info('本次数据处理已完成，共耗时%.4fs:' % (b - a))
        info('---------------------------------------')
    except Exception as e:
        info(e)

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

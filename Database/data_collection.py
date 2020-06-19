# data_collection.py 数据采集模块
import os

from Algorithm.algorithm_main_test import main
from Database.data_storage import data_to_txt
from func_collection import make_directory


def wheel_no_collection(path, file_name):
    with open(path + '/' + file_name) as fi:
        file = fi.readline()
    return file


def optical_fiber_collection(path, folders):
    car_all = {}
    for folder in folders:
        car = {}

        parent_path = os.path.dirname(path)
        alg_path = make_directory(parent_path, folder)

        file_dir = path + '/' + folder
        file_list = os.listdir(file_dir)

        for file in file_list:
            file_path = file_dir + '/' + file
            data = main(file_path)

            # 输出到文件夹
            data_to_txt(path, file, data)

            # 存成字典备用
            car.update({file.split('.')[0]: data})  # 将每个车号下的txt文档添加到字典中
            car_all.update({folder: car})  # 将数据库中的每个车号添加到字典中
    return car_all


if __name__ == '__main__':
    # f = ['DF4-1111']

    # f_path = 'E:\\Python\\Pyinstaller\\TP\\Database\\Data_pool'
    f_path = 'E:/Python/Pyinstaller/TP/Database/Data_pool'
    f = os.listdir(f_path)

    fl = optical_fiber_collection(f_path, f)

    # f_path = 'D:\\jaysk\\Desktop\\TP'
    # f = '20200611085330.AEI'
    # fil = wheel_no_collection(f_path, f)

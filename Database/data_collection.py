# data_collection.py 数据采集模块
import os
from Algorithm.algorithm_main_test import main


def collection(path, folders):
    car_all = {}
    for folder in folders:
        car = {}

        file_dir = path + '/' + folder
        file_list = os.listdir(file_dir)

        for file in file_list:
            file_path = file_dir + '/' + file
            data = main(file_path)
            car.update({file.split('.')[0]: data})  # 将每个车号下的txt文档添加到字典中
            car_all.update({folder: car})   # 将数据库中的每个车号添加到字典中
    return car_all


if __name__ == '__main__':
    # f = ['DF4-1111']

    # f_path = 'E:\\Python\\Pyinstaller\\TP\\Database\\Data_pool'
    f_path = 'E:/Python/Pyinstaller/TP/Database/Data_pool'
    f = os.listdir(f_path)

    fl = collection(f_path, f)

# data_collection.py 数据采集模块
import os
from Algorithm.algorithm_main import main


def collection(path, folders):
    for folder in folders:
        car = {}
        file_dir = path + '/' + folder
        file_list = os.listdir(file_dir)

        for file in file_list:
            file_path = file_dir + '/' + file
            data = main(file_path)
            car = {file.split('.')[0]: data}

        car_all = {folder: car}
        return car_all


if __name__ == '__main__':
    f = ['DF4-1111']
    # f_path = 'E:\\Python\\Pyinstaller\\TP\\Database\\Data_pool'
    f_path = 'E:/Python/Pyinstaller/TP/Database/Data_pool'

    fl = collection(f_path, f)

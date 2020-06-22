# data_collection.py 数据采集模块
from os import path, listdir
from Algorithm.algorithm_main_test import main
from Database.data_storage import data_to_txt
from func_collection import make_directory


def wheel_no_collection(wnc_path, file_name):
    with open(wnc_path + '/' + file_name) as fi:
        file = fi.readline()
    return file


def optical_fiber_collection(ofc_path, folders):
    car_all = {}
    for folder in folders:
        car = {}

        parent_path = path.dirname(ofc_path)
        data_lib_path = parent_path + '/Data_lib'
        if path.exists(data_lib_path):  # 在Data_lib文件夹中新建各个车厢的文件夹
            alg_path = make_directory(data_lib_path, folder)

            file_dir = ofc_path + '/' + folder
            file_list = listdir(file_dir)

            for file in file_list:
                file_path = file_dir + '/' + file
                data = main(file_path)

                # 输出到文件夹
                file_open_path = alg_path + '/' + file
                data_to_txt(file_open_path, data)

                # 存成字典备用
                car.update({file.split('.')[0]: data})  # 将每个车号下的txt文档添加到字典中
                car_all.update({folder: car})  # 将数据库中的每个车号添加到字典中
    return car_all

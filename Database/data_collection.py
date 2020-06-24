# data_collection.py 数据采集模块
from os import path, listdir
from Algorithm.algorithm_main import main
from Database.data_storage import data_to_txt
from func_collection import make_directory
from shutil import rmtree


def wheel_no_collection(wnc_path, file_name):
    with open(wnc_path + '/' + file_name) as fi:
        file = fi.readline()
    return file


def optical_fiber_collection(ofc_path, folders):
    car_all = {}
    for folder in folders:
        car = {}
        folder_date = folder.split()[0].split('#')[1].split('-')
        parent_path = path.dirname(ofc_path)
        data_lib_path = parent_path + '\\Data_lib\\' + folder_date[0] + '\\' + folder_date[1] + '\\' + folder_date[2]
        if path.exists(data_lib_path):  # 在Data_lib文件夹中新建各个车厢的文件夹
            alg_path = make_directory(data_lib_path, folder)
            if alg_path is not None:
                file_dir = ofc_path + '/' + folder
                file_list = listdir(file_dir)

                for file in file_list:
                    if file.split('.')[1] == 'txt':
                        file_path = file_dir + '/' + file
                        data = main(file_path)  # 调用算法主程序

                        # 输出到文件夹
                        file_open_path = alg_path + '/' + file
                        data_to_txt(file_open_path, data)

                        # 存成字典备用
                        car.update({file.split('.')[0]: data})  # 将每个车号下的txt文档添加到字典中
                        car_all.update({folder: car})  # 将数据库中的每个车号添加到字典中
            else:
                rmtree(ofc_path)
                make_directory(path.dirname(ofc_path), 'Data_pool')
    return car_all

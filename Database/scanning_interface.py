# scanning_interface.py
# 扫描接口模块：扫描文件夹，有新的txt文档则调用数据采集模块
import os
import sys
import Config
import shutil


# def scan_path(dir_path):
#     # os.path.isdir(dir)
#     os.listdir(dir_path)


def current_file_path():
    return os.path.split(__file__)[0]


def scan_path(file_path):
    for top_tuple in os.walk(file_path):
        # print(top_tuple)  # top -- 根目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名】。
        return top_tuple


def mkdir(path, folder_name):
    folder = os.listdir(path)
    if folder_name not in folder:
        path_1 = path + '/' + folder_name
        os.makedirs(path_1)
    else:
        print('%s文件夹已存在！' % folder_name)


def car_no_list():
    conf = Config.ConfigInfo()
    _is_first_scan = conf.is_first_scan()

    original_folder_name = 'Data_pool'
    backup_folder_name = 'Data_pool_backup'
    cfp = current_file_path()
    data_pool_path = cfp + '/' + original_folder_name

    if not os.path.exists(data_pool_path):
        mkdir(cfp, original_folder_name)    # 创建原始数据的文件夹

    top_tuple = scan_path(data_pool_path)
    car_no_folders = top_tuple[1]

    if _is_first_scan:  # 检测是否是第一次扫描文件夹
        # mkdir(cfp, 'Data_pool_backup')  # 创建原始数据的备份文件夹
        mkdir(cfp, 'Data_lib')  # 创建经过算法后的数据库

    if len(car_no_folders) != 0:
        for car_no in car_no_folders:
            old_car_data_path = data_pool_path + '/' + car_no
            new_car_data_path = backup_folder_name + '/' + car_no
            try:
                shutil.copytree(old_car_data_path, new_car_data_path)
                shutil.rmtree(old_car_data_path)
            except Exception as e:
                print('异常：', e)
    return car_no_folders


# def car_file_backup():


if __name__ == '__main__':
    folders = car_no_list()

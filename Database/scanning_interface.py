# scanning_interface.py
# 扫描接口模块：扫描文件夹，有新的txt文档则调用数据采集模块
import os
import time
import Config
import shutil
import logging
from Database.data_collection import optical_fiber_collection
from func_collection import make_directory

logging.basicConfig(filename='logging_file.log', level=logging.DEBUG)


def current_file_path():
    return os.path.split(__file__)[0]


def scan_path(file_path):
    for top_tuple in os.walk(file_path):
        # print(top_tuple)  # top -- 根目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名】。
        return top_tuple


# def make_directory(path, folder_name):
#     # sub_path = ''
#     folder = os.listdir(path)
#     if folder_name not in folder:
#         sub_path = path + '/' + folder_name
#         os.makedirs(sub_path)
#     else:
#         print('%s文件夹已存在！' % folder_name)
#     # return sub_path


def database_creation():
    conf = Config.ConfigInfo()
    _is_first_scan = conf.is_first_scan()

    original_folder_name = 'Data_pool'  # 原始数据库的文件夹名称
    backup_folder_name = 'Data_pool_backup'  # 原始数据库备份的文件夹名称
    algorithm_folder_name = 'Data_lib'  # 经过算法后的数据库的文件夹名称

    cfp = current_file_path()
    data_pool_path = cfp + '/' + original_folder_name
    data_pool_back_path = cfp + '/' + backup_folder_name
    data_lib_path = cfp + '/' + algorithm_folder_name

    if not os.path.exists(data_pool_path):
        make_directory(cfp, original_folder_name)  # 创建原始数据库文件夹

    top_tuple = scan_path(data_pool_path)
    car_no_folders = top_tuple[1]

    if not os.path.exists(data_lib_path):
        try:
            make_directory(cfp, algorithm_folder_name)  # 创建经过算法后的数据库文件夹
        except Exception as e:
            logging.warning(e)

    # 创建备份数据库，同时将原始数据库中的内容复制进去
    # TODO 判断car_no_folder，空则等待数据传输，有内容则调用data_collection模块进行算法
    all_car = {}
    if len(car_no_folders) != 0:
        all_car = optical_fiber_collection(data_pool_path, car_no_folders)    # 进行数据采集
        for car_no in car_no_folders:
            old_car_data_path = data_pool_path + '/' + car_no
            new_car_data_path = data_pool_back_path + '/' + car_no
            try:
                shutil.copytree(old_car_data_path, new_car_data_path)
                shutil.rmtree(old_car_data_path)
            except Exception as e:
                logging.warning(e)
                # print('异常：', e)
        logging.info('----------------------------------------------------------------------------------------------')
    return all_car


if __name__ == '__main__':
    a = time.time()
    folders = database_creation()
    b = time.time()
    print('Time:', b - a)

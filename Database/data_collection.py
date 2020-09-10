# data_collection.py 数据采集模块
from datetime import datetime, timedelta
from logging import info
from os import path, listdir
from shutil import rmtree, move

from Algorithm.algorithm_main import al_main_1
from Config import ConfigInfo
from Database.data_storage import data_to_txt
from Function.func_collection import make_directory, read_txt, writelines_txt, folder_creation


def wheel_no_collection(wnc_path, file_name):
    with open(wnc_path + '/' + file_name) as fi:
        file = fi.readline()
    return file


def optical_fiber_collection(ofc_path, folders):
    all_nor_optical = []
    try:
        for folder in folders:
            car = {}
            fd = folder.split()[0].split('#')[1].split('-')  # fd:folder_date
            parent_path = path.dirname(ofc_path)
            data_lib_path = parent_path + '\\Data_lib\\' + fd[0] + '\\' + fd[1] + '\\' + fd[2]
            if path.exists(data_lib_path):  # 在Data_lib文件夹中新建各个车厢的文件夹
                alg_path = make_directory(data_lib_path, folder)
                if alg_path is not None:
                    car_all = {}
                    file_dir = ofc_path + '\\' + folder
                    file_list = listdir(file_dir)

                    for file in file_list:
                        if file.split('.')[1] == 'txt':
                            file_path = file_dir + '/' + file
                            data = al_main_1(file_path)  # 调用算法主程序

                            # 输出到文件夹
                            file_open_path = alg_path + '/' + file
                            each_nor_optical = data_to_txt(file_open_path, data)
                            if len(each_nor_optical) != 0:
                                all_nor_optical.append(each_nor_optical)

                            # 存成字典备用
                            car.update({file.split('.')[0]: data})  # 将每个车号下的txt文档添加到字典中
                            car_all.update({folder: car})  # 将数据库中的每个车号添加到字典中

                    if len(listdir(alg_path)) == 0:
                        rmtree(alg_path)
                else:
                    rmtree(ofc_path)
                    make_directory(path.dirname(ofc_path), 'Data_pool')
    except Exception as e:
        info(e)
        print(e)
    if len(all_nor_optical) > 0:
        return all_nor_optical
    else:
        return {}


def format_conversion(fc_path):
    """
    # TODO 读文件夹，存在文件则读取并进行格式转换，不存在则退出
    :param fc_path:该路径为主程序的绝对路径
    :return:
    """
    # 加载配置文件
    conf = ConfigInfo()
    original_db = conf.get_original_db_name()  # 获取Original_DB文件夹名称
    original_temp_db = conf.get_original_temp_db_name()  # 获取Original_temp_DB文件夹名称
    config_frequency = int(conf.get_optical_fiber_frequency())
    decimal_places = len(str(1 / config_frequency)) - 2

    # 创建所需文件夹
    fc_original_db_path = folder_creation(fc_path, original_db)
    fc_original_temp_db_path = folder_creation(fc_path, original_temp_db)

    # 从Original_temp_DB下读取文件进行处理
    txt_output = []
    txt_content = listdir(fc_original_temp_db_path)
    if len(txt_content) != 0:
        for txt_file_name in txt_content:
            if txt_file_name[-4:] == '.txt':
                txt_ = read_txt(fc_original_temp_db_path + '\\' + txt_file_name)  # txt文档读取
                _txt = txt_[1:]  # 数据截取

                # 时间格式获取
                date_time = txt_[0].strip()
                datetime_ = datetime.fromisoformat(date_time)
                time_delay = timedelta(microseconds=(10 ** 6 / config_frequency))

                for i in range(len(_txt)):
                    time_ = str(datetime_ + time_delay * i)
                    if len(_txt[i]) > 1:
                        format_time = ''
                        if len(time_) == 26:
                            format_time = time_[:20 + decimal_places].replace('.', ':')
                        elif len(time_) == 19:
                            format_time = time_ + ':' + '0' * decimal_places
                        txt_data = _txt[i].strip()
                        if len(txt_data) == 7:
                            txt_new_ = txt_data[:4] + '.' + txt_data[4:] + '0\n'
                            format_single_data = format_time + ',' + txt_new_
                            txt_output.append(format_single_data)
                        else:
                            # format_single_data = format_time + ',' + _txt[i].strip() + '\n'
                            format_single_data = format_time + ',' + _txt[i]
                            txt_output.append(format_single_data)
                if txt_file_name == '4.txt':
                    txt_file_name = '3.txt'
                elif txt_file_name == '5.txt':
                    txt_file_name = '4.txt'
                elif txt_file_name == '6.txt':
                    txt_file_name = '5.txt'
                elif txt_file_name == '3.txt':
                    txt_file_name = '6.txt'
                elif txt_file_name == '12.txt':
                    txt_file_name = '7.txt'
                elif txt_file_name == '11.txt':
                    txt_file_name = '8.txt'
                elif txt_file_name == '10.txt':
                    txt_file_name = '9.txt'
                elif txt_file_name == '8.txt':
                    txt_file_name = '10.txt'
                elif txt_file_name == '7.txt':
                    txt_file_name = '11.txt'
                elif txt_file_name == '9.txt':
                    txt_file_name = '12.txt'
                if len(txt_file_name) == 5:
                    txt_file_name = '0' + txt_file_name  # 统一文件名称：01.txt~12.txt
                writelines_txt(fc_original_db_path + '\\' + txt_file_name, txt_output)
                txt_output = []
            elif txt_file_name[-4:] == '.AEI':
                move(fc_original_temp_db_path + '\\' + txt_file_name, fc_original_db_path + '\\' + txt_file_name)

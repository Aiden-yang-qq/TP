# data_collection.py 数据采集模块
from os import path, listdir
from Algorithm.algorithm_main import al_main
from Database.data_storage import data_to_txt
from Function.func_collection import make_directory, read_txt,writelines_txt
from shutil import rmtree
from logging import info
from datetime import datetime, timedelta


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
                            data = al_main(file_path)  # 调用算法主程序

                            # 输出到文件夹
                            file_open_path = alg_path + '/' + file
                            each_nor_optical = data_to_txt(file_open_path, data)
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
    return all_nor_optical


def format_conversion(fc_path):
    txt_ = read_txt(fc_path)
    _txt = txt_[2:22]
    frequency = int(txt_[0])
    date_time = txt_[1].strip()

    datetime_ = datetime.fromisoformat(date_time)
    time_delay = timedelta(microseconds=(10 ** 6 / frequency))

    txt_output = []
    for i in range(len(_txt)):
        format_time = str(datetime_ + time_delay * i)[:-1 * (8 - len(str(1 / frequency)))].replace('.', ':')
        format_single_data = format_time + ',' + _txt[i].strip() + ','
        txt_output.append(format_single_data)

    # writelines_txt()
    return txt_output


if __name__ == '__main__':
    txt_paht = 'D:\\jaysk\\Desktop\\TP\\document\\data_standard_format.txt'
    fc = format_conversion(txt_paht)

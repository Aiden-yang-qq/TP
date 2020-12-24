# Function function module
from datetime import datetime
from logging import warning, info
from os import listdir, makedirs, path, remove
from shutil import rmtree

from zipfile import ZipFile, ZIP_DEFLATED


def folder_creation(fc_parent_path, folder_name):
    fc_path = fc_parent_path + '\\' + folder_name
    if not path.exists(fc_path):
        try:
            make_directory(fc_parent_path, folder_name)
        except Exception as e:
            warning(e)
    return fc_path


def make_directory(md_path, folder_name):
    sub_path = None
    folder = listdir(md_path)
    if folder_name not in folder:
        sub_path = md_path + '\\' + folder_name
        makedirs(sub_path)
    else:
        print('路径“%s”中已存在“%s”文件夹！' % (md_path, folder_name))
        info('路径“%s”中已存在“%s”文件夹！' % (md_path, folder_name))
    return sub_path


def make_empty_folder(mef_path, folder_name):
    """
    空文件夹创建
    :param mef_path: 创建路径
    :param folder_name: 空文件夹名称
    :return:
    """
    rmtree(mef_path + '\\' + folder_name)
    folder_creation(mef_path, folder_name)


def read_txt(txt_name):
    """
    .txt文件读取
    :param txt_name: 完整txt文件路径，例：'E:\\Python\\Pyinstaller\\TP\\Original_DB\\01.txt'
    :return:
    """
    with open(txt_name, 'r') as f:
        txt_list = f.readlines()
    return txt_list


def writelines_txt(wt_path, write_file):
    try:
        with open(wt_path, 'w') as fw:
            fw.writelines(write_file)
    except Exception as e:
        info('func_collection:', e)


def write_txt(wt_path, write_file):
    with open(wt_path, 'w') as fw:
        fw.write(write_file)


def time_reconstruct(date_time):
    """
    原始时间格式：例如：20200611 08:53:30
    重构后的时间格式：例如：2020-06-11 08:53:30
    :param date_time:
    :return:
    """
    new_date_time = ''
    if len(date_time) == 17:
        new_date_time = date_time[:4] + '-' + date_time[4:6] + '-' + date_time[6:8] + date_time[8:]
    return new_date_time


def date_time2datetime(date_time_str):
    """
    'YYYY-MM-DD HH:MM:SS'字符串格式的时间转换成datetime格式的时间
    :param date_time_str:
    :return:
    """
    return datetime.fromisoformat(date_time_str)


def year_mon_day_folder_generation(original_path, date_time_list):  # 建立年-月-日文件夹
    db_lib_year_dir = original_path + '\\' + date_time_list[0]
    db_lib_month_dir = db_lib_year_dir + '\\' + date_time_list[1]
    db_lib_day_dir = db_lib_month_dir + '\\' + date_time_list[2]
    try:
        if not path.exists(db_lib_year_dir):
            make_directory(original_path, date_time_list[0])
        if not path.exists(db_lib_month_dir):
            make_directory(db_lib_year_dir, date_time_list[1])
        if not path.exists(db_lib_day_dir):
            make_directory(db_lib_month_dir, date_time_list[2])
    except Exception as e:
        warning(e)


def pack_json(json_dir, json_trans_path):
    """
    json文件打包压缩函数
    :param json_dir:
    :param json_trans_path:
    :return:
    """
    json_name = json_dir.split('\\')[-1]
    json_zip_name = json_name.replace('.json', '.zip')
    json_zip_dir = json_trans_path + '\\' + json_zip_name
    with ZipFile(json_zip_dir, 'w', ZIP_DEFLATED) as f:
        f.write(json_dir, json_name)


def remove_json(re_json_path):
    file_list = listdir(re_json_path)
    for file_name in file_list:
        if file_name[-4:] == 'json':
            json_dir = re_json_path + '\\' + file_name
            if path.exists(json_dir):
                remove(json_dir)

# Function 功能模块
from os import listdir, makedirs, path
from logging import warning


def make_directory(md_path, folder_name):
    # sub_path = md_path + '\\' + folder_name
    sub_path = None
    folder = listdir(md_path)
    if folder_name not in folder:
        sub_path = md_path + '\\' + folder_name
        makedirs(sub_path)
    else:
        print('%s文件夹已存在！' % folder_name)
    return sub_path


def read_txt(txt_name):
    with open(txt_name, 'r') as f:
        txt_list = f.readlines()
    return txt_list


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

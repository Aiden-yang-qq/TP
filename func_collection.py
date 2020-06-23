# Function 功能模块
from os import listdir, makedirs


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

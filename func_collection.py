# Function 功能模块
from os import listdir, makedirs


def make_directory(md_path, folder_name):
    sub_path = md_path + '/' + folder_name
    folder = listdir(md_path)
    if folder_name not in folder:
        sub_path = md_path + '/' + folder_name
        makedirs(sub_path)
    else:
        print('%s文件夹已存在！' % folder_name)
    return sub_path

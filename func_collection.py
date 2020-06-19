# Function 功能模块
import os


def make_directory(path, folder_name):
    sub_path = ''
    folder = os.listdir(path)
    if folder_name not in folder:
        sub_path = path + '/' + folder_name
        os.makedirs(sub_path)
    else:
        print('%s文件夹已存在！' % folder_name)
    return sub_path

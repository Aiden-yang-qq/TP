# 扫描文件夹，有新的txt文档则读取并调用算法程序
import os
import sys
import Config


def scan_path(dir_path):
    # os.path.isdir(dir)
    os.listdir(dir_path)


def file_name(file_path):
    for root, folder, files in os.walk(file_path):
        print(root)  # root：当前目录路径
        print(folder)  # folder：当前路径下所有子目录
        print(files)  # files：当前路径下所有非目录子文件
        return root, folder, files


def main(path):
    scan_path(path)


def current_file_path():
    print(os.getcwd())
    return sys.path[0]


if __name__ == '__main__':
    conf = Config.ConfigInfo()
    conf.first_scan()

    # fp = 'E:\\Python\\Pyinstaller\\TP'
    # main(file_path)
    # r, d, f = file_name(fp)
    # print(current_file_path())

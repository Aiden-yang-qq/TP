# 扫描文件夹，有新的txt文档则读取并调用算法程序
import os
import Config


def scan_path(dir_path):
    # os.path.isdir(dir)
    os.listdir(dir_path)


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(root)  # root：当前目录路径
        print(dirs)  # dirs：当前路径下所有子目录
        print(files)  # files：当前路径下所有非目录子文件
        return root, dirs, files


def main(path):
    scan_path(path)


if __name__ == '__main__':
    conf = Config.ConfigInfo()
    conf.first_scan()
    # file_path = 'D:/jaysk/OneDrive/Working/Python/TP'
    # # main(file_path)
    # r, d, f = file_name(file_path)

from os import getcwd
from time import time, sleep
from logging import info

from Database.scanning_interface import database_creation

if __name__ == '__main__':
    try:
        a = time()
        # main_path = path.dirname(__file__)
        # print('main_path:', main_path)
        # print(getcwd())
        main_path = getcwd()
        folders = database_creation(main_path)
        b = time()
        print('数据处理耗时%.4fs:' % (b - a))
        sleep(3)
    except Exception as e:
        info(e)

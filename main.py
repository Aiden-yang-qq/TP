from os import getcwd
from time import time, sleep, ctime
from logging import info

from Database.scanning_interface import database_creation

if __name__ == '__main__':
    try:
        info('---------------------------------------')
        info(ctime())
        print('数据正在处理，请稍等……')
        a = time()
        main_path = getcwd()
        folders = database_creation(main_path)
        b = time()
        print('数据处理耗时:%.4fs，程序结束！' % (b - a))
        sleep(3)
        info('本次数据处理已完成，共耗时%.4fs:' % (b - a))
        info('---------------------------------------')
    except Exception as e:
        info(e)

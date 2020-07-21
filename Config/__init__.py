from sys import argv
from os import path
from configparser import ConfigParser


class ConfigInfo:
    def __init__(self):
        self.cf_path = path.dirname(path.realpath(argv[0]))  # 取出当前文件所处路径
        self.file_path = self.cf_path + '\\Config\\config.ini'
        # print('config_path:', path.realpath(self.file_path))
        self.cp = ConfigParser()
        # self.cp.read(self.file_path, encoding='utf-8-sig')
        self.cp.read(self.file_path)

    def is_first_scan(self):
        first_scan = self.cp.get('SCAN', 'is_first_scan')  # SCAN中的FIRST_SCAN值
        fs = str_to_bool(first_scan)
        if fs:
            print('首次扫描文件夹，将数据库中所有的文件夹及数据全部读取！')
            self.cp.set('SCAN', 'is_first_scan', 'False')  # 设置SCAN中FIRST_SCAN的值
            self.cp.write(open(self.file_path, 'w'))  # 将新的值写入.ini配置文件中
            # TODO 扫描文件夹，获取全部数据列表
            # TODO 调用算法程序
        else:
            print('非第一次扫描文件夹：此次扫描只处理新的数据！')
            # TODO 获取新增数据列表
            # TODO 调用算法程序
        return fs

    def get_original_db_name(self):
        original_db_name = self.cp.get('DATABASE', 'original_db_name')
        return original_db_name

    def get_original_temp_db_name(self):
        original_temp_db_name = self.cp.get('DATABASE', 'original_temp_db_name')
        return original_temp_db_name

    def get_optical_fiber_frequency(self):
        optical_fiber_frequency = self.cp.get('PRE_SET', 'optical_fiber_frequency')
        return optical_fiber_frequency

    def json_storage_path(self):
        json_save_path = self.cp.get('PATH', 'json_save_path')
        return json_save_path


def str_to_bool(string):
    return True if string.lower() == 'true' else False

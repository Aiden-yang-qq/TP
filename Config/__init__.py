from sys import argv
from os import path
from configparser import ConfigParser


class ConfigInfo:
    def __init__(self):
        self.cf_path = path.dirname(path.realpath(argv[0]))  # 取出当前文件所处路径
        # self.file_path = self.cf_path + '\\Config\\config.ini'
        self.file_path = 'D:\\Config\\config.ini'
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

    def json_transfer_path(self):
        json_trans_path = self.cp.get('PATH', 'json_transfer_path')
        return json_trans_path

    def speed_json_path(self):
        speed_json_path = self.cp.get('PATH', 'speed_json_path')
        return speed_json_path

    def speed_json_delay_time(self):
        speed_json_delay_time = self.cp.get('GAP', 'speed_json_delay_time')
        return speed_json_delay_time

    def weight_data(self):
        left_wheel_weight = self.cp.get('WEIGHT', 'left_wheel_weight')
        right_wheel_weight = self.cp.get('WEIGHT', 'right_wheel_weight')
        axle_weight = self.cp.get('WEIGHT', 'axle_weight')
        return left_wheel_weight, right_wheel_weight, axle_weight

    def time_gap_value(self):
        gap_value = self.cp.get('GAP', 'time_gap')
        return gap_value

    def unbalanced_loads_coe(self):
        unbalanced_coefficient = self.cp.get('LOADS', 'unbalances_loads_')
        return unbalanced_coefficient

    def adjust_data(self):
        adjust_0 = self.cp.get('ADJUST', 'adjust_0')
        adjust_1 = self.cp.get('ADJUST', 'adjust_1')
        adjust_2 = self.cp.get('ADJUST', 'adjust_2')
        adjust_3 = self.cp.get('ADJUST', 'adjust_3')
        adjust_4 = self.cp.get('ADJUST', 'adjust_4')
        adjust_5 = self.cp.get('ADJUST', 'adjust_5')
        return adjust_0, adjust_1, adjust_2, adjust_3, adjust_4, adjust_5

    def display_limits(self):
        max_limits = self.cp.get('LIMITS', 'limits_max')
        min_limits = self.cp.get('LIMITS', 'limits_min')
        return max_limits, min_limits

    def optical_wavelength(self):
        opt_l1 = self.cp.get('OPTICAL', 'opt_1550')
        opt_r1 = self.cp.get('OPTICAL', 'opt_1534')
        opt_l2 = self.cp.get('OPTICAL', 'opt_1562')
        opt_r2 = self.cp.get('OPTICAL', 'opt_1541')
        opt_l3 = self.cp.get('OPTICAL', 'opt_1554')
        opt_r3 = self.cp.get('OPTICAL', 'opt_1566')
        return opt_l1, opt_r1, opt_l2, opt_r2, opt_l3, opt_r3

    def optical_difference(self):
        opt_1 = self.cp.get('OPTICAL', 'opt_1st')
        opt_2 = self.cp.get('OPTICAL', 'opt_2nd')
        opt_3 = self.cp.get('OPTICAL', 'opt_3rd')
        return opt_1, opt_2, opt_3

    def optical_wave_diff(self):
        opt_wave_diff = self.cp.get('OPTICAL', 'opt_wave_diff')
        return opt_wave_diff


def str_to_bool(string):
    return True if string.lower() == 'true' else False

from configparser import ConfigParser


class ConfigInfo:
    def __init__(self):
        # self.cp = cp
        # self.file_name = file_name
        self.cp = ConfigParser()
        self.cp.read('config.ini')

    def first_scan(self):
        first_scan = self.cp.get('SCAN', 'first_scan')  # SCAN中的FIRST_SCAN值
        print('1:', first_scan, type(first_scan))
        fs = str_to_bool(first_scan)
        print('fs:', fs, type(fs))
        if str_to_bool(first_scan):
            print('2:', fs, type(fs))
            self.cp.set('SCAN', 'first_scan', 'False')  # 设置SCAN中FIRST_SCAN的值
            self.cp.write(open('config.ini', 'w'))  # 将新的值写入.ini配置文件中
            re_get = self.cp.get('SCAN', 'first_scan')
            print('3:', re_get, type(re_get))
        else:
            print('else')
        print(self.cp.get('SCAN', 'first_scan'))


def str_to_bool(string):
    return True if string.lower() == 'true' else False


if __name__ == '__main__':
    conf = ConfigInfo()
    conf.first_scan()

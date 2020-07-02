# scanning_interface.py
# 扫描接口模块：扫描文件夹，有新的txt文档则调用数据采集模块
from os import path, walk, listdir
# from Config import ConfigInfo
from shutil import copytree, rmtree, move
from logging import basicConfig, DEBUG, warning, info
from Database.data_collection import optical_fiber_collection
from Function.func_collection import make_directory, read_txt, time_reconstruct, year_mon_day_folder_generation, folder_creation

basicConfig(filename='logging_file.log', level=DEBUG)


def current_file_path():
    # print('path.split:', path.split(__file__)[0])
    # print('path.dirname:', path.dirname(__file__))
    return path.split(__file__)[0]


def scan_path(file_path):
    for top_tuple in walk(file_path):
        return top_tuple  # top -- 根目录下的每一个文件夹(包含它自己), 产生3-元组 (dirpath, dirnames, filenames)【文件夹路径, 文件夹名字, 文件名】。


def database_creation(dc_path):
    # conf = ConfigInfo()
    # _is_first_scan = conf.is_first_scan()

    # 光纤数据库文件夹名称命名
    data_base_name = 'DB'  # 存储所有数据的文件夹
    odb_folder_name = 'Original_DB'  # 存储原始数据的文件夹

    # 压力应变片数据库文件夹名称命名
    data_pressure_name = 'DB_pressure'  # 存储所有数据的文件夹
    odb_pressure_name = 'Original_DB_pressure'  # 存储原始数据的文件夹

    # 共用数据库文件夹名称命名
    original_folder_name = 'Data_pool'  # 原始数据库的文件夹名称
    backup_folder_name = 'Data_pool_backup'  # 原始数据库备份的文件夹名称
    algorithm_folder_name = 'Data_lib'  # 经过算法后的数据库的文件夹名称

    # 光纤数据库文件夹路径生成
    cfp = dc_path + '\\' + data_base_name  # “DB”文件夹路径
    odb = dc_path + '\\' + odb_folder_name  # “Original_DB”文件夹路径
    data_lib_path = cfp + '\\' + algorithm_folder_name  # “Data_lib”文件夹路径
    data_pool_path = cfp + '\\' + original_folder_name  # “Data_pool”文件夹路径
    data_pool_back_path = cfp + '\\' + backup_folder_name  # “Data_pool_backup”文件夹路径

    # 压力应变片数据库文件夹路径生成
    cfp_pre = dc_path + '\\' + data_pressure_name  # “DB_pressure”文件夹路径
    odb_pre = dc_path + '\\' + odb_pressure_name  # “Original_DB_pressure”文件夹路径
    data_lib_pre_path = cfp_pre + '\\' + algorithm_folder_name  # “Data_lib”文件夹路径
    data_pool_pre_path = cfp_pre + '\\' + original_folder_name  # “Data_pool”文件夹路径
    data_pool_back_pre_path = cfp_pre + '\\' + backup_folder_name  # “Data_pool_backup”文件夹路径

    # 光纤数据库文件夹创建
    folder_creation(dc_path, data_base_name)  # 创建数据库根目录"DB"文件夹
    folder_creation(cfp, original_folder_name)  # 创建原始数据库"Data_pool"文件夹
    folder_creation(cfp, algorithm_folder_name)  # 创建经过算法后的数据库"Data_lib"文件夹

    # 压力应变片数据库文件夹创建
    folder_creation(dc_path, data_pressure_name)  # 创建数据库根目录"DB"文件夹
    folder_creation(cfp_pre, original_folder_name)  # 创建原始数据库"Data_pool"文件夹
    folder_creation(cfp_pre, algorithm_folder_name)  # 创建经过算法后的数据库"Data_lib"文件夹

    # 生成车号文件夹，并将Original_DB和Original_DB_pressure中的文件复制进去
    odb_dir, new_folder_name = original_db_scanning(dc_path, odb_folder_name)
    odb_pre_dir, new_folder_pre_name = original_db_scanning(dc_path, odb_pressure_name)

    # 在Data_lib文件夹中建立年、月、日文件夹
    if new_folder_name is not '':
        db_folder_date = new_folder_name.split()[0].split('#')[1].split('-')  # 从new_folder_name文件夹中获取年、月
        year_mon_day_folder_generation(data_lib_path, db_folder_date)  # 在“Data_lib”文件夹下创建年月日文件夹
    if new_folder_pre_name is not '':
        db_folder_pre_date = new_folder_pre_name.split()[0].split('#')[1].split('-')  # 从new_folder_name文件夹中获取年、月
        year_mon_day_folder_generation(data_lib_pre_path, db_folder_pre_date)  # 在“Data_lib”文件夹下创建年月日文件夹

    # 在Data_pool_backup文件夹中建立年、月、日文件夹
    if len(new_folder_name) > 1:
        new_fo_name = new_folder_name.replace(':', '_')
        car_folder_dir = data_pool_path + '\\' + new_fo_name
        car_folder_backup_dir = data_pool_back_path + '\\' + new_fo_name
        if not path.exists(car_folder_backup_dir):  # 判断'Data_pool_backup'是否已经有计算过的文件夹存在
            if not path.exists(car_folder_dir):
                make_directory(data_pool_path, new_fo_name)
                try:
                    odb_list = listdir(odb_dir)
                    for f in odb_list:
                        odb_file_dir = odb_dir + '/' + f
                        move(odb_file_dir, car_folder_dir)
                except Exception as e:
                    info(e)
        else:
            print('%s文件夹在%s中已存在，%s中的数据已经过计算，请重新检查数据！' % (new_fo_name, backup_folder_name, odb_folder_name))
            info('%s文件夹在%s中已存在，%s中的数据已经过计算，请重新检查数据！' % (new_fo_name, backup_folder_name, odb_folder_name))
            rmtree(odb)  # 删除已经计算过的'Original_DB'文件夹
            make_directory(dc_path, odb_folder_name)  # 新建'Original_DB'文件夹

    top_tuple = scan_path(data_pool_path)
    car_no_folders = top_tuple[1]

    # 创建备份数据库，同时将原始数据库中的内容复制进去
    all_car = {}
    if len(car_no_folders) != 0:
        all_car = optical_fiber_collection(data_pool_path, car_no_folders)  # 进行数据采集
        if len(all_car) != 0:
            for car_no in car_no_folders:
                cn_date = str(car_no).split()[0].split('#')[1].split('-')
                car_no_date = cn_date[0] + '\\' + cn_date[1] + '\\' + cn_date[2]
                old_car_data_path = data_pool_path + '\\' + car_no
                new_car_data_path = data_pool_back_path + '\\' + car_no_date + '\\' + car_no
                try:
                    copytree(old_car_data_path, new_car_data_path)
                    rmtree(old_car_data_path)
                except Exception as e:
                    warning(e)
    return all_car


def original_db_scanning(ods_path, odb_folder_name):
    # 原始数据存放的文件夹名称：odb_folder_name:Original_DB和Original_DB_pressure
    odb_path = ''
    new_folder_name = ''
    parent_odb_list = listdir(ods_path)

    if odb_folder_name in parent_odb_list:
        odb_path = ods_path + '\\' + odb_folder_name
        aei = search_aei_suffix(odb_path, odb_folder_name)
        if aei is not None:
            car_no, date_time, carriage_no = aei_file_analysis(aei)
            new_folder_name = car_no + '#' + date_time
    else:
        print('%s文件夹不存在，请检查数据是否存放正确！' % odb_folder_name)
        info('%s文件夹不存在，请检查数据是否存放正确！' % odb_folder_name)
        try:
            make_directory(ods_path, odb_folder_name)
        except Exception as e:
            warning(e)
    return odb_path, new_folder_name


def search_aei_suffix(ss_path, odb_folder_name):
    """
    在ss_path路径下搜索文件后缀，如果存在.AEI和.txt文件则对该文件进行读取
    :param ss_path: 需要搜索AEI文件的路径文件夹
    :param odb_folder_name:
    :return:
    """
    sfx_set = {}
    sfx_list = []
    aei_txt = None
    all_set = {'.AEI', '.txt'}
    file_list = listdir(ss_path)
    if len(file_list) != 0:
        for file in file_list:
            sfx = path.splitext(file)
            sfx_list.append(sfx[1])
            sfx_set = set(sfx_list)
            if sfx[1] == '.AEI':
                aei_dir = ss_path + '/' + file
                aei_txt = read_txt(aei_dir)  # 读取AEI文件
        diff = all_set.difference(sfx_set)
        if len(diff) != 0:
            for s in diff:
                if s not in sfx_list:
                    print('找不到%s文件，请重新检查数据！' % s)
                    info('找不到%s文件，请重新检查数据！' % s)
                    rmtree(ss_path)  # 删除'Original_DB'文件夹
                    make_directory(path.dirname(ss_path), odb_folder_name)  # 新建'Original_DB'文件夹
                    return None
    else:
        print('%s文件夹中无可用文件，请重新传入文件！' % odb_folder_name)
        info('%s文件夹中无可用文件，请重新传入文件！' % odb_folder_name)
    return aei_txt


def aei_file_analysis(aei_file):
    """
    [aei_property[0]:'AEM',                 （固定标识）
     aei_property[1]:'1130',                车号
     aei_property[2]: '20200611 08:53:30',  采集日期时间
     aei_property[3]:'N',                   （可能表示方向）
     aei_property[4]:'00',                  （数据，但是未采集到）
     aei_property[5]:'008',                 车厢数
     aei_property[6]:'0032',                轴数
     aei_property[7]:'\n']
    :param aei_file:.AEI文件
    :return:car_no：车号；date_time：日期时间；carriage_no：车厢号
    """
    car_no = ''
    date_time = ''
    carriage_no = ''
    if aei_file is not None:
        aei_property = aei_file[0].split(',')
        car_no = aei_property[1]
        date_time = aei_property[2]
        date_time = time_reconstruct(date_time)
        carriage_no = aei_property[5]
        # print(date_time)
    return car_no, date_time, carriage_no

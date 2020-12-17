# data_collection.py 数据采集模块
from datetime import datetime, timedelta
from logging import info
from os import listdir, path
from shutil import rmtree, move

# from collections import Counter
# import matplotlib.pyplot as plt
from numpy import array, vstack

from Algorithm.algorithm_main import al_main
from Config import ConfigInfo
from Database.data_storage import data_to_txt
from Function.func_collection import make_directory, read_txt, writelines_txt, folder_creation

conf = ConfigInfo()


def wheel_no_collection(wnc_path, file_name):
    with open(wnc_path + '/' + file_name) as fi:
        file = fi.readline()
    return file


def optical_fiber_collection(ofc_path, folders):
    all_nor_optical = []
    try:
        for folder in folders:
            car = {}
            fd = folder.split()[0].split('#')[1].split('-')  # fd:folder_date
            parent_path = path.dirname(ofc_path)
            data_lib_path = parent_path + '\\Data_lib\\' + fd[0] + '\\' + fd[1] + '\\' + fd[2]
            if path.exists(data_lib_path):  # 在Data_lib文件夹中新建各个车厢的文件夹
                alg_path = make_directory(data_lib_path, folder)
                if alg_path is not None:
                    car_all = {}
                    file_dir = ofc_path + '\\' + folder
                    file_list = listdir(file_dir)

                    for file in file_list:
                        if file.split('.')[1] == 'txt':
                            file_path = file_dir + '/' + file
                            data = al_main(file_path)  # 调用算法主程序

                            # 输出到文件夹
                            file_open_path = alg_path + '/' + file
                            each_nor_optical = data_to_txt(file_open_path, data)
                            if len(each_nor_optical) != 0:
                                all_nor_optical.append(each_nor_optical)

                            # 存成字典备用
                            car.update({file.split('.')[0]: data})  # 将每个车号下的txt文档添加到字典中
                            car_all.update({folder: car})  # 将数据库中的每个车号添加到字典中

                    if len(listdir(alg_path)) == 0:
                        rmtree(alg_path)
                else:
                    rmtree(ofc_path)
                    make_directory(path.dirname(ofc_path), 'Data_pool')
    except Exception as e:
        info(e)
        print(e)

    # 对传感器的数据进行修正（基本信号标准统一化）
    if len(all_nor_optical) > 0:
        new_optical = []
        move_set = []
        positive_set = []
        negative_set = []
        amplitude_set = []
        coefficient_set = []
        new_all_nor_optical_tran = []
        all_single_nor_optical_arr_tran = []

        all_nor_optical_arr = array(all_nor_optical)
        all_nor_optical_arr_tran = all_nor_optical_arr.transpose((1, 0, 2))  # 将传感器数据提取出来，后续进行校准
        for i in range(len(all_nor_optical_arr_tran[1])):
            positive_ = []
            negative_ = []
            positive_value = 0
            negative_value = 0
            # amplitude_ = round(sum(abs(all_nor_optical_arr_tran[1][i][-1000:])) / 1000, 4)
            # amplitude_ = max(abs(all_nor_optical_arr_tran[1][i][-5000:]))
            # amplitude_counter = Counter(all_nor_optical_arr_tran[1][i][-5000:])
            for a in all_nor_optical_arr_tran[1][i][-5000:]:
                if a > 0:
                    positive_.append(a)
                elif a < 0:
                    negative_.append(a)

            if len(positive_) != 0:
                positive_value = round(sum(positive_) / len(positive_), 5)
            if len(negative_) != 0:
                negative_value = round(sum(negative_) / len(negative_), 5)

            need_to_move = round((positive_value + negative_value) / 2, 5)

            positive_set.append(positive_value)
            negative_set.append(negative_value)
            move_set.append(need_to_move)

            single_nor_optical_arr_tran = all_nor_optical_arr_tran[1][i] - need_to_move
            all_single_nor_optical_arr_tran.append(single_nor_optical_arr_tran)

            amplitude_ = round(positive_value - need_to_move, 4)
            amplitude_set.append(amplitude_)

        mean_positive = round(sum(positive_set) / len(positive_set), 4)
        mean_negative = round(sum(negative_set) / len(negative_set), 4)
        mean_standard = round((mean_positive - mean_negative) / 2, 4)

        for i in range(len(all_single_nor_optical_arr_tran)):
            if len(all_single_nor_optical_arr_tran) == len(amplitude_set):
                coefficient_ = round(mean_standard / amplitude_set[i], 4)
                coefficient_set.append(coefficient_)
                # new_single_optical = all_nor_optical_arr_tran[1][i] * coefficient_
                new_single_optical = all_single_nor_optical_arr_tran[i] * coefficient_
                # new_optical.append(new_single_optical)
                new_optical.append(new_single_optical)

        if len(all_nor_optical_arr_tran[0]) == len(new_optical):
            new_all_nor_optical = vstack((all_nor_optical_arr_tran[0], new_optical))
            new_all_nor_optical_reshape = new_all_nor_optical.reshape((2, len(new_optical), -1))
            new_all_nor_optical_tran = new_all_nor_optical_reshape.transpose((1, 0, 2))

        # plt.ion()
        # plt.figure()
        # for i in range(len(all_nor_optical_arr_tran[1])):
        #     plt.subplot(2, 6, i + 1)
        #     plt.plot(all_nor_optical_arr_tran[1][i])
        #     plt.ylim((-0.184, 0.52))
        #     plt.grid()
        # # plt.show()
        # plt.figure()
        # for i in range(len(new_optical)):
        #     plt.subplot(2, 6, i + 1)
        #     plt.plot(new_optical[i])
        #     plt.ylim((-0.184, 0.52))
        #     plt.grid()
        # plt.show()

        # return new_all_nor_optical_tran
        return all_nor_optical
    else:
        return {}


def format_conversion(fc_path):
    """
    # TODO 读文件夹，存在文件则读取并进行格式转换，不存在则退出
    :param fc_path:该路径为主程序的相对路径
    :return:
    """
    fc_path = 'D:'
    # 加载配置文件
    original_db = conf.get_original_db_name()  # 获取Original_DB文件夹名称
    original_temp_db = conf.get_original_temp_db_name()  # 获取Original_temp_DB文件夹名称
    config_frequency = int(conf.get_optical_fiber_frequency())
    decimal_places = len(str(1 / config_frequency)) - 2

    # 创建所需文件夹
    fc_original_db_path = folder_creation(fc_path, original_db)
    fc_original_temp_db_path = folder_creation(fc_path, original_temp_db)

    # 从Original_temp_DB下读取文件进行处理
    txt_output = []
    txt_content = listdir(fc_original_temp_db_path)
    if len(txt_content) != 0:
        for txt_file_name in txt_content:
            if txt_file_name[-4:] == '.txt':
                txt_ = read_txt(fc_original_temp_db_path + '\\' + txt_file_name)  # txt文档读取
                _txt = txt_[1:]  # 数据截取

                # 时间格式获取
                date_time = txt_[0].strip()
                datetime_ = datetime.fromisoformat(date_time)
                time_delay = timedelta(microseconds=(10 ** 6 / config_frequency))

                for i in range(len(_txt)):
                    time_ = str(datetime_ + time_delay * i)
                    if len(_txt[i]) > 1:
                        format_time = ''
                        if len(time_) == 26:
                            format_time = time_[:20 + decimal_places].replace('.', ':')
                        elif len(time_) == 19:
                            format_time = time_ + ':' + '0' * decimal_places
                        txt_data = _txt[i].strip()
                        if len(txt_data) == 7:
                            txt_new_ = txt_data[:4] + '.' + txt_data[4:] + '0\n'
                            format_single_data = format_time + ',' + txt_new_
                            txt_output.append(format_single_data)
                        else:
                            # format_single_data = format_time + ',' + _txt[i].strip() + '\n'
                            format_single_data = format_time + ',' + _txt[i]
                            txt_output.append(format_single_data)
                if txt_file_name == '4.txt':
                    txt_file_name = '3.txt'
                elif txt_file_name == '5.txt':
                    txt_file_name = '4.txt'
                elif txt_file_name == '6.txt':
                    txt_file_name = '5.txt'
                elif txt_file_name == '3.txt':
                    txt_file_name = '6.txt'
                elif txt_file_name == '12.txt':
                    txt_file_name = '7.txt'
                elif txt_file_name == '11.txt':
                    txt_file_name = '8.txt'
                elif txt_file_name == '10.txt':
                    txt_file_name = '9.txt'
                elif txt_file_name == '8.txt':
                    txt_file_name = '10.txt'
                elif txt_file_name == '7.txt':
                    txt_file_name = '11.txt'
                elif txt_file_name == '9.txt':
                    txt_file_name = '12.txt'
                if len(txt_file_name) == 5:
                    txt_file_name = '0' + txt_file_name  # 统一文件名称：01.txt~12.txt
                writelines_txt(fc_original_db_path + '\\' + txt_file_name, txt_output)
                txt_output = []
            elif txt_file_name[-4:] == '.AEI':
                move(fc_original_temp_db_path + '\\' + txt_file_name, fc_original_db_path + '\\' + txt_file_name)
            # elif txt_file_name[-5:] == '.json':
            #     move(fc_original_temp_db_path + '\\' + txt_file_name, fc_original_db_path + '\\' + txt_file_name)


# def read_speed_json():
#     speed_set = []
#     start_time = time()
#     speed_km_ = 70 * ones((32, 2))
#     speed_json_path = conf.speed_json_path()
#     speed_json_delay_time = conf.speed_json_delay_time()
#     while True:
#         list_name = listdir(speed_json_path)
#         for file_name in list_name:
#             if file_name[-4:] == 'json':
#                 json_f = speed_json_path + '\\' + file_name
#                 with open(json_f, 'r', encoding='utf-8-sig') as f:
#                     data = load(f)
#                     for speed_ in data['axleSpeeds']:
#                         speed_set.append(speed_['speed'])
#                     speed_trans = array(speed_set).reshape((2, int(len(speed_set) / 2))).transpose((1, 0))
#                     speed_km = around(speed_trans * 1.6093439975538, 2)
#                 if path.exists(json_f):
#                     remove(json_f)
#                 progressbar(0, 0)
#                 return speed_km
#
#         end_time = time()
#         delay_time = round(end_time - start_time, 2)
#
#         progressbar(int(delay_time), int(speed_json_delay_time))
#         if delay_time >= int(speed_json_delay_time):
#             print('历时%ss，未查询到速度信息json文件' % int(delay_time))
#             break
#         sleep(0.2)
#     return speed_km_
#
#
# def progressbar(cur, total):
#     if cur + total != 0:
#         stdout.write('\r')
#         stdout.write('等待速度信息json文件还剩：%ss' % (total - cur))
#         stdout.flush()
#     else:
#         stdout.write('\r')
#         stdout.write('已接收到速度信息json文件，正在进行速度读取！')
#         stdout.flush()
#     if cur >= total:
#         stdout.write('\n')

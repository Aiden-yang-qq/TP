from collections import Counter as c_Counter
from datetime import datetime
from logging import basicConfig, info
from os import getcwd
# from os import getcwd, path as os_path
# from sys import path as sys_path
from time import strftime, localtime

from matplotlib import pyplot as plt
from numpy import array, around, append as np_append
from scipy.signal import butter, lfilter

# from Algorithm.al_func_collection import butter_lowpass_filter
# from Algorithm.data_splitting_integration import data_normalization
# from Function.func_collection import read_txt
from Config import ConfigInfo

# print(sys_path)
# right_now_path = os_path.dirname(__file__)
# parent_path = os_path.dirname(right_now_path)
# sys_path.append(parent_path)

basicConfig(filename='Weight_info.log', level='DEBUG')

conf = ConfigInfo()
# 获取采样频率，对于不同采集频率设定不同的时间间隔
o_f_frequency = int(conf.get_optical_fiber_frequency())

# 获取左右车轮和轴的标准重量
# weight_left=0.667t=2/3t
# weight_right=0.667t=2/3t
# weight_axle=0.766t=23/30t
car_weight_data = conf.weight_data()
standard_left_weight = float(car_weight_data[0])
standard_right_weight = float(car_weight_data[1])
standard_axle_weight = float(car_weight_data[2])

# time_gap还需要根据列车行驶速度确定（速度越快，时间间隔越短）
time_gap = 0.1
if o_f_frequency == 100:
    time_gap = 4
elif o_f_frequency == 2000:
    # time_gap = 0.3
    time_gap = float(conf.time_gap_value())

single_wheel_data_count = int(o_f_frequency * time_gap) * 2


def butter_lowpass_filter(data, cutoff_fre, fs, order=5):
    """
    低通滤波器
    :param data: 数据
    :param cutoff_fre:截止频率
    :param fs: 采样频率
    :param order:
    :return:
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff_fre / nyq
    b, a = butter(order, normal_cutoff, analog=False)
    y_output = lfilter(b, a, data)
    return y_output


def data_normalization(data_n):
    normalization_data = []
    max_data = max(data_n)
    for d in data_n:
        normalization_data.append(round(d / max_data, 4))
    return normalization_data


def read_txt(txt_name):
    """
    .txt文件读取
    :param txt_name: 完整txt文件路径，例：'E:\\Python\\Pyinstaller\\TP\\Original_DB\\01.txt'
    :return:
    """
    with open(txt_name, 'r') as f:
        txt_list = f.readlines()
    return txt_list


def read_fiber_data(rfd_data):
    """
    分析Data_***.txt文件
    :param rfd_data:
    :return:
    """
    data_all = []
    for d in rfd_data:
        wave_list = []
        d = d.replace('\t', ' ').split('|')
        for wave in d:
            if wave != ' \n':
                wave = wave.split()
                wave_list.append(wave)
        data_all.append(wave_list)
    return data_all


def read_fiber_data_simple(rfds_data):
    try:
        data_all = []
        if rfds_data[0][:4] == 'Time':
            for d in rfds_data:
                if d[:4] != 'Time':
                    fiber_data_list = []
                    d = d.replace('\t0', '').split('\t')
                    # date_time = datetime.fromisoformat(d[0][:-4])
                    fiber_data = d[1:]
                    for i in fiber_data:
                        i = i.replace('\n', '')
                        # i_float = round(float(i), 4)  # 修改数据格式，float小数点后保留4位小数
                        i_float = float(i)  # 修改数据格式
                        fiber_data_list.append(i_float)
                    # data_all.append([date_time, fiber_data_list])
                    data_all.append([fiber_data_list])

        else:
            for d in rfds_data:
                fiber_data_list = []
                d = d.replace('\t', ' ').split('|')
                date_time_temp = d[0].split()
                date_time = datetime.fromisoformat(date_time_temp[0].replace(',', ' '))
                temperature = float(date_time_temp[1])
                fiber_data = d[3].split()[:6]
                for i in fiber_data:
                    # fiber_data_list.append(float(i))
                    # TODO 修改数据格式，float小数点后保留4位小数
                    fiber_data_list.append(float(i))

                data_all.append([date_time, temperature, fiber_data_list])
        return data_all
    except Exception as e:
        info(e)


def time_temp_wave(ttw_data):
    datetime_list = []
    temp_list = []
    wave_list = []
    for d in ttw_data:
        if len(d) == 1:
            wave_list.append(d[0])
        else:
            datetime_list.append(d[0])
            temp_list.append(d[1])
            wave_list.append(d[2])

    # # 时间重置到100000microsecond
    # counter = 0
    # datetime_new_list = []
    # time_microsecond = timedelta(microseconds=100000)  # 默认采集频率是10Hz
    # if datetime_list[100] - datetime_list[0] == timedelta(seconds=1):  # 采集频率是100Hz
    #     time_microsecond = timedelta(microseconds=10000)
    # elif datetime_list[2000] - datetime_list[0] == timedelta(seconds=1):  # 采集频率是2kHz
    #     time_microsecond = timedelta(microseconds=500)
    #
    # for i in range(len(datetime_list) - 1):
    #     if datetime_list[i + 1] - datetime_list[i] == timedelta(seconds=1):
    #         counter = i + 1
    #         break
    # original_datetime = datetime_list[counter]
    # for j in range(-1 * counter, len(datetime_list) - counter):
    #     new_datetime = original_datetime + j * time_microsecond
    #     datetime_new_list.append(new_datetime)
    # return datetime_new_list, temp_list, wave_list
    return wave_list


def wave_collection(wave_list):
    wave_1 = []
    wave_2 = []
    wave_3 = []
    wave_4 = []
    wave_5 = []
    wave_6 = []
    for w in wave_list:
        wave_1.append(w[0])
        wave_2.append(w[1])
        wave_3.append(w[2])
        wave_4.append(w[3])
        wave_5.append(w[4])
        wave_6.append(w[5])
    return [wave_1, wave_2, wave_3, wave_4, wave_5, wave_6]


def time_wave(tw_time, tw_wave):
    try:
        tw_all_list = []
        for wave in tw_wave:
            if len(tw_time) == len(wave):
                tw_list = []
                for i in range(len(tw_time)):
                    tw_time_str = str(tw_time[i])
                    wave_str = str(wave[i])
                    if len(tw_time_str) == 19:
                        tw_time_str += '.000'
                    elif len(tw_time_str) == 26:
                        tw_time_str = tw_time_str[:23]
                    if len(wave_str) != 9:
                        wave_str += (9 - len(wave_str)) * '0'
                    # 数据格式：'2020-07-01 16:02:41.600 1534.2053\n'（二者取其一）
                    tw_list.append(tw_time_str.replace('.', ':') + ',' + wave_str + '\n')
                    # 数据格式：'2020-03-02 11:27:38:041,1,8,1,1550.2507,\n'（二者取其一）
                    # tw_time_str = tw_time_str.replace('.', ':')
                    # tw_list.append(tw_time_str + ',1,8,1,' + wave_str + ',\n')

                tw_all_list.append(tw_list)
        return tw_all_list
    except Exception as e:
        info('optical_fiber:', e)


# def data_integration(tw_time, tw_wave):
def data_integration(tw_wave):
    try:
        # tw_all_list = []
        wave_max_set = []
        new_tw_wave_ = []
        new_arr_wave_ = []

        # tw_all_list.append(tw_time)
        optical_order = [2, 0, 4, 1, 3, 5]
        for i_oo in optical_order:
            # new_tw_wave_.append(tw_wave[i_oo] * 4)
            new_tw_wave_.append(tw_wave[i_oo])
        new_tw_wave_ *= 2
        tw_arr = array(new_tw_wave_)

        for wave in tw_arr:
            if len(wave) != 0:
                # wave_str = [tw_time + '\n']
                # wave_str = []
                # for w in wave:
                #     # w_str = str(int(w * 10000)) + '\n'
                #     w_str = int(w * 10000)
                #     wave_str.append(w_str)

                # wave_dict = dict(c_Counter(wave_str))
                wave_dict = c_Counter(wave)
                wave_max = max(wave_dict, key=wave_dict.get)
                new_arr_wave_.append(wave - wave_max)
                wave_max_set.append(wave_max)
                # tw_all_list.append(wave_str)
                # tw_all_list.append(wave)

        # new_wave = []
        # # tw_arr = array(tw_all_list)
        #
        # if len(tw_arr) == len(wave_max_set):
        #     for i, j in zip(tw_arr, wave_max_set):
        #         tw_single = i - j
        #         new_wave.append(tw_single)

        wave_display(new_arr_wave_)
        return new_tw_wave_, new_arr_wave_
    except Exception as e:
        info('optical_fiber:', e)


def wave_display(new_wave):
    plt.ion()
    plt.figure()
    plt.subplot(231)
    plt.plot(new_wave[0])
    plt.grid()
    plt.subplot(232)
    plt.plot(new_wave[2])
    plt.grid()
    plt.subplot(233)
    plt.plot(new_wave[4])
    plt.grid()
    plt.subplot(234)
    plt.plot(new_wave[1])
    plt.grid()
    plt.subplot(235)
    plt.plot(new_wave[3])
    plt.grid()
    plt.subplot(236)
    plt.plot(new_wave[5])
    plt.grid()
    # plt.show()


def optical_data_splitting_test(txt_list, frequency):
    try:
        wheel_count = 0  # 车轮数量计数
        optical_all_data = []  # 一维的数据：所有传感器的数据；二维的数据：各个传感器所有的峰值
        if len(txt_list) != 0:
            x_coordinate = []
            all_each_optical_normalization = []
            for each_optical in txt_list:
                x_wheel_set = []
                max_wheel_set = []
                max_wheel_single_set = []

                each_optical_normalization = data_normalization(each_optical)
                all_each_optical_normalization.append(each_optical_normalization)

                y_after_filter = butter_lowpass_filter(each_optical_normalization, 500, 5000)

                max_single = []
                for i in range(0, len(y_after_filter) - 200, 200):
                    m = max(y_after_filter[i:i + 200])
                    if 0.4 < m:
                        max_single.append(m)

                dividing_line = min(max_single) - 0.05

                for i in range(len(each_optical)):
                    x_coordinate.append(round(i / frequency, 4))
                    if each_optical_normalization[i] > dividing_line:
                        wheel_set = [x_coordinate[i], each_optical[i]]
                        x_wheel_set.append(wheel_set)

                max_wheel_single_set.append(x_wheel_set[0])
                for i in range(1, len(x_wheel_set)):  # 两数据之间间隔>=time_gap则视为两段，<time_gap视为一段
                    if x_wheel_set[i][0] - x_wheel_set[i - 1][0] < time_gap:
                        max_wheel_single_set.append(x_wheel_set[i])
                    elif x_wheel_set[i][0] - x_wheel_set[i - 1][0] >= time_gap:
                        max_wheel_set.append(max_wheel_single_set)
                        max_wheel_single_set = [x_wheel_set[i]]
                if len(max_wheel_single_set) >= 2:
                    max_wheel_set.append(max_wheel_single_set)

                x_data = []
                if len(max_wheel_set) != 0:
                    for max_wheel in max_wheel_set:
                        if len(max_wheel) != 0:
                            get_no = round(len(max_wheel) / 2)
                            x_data.append(max_wheel[get_no][0])

                wheel_dict = {}
                for i in range(len(each_optical)):
                    wheel_dict.update({round(x_coordinate[i], 4): round(each_optical[i], 4)})
                last_wheel_value = list(wheel_dict)[-1]

                x_wheel_list = []
                unit_interval = round(1 / frequency, 4)

                for x in x_data:
                    if int(x / unit_interval) <= int(single_wheel_data_count / 2):
                        x_list = [round(unit_interval * a, 4) for a in range(single_wheel_data_count)]
                        x_wheel_list.append(x_list)
                    elif int(single_wheel_data_count / 2) <= int(x / unit_interval) <= int(
                            last_wheel_value / unit_interval) - int(single_wheel_data_count / 2):
                        x_list = [round(unit_interval * a, 4) for a in
                                  range(int(frequency * x) - int(single_wheel_data_count / 2),
                                        int(frequency * x) + int(single_wheel_data_count / 2))]
                        x_wheel_list.append(x_list)
                    else:
                        x_list = [round(unit_interval * a, 4) for a in
                                  range(int(frequency * last_wheel_value) - single_wheel_data_count,
                                        int(frequency * last_wheel_value))]
                        x_wheel_list.append(x_list)

                y_wheel = []
                y_single_optical = []
                for x_wheel in x_wheel_list:
                    for x_w in x_wheel:
                        y_w = wheel_dict[x_w]
                        y_wheel.append(y_w)
                    y_single_optical.append(y_wheel)
                    y_wheel = []

                if len(y_single_optical) == 32:
                    wheel_count += 1
                # optical_all_data的输出格式:三维列表[12个传感器×32个车轮×600个数据][12×32×600]的矩阵
                optical_all_data.append(y_single_optical)

        # 新增optical_all_data的size不一致的处理
        len_list = []
        for optical_data in optical_all_data:
            len_opt_data = len(optical_data)
            len_list.append(len_opt_data)

        zero_list = []
        len_count = c_Counter(len_list)
        len_ = max(len_count, key=len_count.get)
        if len(len_count) != 1:
            zero_ = [0.0] * single_wheel_data_count
            for i in range(len_):
                zero_list.append(zero_)

            len_new_list = []
            for i in range(len(optical_all_data)):
                len_opt_all_data_ = len(optical_all_data[i])
                if len_opt_all_data_ != len_:
                    optical_all_data[i] = zero_list
                len_opt_all_data_ = len(optical_all_data[i])
                len_new_list.append(len_opt_all_data_)
        return optical_all_data
    except Exception as e:
        info(e)


def optical_to_wheel(optical_all_data):
    try:
        op_left = []
        op_right = []
        op_arr = array(optical_all_data)
        for i in range(len(op_arr)):
            if i % 2 == 0:
                op_left.append(op_arr[i])
            else:
                op_right.append(op_arr[i])

        op_left_arr = array(op_left)
        op_right_arr = array(op_right)
        op_left_arr_tran = op_left_arr.transpose((1, 0, 2))
        op_right_arr_tran = op_right_arr.transpose((1, 0, 2))

        op_left_wheel_value = []
        op_right_wheel_value = []
        if op_left_arr_tran.shape == op_right_arr_tran.shape:
            for i in range(len(op_left_arr_tran)):
                op_max_left_set = []
                op_max_right_set = []
                for j in range(len(op_left_arr_tran[i])):
                    op_max_left = max(op_left_arr_tran[i][j])
                    op_max_right = max(op_right_arr_tran[i][j])
                    op_max_left_set.append(op_max_left)
                    op_max_right_set.append(op_max_right)
                op_max_left_result = round(sum(op_max_left_set) / len(op_max_left_set), 2)
                op_max_right_result = round(sum(op_max_right_set) / len(op_max_right_set), 2)
                op_left_wheel_value.append(op_max_left_result)
                op_right_wheel_value.append(op_max_right_result)
        op_list = [op_left_wheel_value, op_right_wheel_value]
        op_wheel_arr = array(op_list).transpose((1, 0))
        return op_wheel_arr
    except Exception as e:
        info(e)


def wheel_weight_algorithm(ww_wheel_value):
    try:
        # axle_wheel_value = ww_wheel_value.transpose((1, 0))
        # 经验值：742.585 对应 2.1t ==> 重量系数：2.1 / 742.585
        # sum_left_right = 742.585
        sum_left_right = 789.85
        wheelset_standard_weight = standard_left_weight + standard_right_weight + standard_axle_weight
        weight_coefficient = wheelset_standard_weight / sum_left_right
        left_wheel_coefficient = standard_left_weight / (standard_left_weight + standard_axle_weight / 2)
        right_wheel_coefficient = standard_right_weight / (standard_right_weight + standard_axle_weight / 2)
        axle_coefficient = standard_axle_weight / wheelset_standard_weight

        wheel_axle_weight = around(ww_wheel_value * weight_coefficient, 4)
        wheel_axle_weight_tran = wheel_axle_weight.transpose((1, 0))

        # 轮对的重量
        wheelset_weight = around(sum(wheel_axle_weight_tran), 4)

        # 轴的重量
        axle_weight = around(wheelset_weight * axle_coefficient, 3)

        # 车轮的重量
        left_wheel_weight = around(wheel_axle_weight_tran[0] * left_wheel_coefficient, 3)
        right_wheel_weight = around(wheel_axle_weight_tran[1] * right_wheel_coefficient, 3)
        wheel_weight = np_append(left_wheel_weight, right_wheel_weight).reshape((2, -1)).transpose((1, 0))

        return [wheel_weight, axle_weight, wheelset_weight]
    except Exception as e:
        info(e)


def weight_info_to_txt(save_path, file_name_, weight_info_):
    """
    # 重量信息写入日志
    :param save_path:
    :param file_name_:
    :param weight_info_:
    :return:
    """
    try:
        loc_time = localtime()
        time_format = '%Y-%m-%d %H:%M:%S'
        time_ = strftime(time_format, loc_time)
        weight_info_0 = str(weight_info_[0])
        weight_info_1 = str(weight_info_[1]).replace('\n', '')
        weight_info_2 = str(weight_info_[2]).replace('\n', '')
        with open(save_path + '\\Wheel Weight.txt', 'a+') as fw:
            fw.writelines('\n\n=====================================================================================\n')
            fw.writelines(file_name_)
            fw.writelines('\t')
            fw.writelines(time_)
            fw.writelines('\n\nWheel Weight:\n')
            fw.writelines(weight_info_0)
            fw.writelines('\n\nAxle Weight\n')
            fw.writelines(weight_info_1)
            fw.writelines('\n\nWheelset Weight\n')
            fw.writelines(weight_info_2)
            # fw.writelines('\n===========================================================================================\n')
    except Exception as e:
        info(e)


def test_main():
    try:
        file_path = getcwd()
        file_name = input('请输入需要分析重量的文件名称（不包含.txt）:')

        if file_name[-4:] == '.txt':
            p = file_path + '\\' + file_name
        else:
            p = file_path + '\\' + file_name + '.txt'

        data = read_txt(p)
        d_a = read_fiber_data_simple(data)
        ttw_wave_list = time_temp_wave(d_a)
        wave_all = wave_collection(ttw_wave_list)

        tw_txt, new_tw_wave = data_integration(wave_all)

        tw_optical_all_data = optical_data_splitting_test(new_tw_wave, o_f_frequency)
        tw_wheel_arr = optical_to_wheel(tw_optical_all_data)  # 整合传感器：12个传感器的数据整合成32个轴的数据
        weight_info = wheel_weight_algorithm(tw_wheel_arr)  # 车轮重量计算
        weight_info_to_txt(file_path, file_name, weight_info)  # 保存重量信息
        # plt.show()
        print('重量信息见 Wheel Weight.txt 文件！')
    except Exception as e:
        info('test_main:', e)


if __name__ == '__main__':
    test_main()

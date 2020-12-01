from collections import Counter as c_Counter
from logging import basicConfig, info
from os import getcwd
from time import strftime, localtime

# from matplotlib import pyplot as plt
from numpy import array

from Config import ConfigInfo

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

# 获取图像展示区间
pic_limits = conf.display_limits()

# 获取标准光纤波长
optical_wave_length = conf.optical_wavelength()

# 获取轮对经过光纤传感器时的波长
optical_wave_difference_ = conf.optical_difference()

# 获取光纤传感器在有无轮对经过时的差值
opt_wave_diff = conf.optical_wave_diff()

# time_gap还需要根据列车行驶速度确定（速度越快，时间间隔越短）
time_gap = 0.1
if o_f_frequency == 100:
    time_gap = 4
elif o_f_frequency == 2000:
    time_gap = float(conf.time_gap_value())


def read_txt(txt_name):
    """
    .txt文件读取
    :param txt_name: 完整txt文件路径，例：'E:\\Python\\Pyinstaller\\TP\\Original_DB\\01.txt'
    :return:
    """
    with open(txt_name, 'r') as f:
        txt_list = f.readlines()
    return txt_list


def read_fiber_data_simple(rfds_data):
    try:
        data_all = []
        if rfds_data[0][:4] == 'Time':
            for d in rfds_data:
                if d[:4] != 'Time':
                    fiber_data_list = []
                    d = d.replace('\t0', '').split('\t')
                    fiber_data = d[1:]
                    for i in fiber_data:
                        i = i.replace('\n', '')
                        i_float = float(i)  # 修改数据格式
                        fiber_data_list.append(i_float)
                    data_all.append([fiber_data_list])

        else:
            for d in rfds_data:
                fiber_data_list = []
                date_time_temp_ = []
                d = d.replace('\t', ' ').split('|')
                date_time_temp = d[0].split()
                for da in date_time_temp:
                    if len(da) > 2:
                        date_time_temp_.append(da)
                if len(date_time_temp_) == 8:
                    fiber_data = date_time_temp_[-6:]
                    for i in fiber_data:
                        fiber_data_list.append(float(i))

                data_all.append([fiber_data_list])
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

    wave_arr = array(wave_list)
    wave_arr_tran = wave_arr.transpose((1, 0))
    return wave_arr_tran


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


def data_integration(tw_wave):
    try:
        new_tw_wave_ = []
        wavelength_set = []
        wavelength_standard_set = []

        optical_order = [2, 0, 4, 1, 3, 5]
        for i_oo in optical_order:
            new_tw_wave_.append(tw_wave[i_oo])

        for single_wavelength in new_tw_wave_:
            wavelength_counter = c_Counter(single_wavelength)
            wavelength_counter_max = max(wavelength_counter, key=wavelength_counter.get)
            wavelength_mean = sum(single_wavelength) / len(single_wavelength)
            wavelength_set.append([wavelength_counter_max, wavelength_mean])
            wavelength_standard = (wavelength_counter_max + wavelength_mean) / 2
            wavelength_standard_set.append(wavelength_standard)

        info('6个传感器的标准波长：')
        info(wavelength_standard_set)
        return new_tw_wave_, wavelength_standard_set
    except Exception as e:
        info('optical_fiber:', e)


def tw_txt_integration_display(tw_txt):
    """
    校准到零坐标整合
    :param tw_txt:
    :return:
    """
    tw_integration_ = []
    if len(tw_txt) != 0:
        tw_txt_arr = array(tw_txt)
        for single_optical in tw_txt_arr:
            single_set_ = c_Counter(single_optical)
            single_max_ = max(single_set_, key=single_set_.get)
            tw_integration_.append(single_optical - single_max_)
    return tw_integration_


"""
def wave_display(new_wave):
    # plt.ion()
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
    plt.show()


def wave_display_limit(new_wave):
    # y_min = -0.028
    # y_max = 0.08
    y_max = float(pic_limits[0])
    y_min = float(pic_limits[1])
    plt.figure()
    plt.subplot(231)
    plt.plot(new_wave[0])
    plt.ylim((y_min, y_max))
    plt.grid()
    plt.subplot(232)
    plt.plot(new_wave[2])
    plt.ylim((y_min, y_max))
    plt.grid()
    plt.subplot(233)
    plt.plot(new_wave[4])
    plt.ylim((y_min, y_max))
    plt.grid()
    plt.subplot(234)
    plt.plot(new_wave[1])
    plt.ylim((y_min, y_max))
    plt.grid()
    plt.subplot(235)
    plt.plot(new_wave[3])
    plt.ylim((y_min, y_max))
    plt.grid()
    plt.subplot(236)
    plt.plot(new_wave[5])
    plt.ylim((y_min, y_max))
    plt.grid()
    plt.show()
"""


def wheelset_weight_algorithm(wavelength_standard_set):
    wave_difference_set = []
    if len(wavelength_standard_set) == len(optical_wave_length):
        for i in range(len(wavelength_standard_set)):
            wave_difference = wavelength_standard_set[i] - float(optical_wave_length[i])
            wave_difference_set.append(wave_difference)
    info('6个传感器的波长归一差值：')
    info(wave_difference_set)

    # 通过光纤波长的差值进行重量的计算
    wave_integration = []
    for i in range(len(wave_difference_set)):
        if abs(wave_difference_set[i]) < float(opt_wave_diff):
            wave_inte_opt = 0.0
            wave_integration.append(wave_inte_opt)
        else:
            wave_integration.append(wave_difference_set[i])
    wave_integration_arr = array(wave_integration).reshape((-1, 2))
    wave_integration_arr_tran = wave_integration_arr.transpose((1, 0))
    wave_sum = sum(wave_integration_arr_tran)
    info('三组传感器的系数：')
    info(wave_sum.tolist())

    sum_car_weight_data = standard_left_weight + standard_right_weight + standard_axle_weight
    weight_opt_set = []
    for i in range(len(wave_sum)):
        weight_opt = round(wave_sum[i] / float(optical_wave_difference_[i]) * sum_car_weight_data, 3)
        weight_opt_set.append(weight_opt)

    # print(weight_opt_set)

    return weight_opt_set


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
            fw.writelines('\n\n========================================\n')
            fw.writelines(file_name_)
            fw.writelines('\t')
            fw.writelines(time_)
            # fw.writelines('\n\nWheel Weight:\n')
            # fw.writelines(weight_info_0)
            # fw.writelines('\n\nAxle Weight\n')
            # fw.writelines(weight_info_1)
            # fw.writelines('\n\nWheelset Weight\n')
            # fw.writelines(weight_info_2)
            fw.writelines('\n\nWheelset Weight\n')
            fw.writelines('\n1st Optical fiber Sensor:')
            fw.writelines(weight_info_0)
            fw.writelines('\n2nd Optical fiber Sensor:')
            fw.writelines(weight_info_1)
            fw.writelines('\n3rd Optical fiber Sensor:')
            fw.writelines(weight_info_2)
            # fw.writelines('\n===========================================================================================\n')
    except Exception as e:
        info(e)


def test_pic_display():
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

        new_tw_wave, new_arr_wave_ = data_integration(wave_all)
        return new_tw_wave, new_arr_wave_
    except Exception as e:
        info(e)


def test_main():
    try:
        file_path = getcwd()
        file_name = input('请输入需要分析重量的文件名称（不包含.txt）:')

        loc_time = localtime()
        time_format = '%Y-%m-%d %H:%M:%S'
        time_ = strftime(time_format, loc_time)
        info(file_name)
        info(time_)

        if file_name[-4:] == '.txt':
            p = file_path + '\\' + file_name
        else:
            p = file_path + '\\' + file_name + '.txt'

        data = read_txt(p)
        d_a = read_fiber_data_simple(data)
        ttw_wave_arr = time_temp_wave(d_a)
        # wave_all = wave_collection(ttw_wave_list)

        tw_txt, wavelength_standard_set = data_integration(ttw_wave_arr)
        weight_info = wheelset_weight_algorithm(wavelength_standard_set)  # 车轮重量计算
        weight_info_to_txt(file_path, file_name, weight_info)  # 保存重量信息
        print('重量信息见 Wheel Weight.txt 文件！')
        # return new_arr_wave_
        return tw_txt
    except Exception as e:
        info('test_main:', e)


if __name__ == '__main__':
    info('\n=================================')
    new_arr_wave = test_main()
    # info('\n')
    # wave_display_limit(new_arr_wave)
    # ntw_wave, narr_wave = test_pic_display()
    # wave_display(narr_wave)

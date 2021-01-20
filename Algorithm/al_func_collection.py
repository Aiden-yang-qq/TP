# al_func_collection.py:Algorithm functional collection
from matplotlib import pyplot as plt
from numpy import ceil, arange, power, log2, array, around, linspace, pi, hstack
from numpy.fft import fft
from scipy.signal import butter, lfilter

from Function.func_collection import read_txt


def hex2decimal(hd_path):
    hex_list = []
    dec_list = []
    hex_txt = read_txt(hd_path)
    if len(hex_txt) == 1:
        hex_str = hex_txt[0]
        hex_count = len(hex_str) // 6
        hex_s = hex_str[:hex_count * 6]
        for c in range(hex_count):
            hex_single = hex_s[c * 6:(c + 1) * 6].split()
            hex_single = hex_single[1] + hex_single[0]
            dec_single = int(hex_single, 16)
            hex_list.append(hex_single)
            dec_list.append(dec_single)
    return hex_list, dec_list


def decimal2voltage(dec_list):
    voltage_list = []
    if len(dec_list) != 0:
        for dec in dec_list:
            vol = round(dec / 65535 * 5, 4)
            voltage_list.append(vol)
    return voltage_list


def fft_func(fs, data):
    """
    快速傅里叶变换
    :param fs: 采样频率
    :param data:
    :return:
    """
    len_ = len(data)
    n = int(power(2, ceil(log2(len_))))
    fre_ = arange(int(n / 2)) * fs / n
    fft_y_ = (fft(data, n)) / len_ * 2
    fft_y_ = fft_y_[range(int(n / 2))]
    return fre_, fft_y_


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
    # b, a = butter(N=order, Wn=normal_cutoff, btype='low', analog=False, output='ba', fs=fs)
    y_output = lfilter(b, a, data)
    return y_output


def non_circularity(x_wheel_data, all_wheel_data):
    """
    不圆度检测
    :param x_wheel_data:
    :param all_wheel_data:
    :return:
    """
    if len(all_wheel_data) != 0:
        radius_standard = 0.7
        coefficient = 0.3

        all_wheel_data_arr = array(all_wheel_data)
        # theta = linspace(0, 2 * pi, len(x_wheel_data))
        theta = linspace(0, 7.2 / 0.84, len(x_wheel_data))
        radius = around(radius_standard - coefficient - all_wheel_data_arr, 3)

        plt.figure()
        graph = plt.subplot(111, polar=True)
        graph.plot(theta, radius[0][0], linewidth=3)
        # graph.title('10')
        plt.show()

        # theta = linspace(0, 7.2 / 0.84, len(x_wheel_data))
        # radius = around(radius_standard - coefficient - all_wheel_data_arr, 3)
        # r9 = hstack((radius[0][1], radius[0][1][:int(len(radius[0][1]) / 2)]))
        # plt.figure()
        # graph = plt.subplot(111, polar=True)
        # graph.plot(theta, r9, linewidth=3)
        # # graph.title('10')
        # plt.show()


if __name__ == '__main__':
    # p = 'D:\\jaysk\\Desktop\\TP\\pressure.txt'
    p = 'D:\\jaysk\\Desktop\\TP\\串口数据.txt'
    h, d = hex2decimal(p)
    vo = decimal2voltage(d)

    # plt.figure()
    # plt.plot(vo)
    # plt.grid()
    # plt.show()

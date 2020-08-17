# picture_generation.py 图像生成
from os import path, listdir

from matplotlib import pyplot as plt
from Config import ConfigInfo
from Algorithm.data_splitting_integration import optical_data_splitting, optical_data_to_wheel
from Function.func_collection import read_txt

conf = ConfigInfo()
o_f_frequency = conf.get_optical_fiber_frequency()  # 频率取不到，因为picture.py的路径不在main.py的路径上


def txt_to_list(ttp_path):
    txt_set = []
    txt_name = listdir(ttp_path)
    for txt_signal_name in txt_name:
        xy_list = []
        txt_path = ttp_path + '\\' + txt_signal_name
        if path.exists(txt_path):
            x_list = []
            y_list = []
            txt = read_txt(txt_path)
            for t in txt:
                xy_t = t.strip().split()
                x_t = float(xy_t[0])
                y_t = float(xy_t[1])
                x_list.append(x_t)
                y_list.append(y_t)
            xy_list.append(x_list)
            xy_list.append(y_list)
        txt_set.append(xy_list)
    return txt_set


def pic_generation(txt_set):
    # 左1 右1
    # 左2 右2
    # 左3 右3
    plt.figure()
    plt.subplot(321)
    plt.plot(txt_set[2][0], txt_set[2][1])
    plt.grid()
    plt.subplot(322)
    plt.plot(txt_set[0][0], txt_set[0][1])
    plt.grid()
    plt.subplot(323)
    plt.plot(txt_set[4][0], txt_set[4][1])
    plt.grid()
    plt.subplot(324)
    plt.plot(txt_set[1][0], txt_set[1][1])
    plt.grid()
    plt.subplot(325)
    plt.plot(txt_set[3][0], txt_set[3][1])
    plt.grid()
    plt.subplot(326)
    plt.plot(txt_set[5][0], txt_set[5][1])
    plt.grid()
    plt.show()


# def wheel_

if __name__ == '__main__':
    # p = 'E:\\Python\\Pyinstaller\\TP\\DB\\Data_lib\\2020\\06\\11\\1130#2020-06-11 08_53_30'
    # p = 'E:\\Python\\Pyinstaller\\TP\\DB\\Data_lib\\2020\\06\\10\\1133#2020-06-10 18_55_15'
    p = 'E:\\Python\\Pyinstaller\\TP\\DB\\Data_lib\\2020\\06\\11\\1130#2020-06-11 08_53_30'
    txt_list = txt_to_list(p)
    # pic_generation(txt_list)
    # wdi = wheel_data_integration(txt_list)

    # w = optical_data_splitting(txt_list, o_f_frequency)
    # wd = optical_data_to_wheel(w, o_f_frequency)

    # plt.figure()
    # plt.plot(wdi[0], wdi[1], 'o')
    # plt.plot(wdi[0], wdi[1])
    # plt.grid()
    # plt.show()
    plt.figure()
    plt.plot(txt_list[0][0], txt_list[0][1])
    plt.grid()
    plt.show()

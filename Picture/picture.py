# picture_generation.py 图像生成
from os import path, listdir
from Function.func_collection import read_txt
from matplotlib import pyplot as plt
from Algorithm.data_splitting_integration import wheel_data_integration, wheel_data_splitting


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
    p = 'E:\\Python\\Pyinstaller\\TP\\DB\\Data_lib\\2020\\06\\11\\1130#2020-06-11 08_53_30'
    txt_list = txt_to_list(p)
    # pic_generation(txt_list)
    # wdi = wheel_data_integration(txt_list)

    w = wheel_data_splitting(txt_list)

    # plt.figure()
    # plt.plot(wdi[0], wdi[1], 'o')
    # plt.plot(wdi[0], wdi[1])
    # plt.grid()
    # plt.show()

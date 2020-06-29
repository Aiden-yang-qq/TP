# al_func_collection.py:Algorithm functional collection
from func_collection import read_txt
from matplotlib import pyplot as plt


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


if __name__ == '__main__':
    # p = 'D:\\jaysk\\Desktop\\TP\\pressure.txt'
    p = 'D:\\jaysk\\Desktop\\TP\\串口数据.txt'
    h, d = hex2decimal(p)
    vo = decimal2voltage(d)

    plt.figure()
    plt.plot(vo)
    plt.grid()
    plt.show()

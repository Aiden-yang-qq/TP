from collections import Counter as Col_Counter
from os import listdir, getcwd
from os.path import getsize

from matplotlib import pyplot as plt
from numpy import array


def data_read():
    opt_txt_set = []
    all_txt_file_int = []
    all_txt_file_str = []
    folder_path = getcwd()
    txt_file = listdir(folder_path)

    if len(txt_file) != 0:
        for opt_txt in txt_file:
            if opt_txt[-3:] == 'txt' and len(opt_txt) <= 6:
                opt_txt_set.append(opt_txt)

        # opt_txt_set.sort(key=len)   # 从小到大调整顺序

        start_ = 1
        if len(opt_txt_set) != 0:
            file_dir = folder_path + '\\' + opt_txt_set[0]
            txt_size = getsize(file_dir)
            if txt_size >= 300000:
                start_ = int(input('请输入起始帧数：'))

        for single_txt in opt_txt_set:
            if single_txt[-3:] == 'txt':
                with open(folder_path + '\\' + single_txt, 'r') as f:
                    txt = f.readlines()
                    txt_data_int = []
                    txt_data_str = [txt[0]]
                    if len(txt) > 70000:
                        len_start = start_
                        len_end = len_start + 30000
                    else:
                        len_start = 1
                        len_end = len(txt)

                    for i in range(len_start, len_end):
                        txt_ = txt[i]
                        txt_int = int(txt_.strip())

                        txt_data_int.append(txt_int)
                        txt_data_str.append(txt_)

                    all_txt_file_int.append(txt_data_int)
                    all_txt_file_str.append(txt_data_str)

        if start_ != 1:
            write_to_new_txt(all_txt_file_str)
    return all_txt_file_int, all_txt_file_str


def txt_data_normalization(all_txt_file_int):
    max_count = []
    all_txt_file_arr = []
    if len(all_txt_file_int) != 0:
        for single_txt_data in all_txt_file_int:
            txt_count = Col_Counter(single_txt_data)
            txt_max = max(txt_count, key=txt_count.get)
            txt_arr = array(single_txt_data) - txt_max
            all_txt_file_arr.append(txt_arr)
            max_count.append(txt_max)
        return all_txt_file_arr, max_count


def write_to_new_txt(all_txt_file_str):
    folder_path = getcwd()
    if len(all_txt_file_str) != 0:
        for i in range(len(all_txt_file_str)):
            writelines_txt(folder_path + '\\%s.txt' % (i + 1), all_txt_file_str[i])


def writelines_txt(wt_path, write_file):
    with open(wt_path, 'w') as fw:
        fw.writelines(write_file)


def data_display(all_txt_file, max_count):
    y_min = -100
    y_max = 300
    plt.figure()
    plt.subplot(2, 6, 1)
    plt.plot(all_txt_file[0])
    plt.ylim((y_min, y_max))
    plt.title(max_count[0])
    plt.grid()
    plt.subplot(2, 6, 2)
    plt.plot(all_txt_file[4])
    plt.ylim((y_min, y_max))
    plt.title(max_count[4])
    plt.grid()
    plt.subplot(2, 6, 3)
    plt.plot(all_txt_file[6])
    plt.ylim((y_min, y_max))
    plt.title(max_count[6])
    plt.grid()
    plt.subplot(2, 6, 4)
    plt.plot(all_txt_file[7])
    plt.ylim((y_min, y_max))
    plt.title(max_count[7])
    plt.grid()
    plt.subplot(2, 6, 5)
    plt.plot(all_txt_file[8])
    plt.ylim((y_min, y_max))
    plt.title(max_count[8])
    plt.grid()
    plt.subplot(2, 6, 6)
    plt.plot(all_txt_file[5])
    plt.ylim((y_min, y_max))
    plt.title(max_count[5])
    plt.grid()
    plt.subplot(2, 6, 7)
    plt.plot(all_txt_file[3])
    plt.ylim((y_min, y_max))
    plt.title(max_count[3])
    plt.grid()
    plt.subplot(2, 6, 8)
    plt.plot(all_txt_file[2])
    plt.ylim((y_min, y_max))
    plt.title(max_count[2])
    plt.grid()
    plt.subplot(2, 6, 9)
    plt.plot(all_txt_file[1])
    plt.ylim((y_min, y_max))
    plt.title(max_count[1])
    plt.grid()
    plt.subplot(2, 6, 10)
    plt.plot(all_txt_file[10])
    plt.ylim((y_min, y_max))
    plt.title(max_count[10])
    plt.grid()
    plt.subplot(2, 6, 11)
    plt.plot(all_txt_file[9])
    plt.ylim((y_min, y_max))
    plt.title(max_count[9])
    plt.grid()
    plt.subplot(2, 6, 12)
    plt.plot(all_txt_file[11])
    plt.ylim((y_min, y_max))
    plt.title(max_count[11])
    plt.grid()
    plt.show()


def data_display_all(all_txt_file):
    plt.figure()
    for i in range(len(all_txt_file)):
        plt.subplot(2, 6, i + 1)
        plt.plot(all_txt_file[i])
        plt.grid()
    plt.show()


def odtp_main():
    all_txt_file_int, all_txt_file_str = data_read()
    all_txt_file_arr, max_count = txt_data_normalization(all_txt_file_int)
    # write_to_new_txt(all_txt_file_str)
    data_display(all_txt_file_arr, max_count)
    # print('Hello')


if __name__ == '__main__':
    odtp_main()

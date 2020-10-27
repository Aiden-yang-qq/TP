from collections import Counter as Col_Counter
from os import listdir, getcwd

from matplotlib import pyplot as plt
from numpy import array

# from Function.func_collection import writelines_txt


def data_read():
    all_txt_file_int = []
    all_txt_file_str = []
    folder_path = getcwd()
    txt_file = listdir(folder_path)

    if len(txt_file) != 0:
        for single_txt in txt_file:
            if single_txt[-3:] == 'txt':
                with open(folder_path + '\\' + single_txt, 'r') as f:
                    txt = f.readlines()
                    txt_data_int = []
                    txt_data_str = [txt[0]]
                    if len(txt) > 70000:
                        len_start = 65000
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
    return all_txt_file_int, all_txt_file_str


def txt_data_normalization(all_txt_file_int):
    all_txt_file_arr = []
    if len(all_txt_file_int) != 0:
        for single_txt_data in all_txt_file_int:
            txt_count = Col_Counter(single_txt_data)
            txt_max = max(txt_count, key=txt_count.get)
            txt_arr = array(single_txt_data) - txt_max
            all_txt_file_arr.append(txt_arr)
        return all_txt_file_arr


# def write_to_new_txt(all_txt_file_str):
#     folder_path = getcwd()
#     if len(all_txt_file_str) != 0:
#         for i in range(len(all_txt_file_str)):
#             writelines_txt(folder_path + '\\%s.txt' % (i + 1), all_txt_file_str[i])


def data_display(all_txt_file):
    # plt.figure()
    # for i in range(len(all_txt_file)):
    #     plt.subplot(2, 6, i+1)
    #     plt.plot(all_txt_file[i])
    #     plt.grid()
    # plt.show()
    plt.figure()
    plt.subplot(2, 6, 1)
    plt.plot(all_txt_file[0])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 2)
    plt.plot(all_txt_file[4])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 3)
    plt.plot(all_txt_file[6])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 4)
    plt.plot(all_txt_file[7])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 5)
    plt.plot(all_txt_file[8])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 6)
    plt.plot(all_txt_file[5])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 7)
    plt.plot(all_txt_file[3])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 8)
    plt.plot(all_txt_file[2])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 9)
    plt.plot(all_txt_file[1])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 10)
    plt.plot(all_txt_file[10])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 11)
    plt.plot(all_txt_file[9])
    plt.ylim((-100, 300))
    plt.grid()
    plt.subplot(2, 6, 12)
    plt.plot(all_txt_file[11])
    plt.ylim((-100, 300))
    plt.grid()
    plt.show()


def odtp_main():
    all_txt_file_int, all_txt_file_str = data_read()
    all_txt_file_arr = txt_data_normalization(all_txt_file_int)
    # write_to_new_txt(all_txt_file_str)
    data_display(all_txt_file_arr)
    # print('Hello')


if __name__ == '__main__':
    odtp_main()

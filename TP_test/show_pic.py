from collections import Counter as Coll_Counter
from os import getcwd, path

from matplotlib import pyplot as plt
from numpy import array

# with open('D:\\jaysk\\Desktop\\TP\\LSSJ\\20200806235951\\1.txt', 'r') as f:
folder_path = getcwd()
file_name = input('文件名（1-12）：')
file_path = folder_path + '\\' + file_name + '.txt'

if path.exists(file_path):
    with open(file_path, 'r') as f:
        txt = f.readlines()

    txt_l = []
    for t in txt[1:]:
        tt = int(t.strip())
        txt_l.append(tt)

    txt_count = Coll_Counter(txt_l)
    txt_max = max(txt_count, key=txt_count.get)

    new_txt = array(txt_l) - txt_max

    plt.figure()
    plt.plot(new_txt)
    plt.grid()
    plt.show()

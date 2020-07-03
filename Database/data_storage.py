# 将数据存成txt文档，文件名称以车号命名
from logging import info
from Function.func_collection import write_txt
from Algorithm.data_splitting_integration import data_normalization


def data_to_txt(path, each_wheel_data):
    try:
        if len(each_wheel_data) != 0:
            if len(each_wheel_data[0]) == len(each_wheel_data[1]):
                ewd_all = []
                each_wheel_nor_data = data_normalization(each_wheel_data[1])
                for i in range(len(each_wheel_data[0])):
                    ewd = str(round(each_wheel_data[0][i], 3)) + ' ' + str(each_wheel_nor_data[i])  # 保留小数位数越多越精确
                    ewd_all.append(ewd)

                ea = "\n".join(ewd_all)
                write_txt(path, ea)
    except Exception as e:
        info(e)

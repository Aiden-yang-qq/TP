# 将数据存成txt文档，文件名称以车号命名


def data_to_txt(path, each_wheel_data):
    if len(each_wheel_data) != 0:
        if len(each_wheel_data[0]) == len(each_wheel_data[1]):
            ewd_all = []
            for i in range(len(each_wheel_data[0])):
                ewd = str(round(each_wheel_data[0][i], 3)) + ' ' + str(each_wheel_data[1][i])  # 保留小数位数越多越精确
                ewd_all.append(ewd)

            ea = "\n".join(ewd_all)
            with open(path, 'w') as f:
                f.write(ea)

# 将数据存成txt文档，文件名称以车号命名


def data_to_txt(path, each_wheel_data):
    if len(each_wheel_data) != 0:
        if len(each_wheel_data[0]) == len(each_wheel_data[1]):
            ewd_all = []
            for i in range(len(each_wheel_data[0])):
                ewd = str(round(each_wheel_data[0][i], 3)) + ' ' + str(each_wheel_data[1][i])  # 保留小数位数越多越精确
                ewd_all.append(ewd)

            ea = "\n".join(ewd_all)
            # print('Done')
            with open(path, 'w') as f:
                f.write(ea)

# if __name__ == '__main__':
#     path = 'E:\\Python\\Pyinstaller\\TP\\Database\\Data_pool'
#
#     data_to_txt()

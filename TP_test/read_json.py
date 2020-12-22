from json import load
from os import getcwd, path

from matplotlib import pyplot as plt

# from numpy import arange

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def read_json_main():
    read_json_main_path = getcwd()
    json_file_name_1 = input('请输入第一个json文件的名称：')
    json_file_name_2 = input('请输入第二个json文件的名称：')

    # json_file_name_1 = '1124#2020-11-12 23_59_18'
    # json_file_name_1 = '1124#2020-11-30 23_21_11'
    # json_file_name_2 = '1124#2020-12-14 00_12_26'
    # json_file_name_2 = '1124#2020-12-09 23_04_11'
    # json_file_name_2 = '1124#2020-12-17 00_20_32'
    # json_file_name_1 = '1120#2020-11-06 00_17_17'
    # json_file_name_2 = '1120#2020-12-02 00_05_13'

    json_file_dir_1 = read_json_main_path + '\\' + json_file_name_1 + '.json'
    json_file_dir_2 = read_json_main_path + '\\' + json_file_name_2 + '.json'

    json_data_1 = None
    json_data_2 = None

    if path.exists(json_file_dir_1):
        json_data_1 = read_json_file(json_file_dir_1)
    else:
        print('未找到%s文件' % json_file_name_1)
    if path.exists(json_file_dir_2):
        json_data_2 = read_json_file(json_file_dir_2)
    else:
        print('未找到%s文件' % json_file_name_2)

    # 对两个json文件进行读取并展示
    if (json_data_1 is not None) and (json_data_2 is not None):
        if json_data_1['carNo'] == json_data_2['carNo']:
            carriage_no = input('请输入完整车厢号（11xx1-11xx8）：')
            axle_no = input('请输入轴号（1-4）：')

            json_axle_data_1 = []
            json_axle_data_2 = []
            if (carriage_no[:4] == json_data_1['carNo']) and (1 <= int(carriage_no[4:]) <= 8):
                if 1 <= int(axle_no) <= 4:
                    json_axle_data_1 = get_json_axle_data(json_data_1, carriage_no, axle_no)
                    json_axle_data_2 = get_json_axle_data(json_data_2, carriage_no, axle_no)
                else:
                    print('轴号输入有误！')
            else:
                print('车厢号输入有误！')

            axle_data_display(json_axle_data_1, json_axle_data_2, carriage_no, axle_no, json_file_name_1,
                              json_file_name_2)
        else:
            print('输入的两个文件车号不相同，不具有可比性！')


def read_json_file(rjf_path):
    if path.exists(rjf_path):
        with open(rjf_path, 'r', encoding='utf-8-sig') as f:
            json_content = load(f)
    return json_content


def get_json_axle_data(json_data, carriage_no, axle_no):
    # each_wheel_data = []
    carriage_data = json_data['vi']
    each_wheel_data = json_data_collection(carriage_data, carriage_no, axle_no)
    return each_wheel_data


def json_data_collection(carriage_data, carriage_no, axle_no):
    each_wheel_data = []
    if len(carriage_data) == 8:
        for each_carriage in carriage_data:
            if each_carriage['vehicleNo'] == carriage_no:
                each_carriage_data = each_carriage['bc']
                if len(each_carriage_data) == 8:
                    for each_wheel in each_carriage_data:
                        each_wheel_data_left = []
                        each_wheel_data_right = []
                        if each_wheel['vehicleAxleSeq'] == axle_no:
                            if each_wheel['vehicleSide'] == 'L':
                                each_wheel_data_left = [each_wheel['xAxis'], each_wheel['yAxis']]
                            else:
                                each_wheel_data_right = [each_wheel['xAxis'], each_wheel['yAxis']]

                            if len(each_wheel_data_left) != 0:
                                each_wheel_data.append(each_wheel_data_left)
                            if len(each_wheel_data_right) != 0:
                                each_wheel_data.append(each_wheel_data_right)
    return each_wheel_data


def axle_data_display(json_axle_data_1, json_axle_data_2, carriage_no, axle_no, json_file_name_1, json_file_name_2):
    if (len(json_axle_data_1) == len(json_axle_data_2)) and (len(json_axle_data_1) != 0):
        ymin = -0.15
        ymax = 0.4

        plt.figure()
        for i in range(len(json_axle_data_1)):
            plt.subplot(1, 2, i + 1)
            if i == 0:
                plt.plot(json_axle_data_1[i][0], json_axle_data_1[i][1], label='%s 左侧车轮数据' % json_file_name_1)
                plt.plot(json_axle_data_2[i][0], json_axle_data_2[i][1], label='%s 左侧车轮数据' % json_file_name_2)
            else:
                plt.plot(json_axle_data_1[i][0], json_axle_data_1[i][1], label='%s 右侧车轮数据' % json_file_name_1)
                plt.plot(json_axle_data_2[i][0], json_axle_data_2[i][1], label='%s 右侧车轮数据' % json_file_name_2)
            plt.xlim(0, 0.84)
            plt.ylim(ymin, ymax)
            # plt.yticks(arange(-0.15, 0.41, 0.05))
            plt.ylabel('光纤波长长度/nm')
            plt.legend()
            plt.grid()
        plt.suptitle('两趟列车，%s车厢%s号轴左右侧车轮的数据对比' % (carriage_no, axle_no))
        plt.show()
    elif len(json_axle_data_1) != len(json_axle_data_2):
        if len(json_axle_data_1) == 0 and len(json_axle_data_2) != 0:
            print('%s车厢第一个文件数据未采集到！' % carriage_no)
        elif len(json_axle_data_1) != 0 and len(json_axle_data_2) == 0:
            print('%s车厢第二个文件数据未采集到！' % carriage_no)
    else:
        print('两个文件数据均未采集到，无法展示！')


if __name__ == '__main__':
    read_json_main()
    # print('Done')

from json import load, loads
from os import getcwd, path
from sys import exit
from time import sleep

from matplotlib import pyplot as plt
from numpy import arange

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def read_json_main():
    read_json_main_path = getcwd()

    # 判断第一个json文件是否存在
    json_data_1 = None
    json_file_name_1 = input('请输入第一个json文件的名称：')
    json_file_dir_1 = read_json_main_path + '\\' + json_file_name_1 + '.json'
    if path.exists(json_file_dir_1):
        json_data_1 = read_json_file(json_file_dir_1)
    else:
        print('未找到%s文件' % json_file_name_1)
        sleep(1)
        exit()

    # 判断第二个json文件是否存在
    json_data_2 = None
    json_file_name_2 = input('请输入第二个json文件的名称：')
    json_file_dir_2 = read_json_main_path + '\\' + json_file_name_2 + '.json'
    if path.exists(json_file_dir_2):
        json_data_2 = read_json_file(json_file_dir_2)
    else:
        print('未找到%s文件' % json_file_name_2)
        sleep(1)
        exit()

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
                    sleep(1)
            else:
                print('车厢号输入有误！')
                sleep(1)

            axle_data_display(json_axle_data_1, json_axle_data_2, carriage_no, axle_no, json_file_name_1,
                              json_file_name_2)
        else:
            print('输入的两个文件车号不相同，不具有可比性！')
    else:
        print('请重启本程序并输入正确的json文件名称！')
        sleep(1)
        exit()


def read_json_file(rjf_path):
    if path.exists(rjf_path):
        with open(rjf_path, 'r', encoding='utf-8-sig') as f:
            json_content = load(f)
    return json_content


def get_json_axle_data(json_data, carriage_no, axle_no):
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
    # if (len(json_axle_data_1) == len(json_axle_data_2)) and (len(json_axle_data_1) != 0):
    if len(json_axle_data_1) == len(json_axle_data_2) != 0:
        ymin = -0.14
        ymax = 0.4

        plt.figure()
        for i in range(len(json_axle_data_1)):
            plt.subplot(1, 2, i + 1)
            ax = plt.gca()
            ax.axhline(-0.1, c='silver')
            ax.axhline(0.0, c='silver')
            ax.axhline(0.1, c='silver')
            ax.axhline(0.2, c='silver')
            ax.axhline(0.3, c='silver')
            # plt.style.use('ggplot')
            if i == 0:
                plt.plot(json_axle_data_1[i][0], json_axle_data_1[i][1], label='%s 左侧车轮数据' % json_file_name_1)
                plt.plot(json_axle_data_2[i][0], json_axle_data_2[i][1], label='%s 左侧车轮数据' % json_file_name_2)
            else:
                plt.plot(json_axle_data_1[i][0], json_axle_data_1[i][1], label='%s 右侧车轮数据' % json_file_name_1)
                plt.plot(json_axle_data_2[i][0], json_axle_data_2[i][1], label='%s 右侧车轮数据' % json_file_name_2)
            plt.xlim(0, 0.84)
            plt.ylim(ymin, ymax)
            plt.yticks(arange(-0.14, 0.41, 0.02))
            plt.ylabel('光纤波长幅值/nm')
            plt.legend()
            plt.grid(linestyle='-.', alpha=0.75)
        plt.suptitle('%s车厢%s号轴在不同时间点，左右侧车轮的数据对比' % (carriage_no, axle_no))
        print('%s车厢%s号轴在不同时间点，左右侧车轮的数据对比' % (carriage_no, axle_no))
        plt.show()
    elif len(json_axle_data_1) != len(json_axle_data_2):
        if len(json_axle_data_1) == 0 and len(json_axle_data_2) != 0:
            print('%s车厢第一个文件数据未采集到！' % carriage_no)
        elif len(json_axle_data_1) != 0 and len(json_axle_data_2) == 0:
            print('%s车厢第二个文件数据未采集到！' % carriage_no)
    else:
        print('数据有误，无法展示！')
        exit()


def read_result_json():
    result_path_ = getcwd()
    result_json_name = result_path_ + '\\result(2)_.json'
    json_file = read_json_file(result_json_name)
    car_sort_dict = json_file_handle(json_file)
    parameter_algorithm(car_sort_dict)
    pass


def json_file_handle(json_file):
    if len(json_file) != 0:
        car_dict = {}
        for car_no in json_file.keys():
            if car_no[:2] == '11':
                value_set = []
                for value in json_file[car_no]:
                    if value.upper() != 'NAN':
                        value_set.append(int(value))
                car_dict.update({int(car_no): value_set})

        car_sort = sorted(car_dict.items(), key=lambda x: x[0], reverse=False)
        car_sort_dict = dict(car_sort)
        return car_sort_dict


def parameter_algorithm(car_sort_dict):
    ie_data = {}
    if len(car_sort_dict) != 0:
        for car_key in car_sort_dict.keys():
            impact_equivalent = car_sort_dict[car_key]
            ie_average = round(sum(impact_equivalent) / len(impact_equivalent), 2)
            ie_variance = round(sum([(x - ie_average) ** 2 for x in impact_equivalent]) / len(impact_equivalent), 2)
            ie_data.update({car_key: [ie_average, ie_variance]})

        car_no = []
        average_ = []
        variance_ = []
        for data_ in ie_data.keys():
            car_no.append(data_)
            average_.append(ie_data[data_][0])
            variance_.append(ie_data[data_][1])
    return ie_data


if __name__ == '__main__':
    # read_json_main()
    # print('Done')
    read_result_json()

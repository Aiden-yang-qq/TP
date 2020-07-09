# 将数据存成txt文档，文件名称以车号命名
from json import load, dump, dumps
from math import ceil
from uuid import uuid1
from logging import info
from Function.func_collection import write_txt
from Algorithm.data_splitting_integration import data_normalization


def data_to_txt(path, each_wheel_data):
    try:
        if len(each_wheel_data) != 0:
            each_normalization_wheel = []
            if len(each_wheel_data[0]) == len(each_wheel_data[1]):
                ewd_all = []
                each_wheel_nor_data = data_normalization(each_wheel_data[1])
                each_normalization_wheel.append(each_wheel_data[0])
                each_normalization_wheel.append(each_wheel_nor_data)
                for i in range(len(each_wheel_data[0])):
                    ewd = str(round(each_wheel_data[0][i], 3)) + ' ' + str(each_wheel_nor_data[i])  # 保留小数位数越多越精确
                    ewd_all.append(ewd)

                ea = "\n".join(ewd_all)
                write_txt(path, ea)
                return each_normalization_wheel
    except Exception as e:
        info(e)


def read_json():
    json_path = 'E:\\Python\\Pyinstaller\\TP'
    json_name = 'TP_json.json'
    json_f = json_path + '\\' + json_name
    with open(json_f, 'r', encoding='utf-8-sig') as f:
        data = load(f)
    return data


def write_json(json_name, json_data):
    json_path = 'D:\\json_file_TP'
    json_dir = json_path + '\\' + json_name + '.json'
    with open(json_dir, 'w') as f:
        dump(json_data, f)


def car_json(car_no, file_name='', sddt='', wheel_no=64, all_carriage_json=[]):
    car = {
        "dataStatus": "",  # 0正常，1少车 2少轴
        "carNo": "%s" % car_no,  # 车号
        "sd": "",  # 速度
        "sddt": "%s" % sddt,  # 数据生成检测时间
        "edsi": "",  # site identifier站点标识
        "fileName": "%s" % file_name,  # 文件名
        "dtOfPass": "",  # 检测时间,MM/DD/YYYY HH:MM:SS
        "numOfAxle": "%s" % int(wheel_no / 2),  # 总轴数（根据车厢换算：轴数=车厢数×4）
        "numOfCarr": "%s" % int(wheel_no / 8),  # 总车厢数
        "trainSpeed": "",  # ""%s" % train_speed,  # 平均速度（列车的速度根据8节车厢的平均速度来给定）
        "trainDirection": "",  # 列车方向  N F
        "sides": "",  # 处理哪一端取值B,N,F,blank。
        "verOfsoftware": "",  # 软件版本号
        "vi": all_carriage_json  # TODO 根据实际车厢数修改txt文件
    }
    return car


def carriage_json(axle_count, all_wheel_json):
    carriage = {
        "vid": "%s" % uuid1(),  # 32位uuid
        "vehicleNo": "",  # ""%s" % vehicle_no_bc,  # 车厢号
        "carOri": "",  # 车厢方向
        "axleCount": "%d" % axle_count,  # 轴数
        "vehicleType": "",  # 车厢类型，5=机车，19=挂车，其他值=其他
        "vehicleSeq": "",  # 辆序
        "bc": all_wheel_json  # TODO 根据实际轮数修改txt文件
    }
    return carriage


def wheel_json(rail, axle_seq, invalid_flag=0, x_axis=[], y_axis=[]):
    # x_axis = []
    # y_axis = []
    car_wheel = {
        "bcd": "%s" % uuid1(),
        "rail": "%s" % rail,  # 取值NS,FS
        "vehicleAxleSeq": "%s" % axle_seq,  # 在该车厢的轴序
        "axleSeq": "",  # 在整个编组中的轴序，取值1-9999（指8节车厢中的哪一节车厢）
        "vehicleSeq": "",  # 辆序，取值1-999，对应vi里的seqs
        "vehicleNoBC": "",  # ""%s" % vehicle_no_bc,  # 车号，对应vi里的vehicleNo
        "vehicleSide": "",  # 左右侧，取值L,R,U
        "axleSpeed": "",  # "%d mph" % speed,  # 通过速度mph（车轮的速度根据车厢来给定）
        "invalidFlag": "%s" % invalid_flag,  # 数据是否有效，0有效，其他无效
        "invalidDesc": "",  # 无效描述
        "data1": "",  # 值,-999.999-999.999
        "data2": "",  # 值,-999.999-999.999
        "data3": "",  # 值,-999.999-999.999
        "data4": "",  # 值,-999.999-999.999
        "bearingDefect": "",  # 是否有缺陷，0无，1有
        "defectType1": "",  # 是否有平轮缺陷
        "defectType2": "",  # 是否有不圆度缺陷
        "defectType3": "",  # 是否有多边形缺陷
        "defectType4": "",  # 是否有车辆偏载缺陷
        "defectRank": "",  # 级别，1-3
        "alarmSend": "",  # 是否发送报警给用户，1是，0否
        "xAxis": x_axis,
        "yAxis": y_axis
    }
    return car_wheel


def car_json_integration(json_name, all_wheel_data):
    all_wheel_no = len(all_wheel_data)
    car_no = json_name[:4]

    # 各个车轮json数据
    all_wheel_json = []
    all_wheel_set_json = []
    for i in range(all_wheel_no):
        if i % 2 == 0:
            rail = 'NS'
        else:
            rail = 'FS'

        axle_seq = ceil((i + 1) / 2)
        wheel_single_json = wheel_json(rail=rail, axle_seq=axle_seq, x_axis=all_wheel_data[i][0],
                                       y_axis=all_wheel_data[i][1])
        all_wheel_json.append(wheel_single_json)
        if len(all_wheel_json) % 8 == 0:
            all_wheel_set_json.append(all_wheel_json)

    # 各个车厢json数据
    all_carriage_json = []
    for i in range(len(all_wheel_set_json)):
        axle_count = int(len(all_wheel_set_json[i]) / 2)
        carriage_single_json = carriage_json(axle_count, all_wheel_json=all_wheel_set_json[i])
        all_carriage_json.append(carriage_single_json)

    # 整车json数据
    all_car_json = car_json(car_no=car_no, wheel_no=all_wheel_no, all_carriage_json=all_carriage_json)
    return all_car_json


if __name__ == '__main__':
    # json_path = 'E:\\Python\\Pyinstaller\\TP'
    # json_name = 'TP_json.json'
    # json_f = json_path + '\\' + json_name
    # d = data_to_json(json_f)
    # json_fi = read_json()

    print('Json:')

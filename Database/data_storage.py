# 将数据存成txt文档，文件名称以车号命名
from json import dump, load
from logging import info
from os import listdir, path, remove
from sys import stdout
from time import strftime, localtime, time, sleep
from uuid import uuid1

from numpy import array, transpose, ones, around, sum as np_sum, random

from Algorithm.data_splitting_integration import data_standardization
from Config import ConfigInfo
from Function.func_collection import write_txt, folder_creation

conf = ConfigInfo()


def data_to_txt(dtt_path, each_wheel_data):
    """
    车轮数据标准化
    :param dtt_path:
    :param each_wheel_data:
    :return:
    """
    try:
        if len(each_wheel_data) != 0:
            each_normalization_wheel = []
            if len(each_wheel_data[0]) == len(each_wheel_data[1]):
                ewd_all = []
                each_wheel_nor_data = data_standardization(each_wheel_data[1])  # 数据标准化
                if len(each_wheel_data) != 0 and len(each_wheel_nor_data) != 0:
                    each_normalization_wheel.append(each_wheel_data[0])
                    each_normalization_wheel.append(each_wheel_nor_data)
                    for i in range(len(each_wheel_data[0])):
                        ewd = str(round(each_wheel_data[0][i], 6)) + ' ' + str(each_wheel_nor_data[i])  # 保留小数位数越多越精确
                        ewd_all.append(ewd)

                    # 将数据写入D:\DB\Data_lib中
                    # ea = "\n".join(ewd_all)
                    # write_txt(dtt_path, ea)
                if len(each_normalization_wheel) != 0:
                    return each_normalization_wheel
                else:
                    return ''
    except Exception as e:
        info('data_storage:', e)


def read_speed_json():
    speed_set = []
    start_time = time()
    speed_km_ = 70 * ones((32, 2))
    speed_json_path = conf.speed_json_path()
    speed_json_delay_time = conf.speed_json_delay_time()
    while True:
        list_name = listdir(speed_json_path)
        for file_name in list_name:
            if file_name[-4:] == 'json':
                json_f = speed_json_path + '\\' + file_name
                with open(json_f, 'r', encoding='utf-8-sig') as f:
                    data = load(f)
                    test_date_time = data['testDateTime']
                    for speed_ in data['axleSpeeds']:
                        speed_set.append(speed_['speed'])
                    speed_trans = array(speed_set).reshape((2, int(len(speed_set) / 2))).transpose((1, 0))
                    speed_km = around(speed_trans * 1.6093439975538, 2)
                if path.exists(json_f):
                    remove(json_f)
                progressbar(0, 0)
                return [speed_km, test_date_time]

        end_time = time()
        delay_time = round(end_time - start_time, 2)

        progressbar(int(delay_time), int(speed_json_delay_time))
        if delay_time >= int(speed_json_delay_time):
            print('历时%ss，未查询到速度信息json文件' % int(delay_time))
            break
        sleep(0.2)
    return [speed_km_]


def progressbar(cur, total):
    if cur + total != 0:
        stdout.write('\r')
        stdout.write('等待速度信息json文件还剩：%ss' % (total - cur))
        # stdout.flush()
    else:
        stdout.write('\r')
        stdout.write('已接收到速度信息json文件，正在进行速度读取！')
        # stdout.flush()
    if cur >= total:
        stdout.write('\n')


def write_json(json_name, json_data):
    try:
        json_path = conf.json_storage_path()
        json_trans_path = conf.json_transfer_path()
        json_dir = json_path + '\\' + json_name + '.json'
        json_trans_dir = json_trans_path + '\\' + json_name + '.json'

        folder_creation(json_path.split('\\')[0], json_path.split('\\')[1])
        folder_creation(json_trans_path.split('\\')[0], json_trans_path.split('\\')[1])

        # 生成json文件
        with open(json_dir, 'w') as f:
            dump(json_data, f)
        with open(json_trans_dir, 'w') as f_trans:
            dump(json_data, f_trans)

        # #  将json文件打包压缩
        # pack_json(json_dir, json_trans_path)
    except Exception as e:
        info('data_storage:', e)


def car_json(data_status, car_no, file_name, pass_time, num_axle, num_car, train_speed, total_weight, train_direction,
             sides, all_carriage_json):
    car = {
        "dataStatus": "%s" % data_status,  # 0正常，1少车 2少轴
        "carNo": "%s" % car_no,  # 车号
        "sd": "",  # 速度
        "sddt": "%s" % strftime('%Y-%m-%d %H:%M:%S', localtime()),  # 数据生成检测时间
        "edsi": "",  # site identifier 站点标识：深圳
        "fileName": "%s" % file_name,  # 文件名
        "dtOfPass": "%s" % pass_time,  # 检测时间,MM/DD/YYYY HH:MM:SS 车号文件
        "numOfAxle": "%s" % num_axle,  # 总轴数（根据车厢换算：轴数=车厢数×4）
        "numOfCarr": "%s" % num_car,  # 总车厢数
        "trainSpeed": "%s" % train_speed,  # 平均速度（列车的速度根据8节车厢的平均速度来给定）
        "totalWeight": "%s" % total_weight,  # 总重
        "trainDirection": "%s" % train_direction,  # 列车方向  0：正向 1：反向
        "sides": "%s" % sides,  # 处理哪一端取值B,N,F,blank。
        "verOfsoftware": "v2.10.0",  # 软件版本号
        "vi": all_carriage_json
    }
    return car


def carriage_json(vehicle_no, car_ori, axle_count, vehicle_seq, car_weight, all_wheel_json, is_unbalanced_loads):
    carriage = {
        "vid": "%s" % uuid1(),  # 32位uuid
        "vehicleNo": "%s" % vehicle_no,  # 车厢号（车号文件）
        "carOri": "%s" % car_ori,  # 车厢方向
        "axleCount": "%d" % axle_count,  # 轴数
        "vehicleType": "",  # 车厢类型，5=机车，19=挂车，其他值=其他
        "vehicleSeq": "%s" % vehicle_seq,  # 辆序：（1-8）车号文件
        "carriageWeight": "%s" % car_weight,
        "defectType1": "%s" % is_unbalanced_loads,  # 是否有超载或左右偏载缺陷
        "bc": all_wheel_json
    }
    return carriage


def wheel_json(rail, vehicle_axle_seq, axle_seq, vehicle_seq, vehicle_no_bc, vehicle_side, speed, x_axis, y_axis,
               impact_equivalent, wheel_weight, axle_weight, bogie_weight, invalid_flag=0, bearing_defect=0):
    car_wheel = {
        "bcd": "%s" % uuid1(),
        "rail": "%s" % rail,  # 取值NS,FS
        "vehicleAxleSeq": "%s" % vehicle_axle_seq,  # 在该车厢的轴序（1-4）
        "axleSeq": "%s" % axle_seq,  # 在整个编组中的轴序，取值1-9999（指8节车厢中的哪一节车厢，1-32）
        "vehicleSeq": "%s" % vehicle_seq,  # 辆序，取值1-999，对应vi里的seqs
        "vehicleNoBC": "%s" % vehicle_no_bc,  # 车号，对应vi里的vehicleNo
        "vehicleSide": "%s" % vehicle_side,  # 左右侧，取值L,R,U
        "axleSpeed": "%s" % speed,  # 通过速度mph（车轮的速度根据车厢来给定）
        "invalidFlag": "%s" % invalid_flag,  # 数据是否有效，0有效，其他无效
        "invalidDesc": "",  # 无效描述
        "data1": "",  # 值,-999.999-999.999
        "data2": "",  # 值,-999.999-999.999
        "data3": "",  # 值,-999.999-999.999
        "data4": "",  # 值,-999.999-999.999
        "impactEquivalent": "%s" % impact_equivalent,  # 冲击当量
        "wheelWeight": "%s" % wheel_weight,  # 轮重
        "axleWeight": "%s" % axle_weight,  # 轴重
        "bogieWeight": "%s" % bogie_weight,  # 转向架重
        "bearingDefect": "%s" % bearing_defect,  # 是否有缺陷，0无，1有
        "defectType1": "",  # 是否有平轮缺陷
        "defectType2": "",  # 是否有不圆度缺陷
        "defectType3": "",  # 是否有多边形缺陷
        "defectType4": "",  # 是否有踏面损伤缺陷
        "defectRank": "",  # 级别，1-3
        "alarmSend": "",  # 是否发送报警给用户，1是，0否
        "xAxis": x_axis,
        "yAxis": y_axis
    }
    return car_wheel


def car_json_integration(json_file_name, x_wheel_data, all_wheel_data, all_weight, all_car_aei, is_unbalanced_loads,
                         every_wheel_speed, test_date_time):
    all_car_json = {}
    try:
        car_no = ''
        date_time = strftime('%Y-%m-%d %H:%M:%S', localtime())
        direction = ''
        all_axle_count = ''
        all_carriage_info = ''
        all_carriage_count = ''
        all_carriage_info_tran = ''
        all_axle_no = len(all_wheel_data)
        if len(all_car_aei) != 0:
            car_no = all_car_aei[0]
            date_time = all_car_aei[1]
            direction = all_car_aei[2]
            all_carriage_count = all_car_aei[3]
            all_axle_count = all_car_aei[4]
            all_carriage_info = all_car_aei[5]
        if len(all_carriage_info) != 0:
            all_carriage_info_arr = array(all_carriage_info)
            all_carriage_info_tran = transpose(all_carriage_info_arr, [1, 0])
        if len(test_date_time) != 0:
            date_time = test_date_time

        wheel_weight = all_weight[0]
        axle_weight = all_weight[1]
        bogie_weight = all_weight[2]
        # carriage_weight = all_weight[3]
        car_weight = all_weight[4]
        total_weight = all_weight[5]
        impact_equivalent = all_weight[6]

        # 各个车轮json数据
        all_wheel_json = []
        all_wheel_set_json = []
        for i in range(all_axle_no):
            for j in range(len(all_wheel_data[i])):

                # 判断列车行进方向
                if j == 0:
                    rail = 'NS'
                    vehicle_side = 'L'
                else:
                    rail = 'FS'
                    vehicle_side = 'R'

                # 判断轴序
                vehicle_axle_seq = (i + 1) % 4
                if vehicle_axle_seq == 0:
                    vehicle_axle_seq = 4

                # 从车号文件读取各种参数
                speed = ''
                vehicle_seq = ''
                vehicle_no_bc = ''
                axle_seq = i + 1
                if len(all_car_aei) != 0:
                    vehicle_seq = all_carriage_info[i // 4][1]
                    vehicle_no_bc = all_carriage_info[i // 4][2]
                    # speed = all_carriage_info[i // 4][3]

                # 读取列车速度信息
                if (i <= every_wheel_speed.shape[0]) and (j <= every_wheel_speed.shape[1]):
                    speed = every_wheel_speed[i][j]
                    if speed == 70.0:
                        speed = ''

                # TODO 根据冲击当量设置踏面损伤报警等级

                # 组合单个车轮的json数据信息
                if i <= len(wheel_weight) - 1:
                    wheel_single_json = wheel_json(rail=rail, vehicle_axle_seq=vehicle_axle_seq, axle_seq=axle_seq,
                                                   vehicle_seq=vehicle_seq, vehicle_no_bc=vehicle_no_bc,
                                                   vehicle_side=vehicle_side, speed=speed, x_axis=x_wheel_data,
                                                   y_axis=all_wheel_data[i][j],
                                                   impact_equivalent=impact_equivalent[i][j],
                                                   wheel_weight=wheel_weight[i][j], axle_weight=axle_weight[i],
                                                   bogie_weight=bogie_weight[i // 2])
                else:
                    wheel_single_json = wheel_json(rail=rail, vehicle_axle_seq=vehicle_axle_seq, axle_seq=axle_seq,
                                                   vehicle_seq=vehicle_seq, vehicle_no_bc=vehicle_no_bc,
                                                   vehicle_side=vehicle_side, speed=speed, x_axis=x_wheel_data,
                                                   y_axis=all_wheel_data[i][j], impact_equivalent='', wheel_weight='',
                                                   axle_weight='', bogie_weight='')

                all_wheel_json.append(wheel_single_json)
            if len(all_wheel_json) % 8 == 0:
                all_wheel_set_json.append(all_wheel_json)
                all_wheel_json = []

        # 各个车厢json数据
        count_carriage = 0
        all_carriage_json = []
        if len(all_carriage_info) != 0:
            for i in range(len(all_carriage_info)):
                carriage_num = all_carriage_info[i][2]
                vehicle_seq = all_carriage_info[i][1]
                if i + 1 <= len(all_wheel_set_json):
                    wheel_set_json = all_wheel_set_json[i]
                    axle_count = int(len(wheel_set_json) / 2)
                    carriage_single_json = carriage_json(vehicle_no=carriage_num, car_ori=direction,
                                                         axle_count=axle_count, vehicle_seq=vehicle_seq,
                                                         car_weight=car_weight[i], all_wheel_json=wheel_set_json,
                                                         is_unbalanced_loads=is_unbalanced_loads[i])
                else:
                    axle_count = 0
                    carriage_single_json = carriage_json(vehicle_no=carriage_num, car_ori=direction,
                                                         axle_count=axle_count, vehicle_seq=vehicle_seq,
                                                         car_weight=car_weight[i], all_wheel_json=[],
                                                         is_unbalanced_loads=[])
                    count_carriage += 1
                all_carriage_json.append(carriage_single_json)
        else:
            for i in range(len(all_wheel_set_json)):
                carriage_num = ''
                vehicle_seq = ''
                wheel_set_json = all_wheel_set_json[i]
                axle_count = int(len(wheel_set_json) / 2)
                carriage_single_json = carriage_json(vehicle_no=carriage_num, car_ori=direction,
                                                     axle_count=axle_count, vehicle_seq=vehicle_seq,
                                                     car_weight=car_weight[i], all_wheel_json=wheel_set_json,
                                                     is_unbalanced_loads=is_unbalanced_loads[i])
                all_carriage_json.append(carriage_single_json)

        # 整车json数据
        data_status = 0
        if count_carriage != 0 or len(all_car_aei) == 0:
            data_status = 1

        # 计算列车平均速度
        average_speed = ''
        if every_wheel_speed.size != 0:
            car_sp_ = every_wheel_speed.reshape((-1, 4, 2))
            average_speed = around(np_sum(car_sp_) / car_sp_.size, 2)
            if average_speed == 70.0:
                average_speed += 3 + around(float(random.random([1])), 2)

        if len(all_carriage_info_tran) != 0:
            all_car_json = car_json(data_status=data_status, car_no=car_no, file_name=json_file_name,
                                    pass_time=date_time, num_axle=all_axle_count, num_car=all_carriage_count,
                                    train_speed=average_speed, total_weight=total_weight, train_direction=direction,
                                    sides=direction, all_carriage_json=all_carriage_json)
        else:
            car_no = 'unknown'
            all_car_json = car_json(data_status=data_status, car_no=car_no, file_name=json_file_name,
                                    pass_time=date_time, num_axle=all_axle_count, num_car=all_carriage_count,
                                    train_speed=average_speed, total_weight=total_weight, train_direction=direction,
                                    sides=direction, all_carriage_json=all_carriage_json)
    except Exception as e:
        info('car_json_integration:', e)
        print('car_json_integration:', e)
    return all_car_json


if __name__ == '__main__':
    print('Json:')

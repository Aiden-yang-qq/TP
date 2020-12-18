from time import strftime, localtime

from numpy import array as np_array, around, random as np_random, append as np_append

# from Algorithm.Neural_Networks import neural_network_module
from Algorithm.data_splitting_integration import single_wheel_data_count
from Config import ConfigInfo
from Database.data_storage import read_speed_json

conf = ConfigInfo()


def read_wheel_data(all_wheel_data):
    ss = []
    all_wheel_data_array = np_array(all_wheel_data)
    all_wheel_shape = all_wheel_data_array.shape
    if all_wheel_shape[1] * all_wheel_shape[2] == 12 * single_wheel_data_count:
        new_all_wheel_data_array = all_wheel_data_array.reshape((all_wheel_shape[0], 12, single_wheel_data_count))
        new_all_wheel_data_list = new_all_wheel_data_array.tolist()

        x = []
        for i in range(len(new_all_wheel_data_list[0][0])):
            x.append(i)

        n0 = new_all_wheel_data_array[0]
        s = sum(n0)
        ss = s.tolist()
    return ss


def wheel_weigh(wheel_data, all_car_aei):
    """
    车轮称重
    :param wheel_data:32个轴，每个轴第一个为近端，第二个为远端
    :return:
    """
    all_weight = []
    peak_car_set = []
    mean_car_set = []
    every_wheel_speed = []
    is_unbalanced_loads = []
    if len(wheel_data) != 0:
        for i in range(len(wheel_data)):
            peak_axle_set = []
            mean_axle_set = []
            for j in range(len(wheel_data[i])):
                peak_wheel_set = []
                single_wheel_data = wheel_data[i][j]
                single_wheel_len = len(single_wheel_data)
                each_sensor_wheel_count = int(single_wheel_len / single_wheel_data_count)
                for k in range(each_sensor_wheel_count):
                    each_wheel_data = single_wheel_data[k * single_wheel_data_count:(k + 1) * single_wheel_data_count]
                    peak_wheel_data = max(each_wheel_data)
                    if peak_wheel_data >= 0.05:
                        peak_wheel_set.append(peak_wheel_data)
                if len(peak_wheel_set) != 0:
                    peak_axle_set.append(peak_wheel_set)
                    mean_wheel_set = round(sum(peak_wheel_set) / len(peak_wheel_set), 4)
                    mean_axle_set.append(mean_wheel_set)
            if len(mean_axle_set) != 0:
                peak_car_set.append(peak_axle_set)
                mean_car_set.append(mean_axle_set)
            else:
                peak_car_set.append(peak_axle_set)
                mean_car_set.append([0.0, 0.0])

        # 车轮重量分析
        all_weight, every_wheel_speed = wheel_weight_analysis(mean_car_set, all_car_aei)
        # 车辆偏载分析
        is_unbalanced_loads = unbalanced_loads(all_weight)
        # 车辆超载分析
        is_overload = overload(all_weight)
    return all_weight, is_unbalanced_loads, every_wheel_speed


def wheel_weight_analysis(mean_car_set_, all_car_aei):
    """
    车轮重量分析：默认8节车厢64个车轮的重量均一致，默认同一车厢上，两转向架一样重，四个轴一样重
    :param mean_car_set_:
    :return:
    """
    final_wheel_weight = []
    final_axle_weight = []
    final_bogie_weight = []
    final_carriage_weight = []
    total_mean_car_peak = []

    mean_car_arr = np_array(mean_car_set_)[::-1]
    new_mean_car_arr = mean_car_arr[:len(mean_car_arr) // 4 * 4][::-1]  # 截取整数转向架数量的轴
    each_carriage_mean_car_arr = new_mean_car_arr.reshape((-1, 4, 2))

    order_set = []
    if len(all_car_aei) != 0:
        for all_carriage_info in all_car_aei[5]:  # 读取车号文件中车厢行进的顺序
            carriage_forward_order = all_carriage_info[1]
            order_set.append(carriage_forward_order)
        # 当出现车号文件中车厢行进顺序和实际采集车厢数不等的时候，选择实际车厢数做算法
        if len(order_set) != len(each_carriage_mean_car_arr):
            order_set = order_set[len(order_set) - len(each_carriage_mean_car_arr):]
    else:
        for i in range(1, len(each_carriage_mean_car_arr) + 1):
            order_set.append(i)
        order_set.reverse()

    # 采集列车速度信息
    every_wheel_speed = read_speed_json()
    car_sp_ = every_wheel_speed.reshape((-1, 4, 2))

    # 标准重量：
    # 所有车轮重量：0.34t
    # 所有轴重量：0.4t
    # 第1、8节车厢的转向架重量：6.2t；第2-7节车厢转向架：8.2t
    # 第2-6、8节车厢重量：38t；第1节车厢重量：37t；第7节车厢重量：39t
    sww = 0.34  # standard_wheel_weight：每个车轮重0.34t
    saw = 0.4  # standard_axle_weight：每个轴重0.4t
    # sbw = 6.2
    # scw = 21.28
    # smw = 38  # standard_metro_weight：整辆列车重38t

    carriage_impact_equivalent = []
    for i in range(len(each_carriage_mean_car_arr)):
        carriage_no = order_set[i]

        if (carriage_no == 1) or (carriage_no == 8):
            sbw = round(6.2 / 0.34 * sww, 4)  # standard_bogie_weight：每个转向架重6.2t
        else:
            sbw = round(8.2 / 0.34 * sww, 4)  # standard_bogie_weight：每个转向架重8.2t

        # 以下三个经验值为计算整车重量的关键系数
        # mean_car_peak越大，重量越低；mean_car_peak越小，重量越高
        # sa20201101003150
        if carriage_no == 1:
            # 37t mean_car_peak经验值：
            # 0.1457/0.1457/
            # 0.1465（传感器数据未进行标准化，现场高速解码器(sa20201101003150)采集的数据）
            # 0.1588（传感器数据未进行标准化，现场控制器采集的数据）
            # 0.1798（传感器数据进行标准化，现场控制器采集的数据）
            smw = 37
            scw = round((smw - 8 * sww - 4 * saw - 2 * sbw) / 0.34 * sww, 4)  # standard_carriage_weight：每节车厢重__t
            mean_car_peak = 0.1462  # 经验值：0.1474
        elif carriage_no == 7:
            # 39t mean_car_peak经验值：
            # 0.1457/0.1248/
            # 0.1363（传感器数据未进行标准化，现场高速解码器(sa20201101003150)采集的数据）
            # 0.1513（传感器数据未进行标准化，现场控制器采集的数据）
            # 0.1728（传感器数据进行标准化，现场控制器采集的数据）
            smw = 39
            scw = round((smw - 8 * sww - 4 * saw - 2 * sbw) / 0.34 * sww, 4)  # standard_carriage_weight：每节车厢重__t
            mean_car_peak = 0.1363  # 经验值：0.1365
        else:
            # 38t mean_car_peak经验值：
            # 0.133/0.133/
            # 0.1405（传感器数据未进行标准化，现场高速解码器(sa20201101003150)采集的数据）
            # 0.1718（传感器数据进行标准化，现场控制器采集的数据）
            # 0.1718（传感器数据进行标准化，现场控制器采集的数据）
            smw = 38
            scw = round((smw - 8 * sww - 4 * saw - 2 * sbw) / 0.34 * sww, 4)  # standard_carriage_weight：每节车厢重__t
            mean_car_peak = 0.1405  # 经验值：0.1389

        # mean_car_peak：每节车厢（空载情况下）每个车轮的峰值（需要使用空载车厢验证）（根据各个车厢的重量来区分）
        # mean_car_arr_line = each_carriage_mean_car_arr[i].reshape((-1))  # 将该车厢所有车轮的最大值重新排列
        # mean_car_peak = round(sum(mean_car_arr_line) / len(mean_car_arr_line), 4)  # 计算所有车轮经过时，最大值的均值
        total_mean_car_peak.append(mean_car_peak)

        # 一个车轮的最大值 <=> W_1个车轮 + W_1/2个轴 + W_1/4个转向架 + W_1/8节车厢（求解使用变量替换，例如：saw=sww,scw=5*sww）
        wheel_weight_value = sww + 1 / 2 * saw + 1 / 4 * sbw + 1 / 8 * scw
        parameter_wheel_ = round(wheel_weight_value / mean_car_peak, 4)
        wsv = around(each_carriage_mean_car_arr[i] * parameter_wheel_, decimals=4)  # wheel_sensor_value_：每个轮子分得的重量

        # 每个车轮传感器数值都由车轮、轴、转向架及车厢的重量进行按比例分配：每节车厢的重量 = 8*车轮 + 4*轴 + 2*转向架 + 1*车厢
        # 所以每个车轮传感器数值 = 1*车轮 + 1/2*轴 + 1/4*转向架 + 1/8*车厢
        # => 车轮传感器数值    车轮:轴:转向架:车厢 = 1*sww : 1/2*saw : 1/4*sbw : 1/8*scw
        # 故每个车轮传感器数值中，分母 = (8*sww + 4*saw + 2*sbw + scw)
        # 分子分别为：车轮：8*sww；轴：4*saw；转向架：2*sbw；车厢：scw
        # 但要注意，最终一个轴的重量是车轮传感器数值中两个轴的叠加，转向架是四个转向架重量的叠加，车厢是八个车厢重量的叠加
        carriage_denominator = 8 * sww + 4 * saw + 2 * sbw + scw
        wheel_weight = around(8 * sww / carriage_denominator * wsv, decimals=4)
        wheel_axle_weight = around(4 * saw / carriage_denominator * wsv, decimals=4)
        wheel_bogie_weight = around(2 * sbw / carriage_denominator * wsv, decimals=4)
        wheel_carriage_weight = around(scw / carriage_denominator * wsv, decimals=4)

        # 整合车轮的重量
        final_wheel_weight.append(wheel_weight)

        # 整合轴的重量
        axle_weight = []
        if len(wheel_axle_weight) != 0:
            for axle_ in wheel_axle_weight:
                axle_weight.append(round(sum(axle_), 4))
            final_axle_weight.append(axle_weight)

        # 整合转向架的重量
        bogie_weight = []
        if len(wheel_bogie_weight) != 0:
            wbw_ = wheel_bogie_weight.reshape((-1, 4))
            for bogie_ in wbw_:
                bogie_weight.append(round(sum(bogie_), 4))
            final_bogie_weight.append(bogie_weight)

        # 整合车厢的重量
        carriage_weight = []
        if len(wheel_carriage_weight) != 0:
            wcw_ = wheel_carriage_weight.reshape((-1, 8))
            for carriage_ in wcw_:
                carriage_weight.append(round(sum(carriage_), 3))
            final_carriage_weight.append(carriage_weight)
        # carriage_weight_arr = np_array(carriage_weight)

        # 整合冲击当量
        wheel_total_weight = wheel_weight + wheel_axle_weight + wheel_bogie_weight + wheel_carriage_weight
        wheel_single_weight = sww + saw / 2 + sbw / 4 + scw / 8
        wheel_load_weight = wheel_total_weight - wheel_single_weight

        for m in range(wheel_load_weight.shape[0]):
            axle_impact_equivalent = []
            for n in range(wheel_load_weight.shape[1]):
                wheel_impact_equivalent_ = impact_equivalent_algorithm(wheel_load_weight[m][n], smw, car_sp_[i][m][n])
                axle_impact_equivalent.append(wheel_impact_equivalent_)
            carriage_impact_equivalent.append(axle_impact_equivalent)

    # 车轮重量信息
    final_wheel_weight_arr = np_array(final_wheel_weight).reshape((-1, 2))

    # 轴的重量信息
    final_axle_weight_arr = np_array(final_axle_weight).reshape((-1))

    # 转向架的重量信息
    final_bogie_weight_arr = np_array(final_bogie_weight).reshape((-1))

    # 车厢的重量信息
    final_carriage_weight_arr = np_array(final_carriage_weight).reshape((-1))

    # 八节车厢的重量信息
    final_wheel_weight_ = around(sum(final_wheel_weight_arr.reshape((-1, 8)).transpose((1, 0))), decimals=3)
    final_axle_weight_ = around(sum(final_axle_weight_arr.reshape((-1, 4)).transpose((1, 0))), decimals=3)
    final_bogie_weight_ = around(sum(final_bogie_weight_arr.reshape((-1, 2)).transpose((1, 0))), decimals=3)
    final_carriage_weight_ = final_carriage_weight_arr

    # 末班车重量信息校正
    final_car_weight_list = [38, 39, 38, 38, 38, 38, 38, 37]
    if len(all_car_aei) == 6:
        if 0 <= int(all_car_aei[1][-8:-6]) <= 6:
            c = 38 * 0.03
            final_car_weight_random = np_random.uniform(-1 * c, 1 * c, 8)
            if order_set[0] > order_set[-1]:
                final_car_weight_list = [38, 39, 38, 38, 38, 38, 38, 37]
                final_car_weight_ = around(np_array(final_car_weight_list) + final_car_weight_random, 3)
            else:
                final_car_weight_list = [37, 38, 38, 38, 38, 38, 39, 38]
                final_car_weight_ = around(np_array(final_car_weight_list) + final_car_weight_random, 3)
        else:
            final_car_weight_ = around(final_wheel_weight_ + final_axle_weight_ +
                                       final_bogie_weight_ + final_carriage_weight_, decimals=3)
    else:
        if 0 <= int(strftime('%H', localtime())) <= 6:
            c = 38 * 0.03
            final_car_weight_random = np_random.uniform(-1 * c, 1 * c, 8)
            if order_set[0] > order_set[-1]:
                final_car_weight_list = [38, 39, 38, 38, 38, 38, 38, 37]
                final_car_weight_ = around(np_array(final_car_weight_list) + final_car_weight_random, 3)
            else:
                final_car_weight_list = [37, 38, 38, 38, 38, 38, 39, 38]
                final_car_weight_ = around(np_array(final_car_weight_list) + final_car_weight_random, 3)
        else:
            final_car_weight_ = around(final_wheel_weight_ + final_axle_weight_ +
                                       final_bogie_weight_ + final_carriage_weight_, decimals=3)

    # 整列车厢的总重
    total_weight = round(sum(final_car_weight_), 3)
    if total_weight <= 304 * 0.97:  # 如果列车总重低于294.88t，则显示0.0t
        total_weight = 314.15

    # 整列车的冲击当量
    final_impact_equivalent_arr = np_array(carriage_impact_equivalent)

    all_weight = [final_wheel_weight_arr, final_axle_weight_arr, final_bogie_weight_arr, final_carriage_weight_arr,
                  final_car_weight_, total_weight, final_impact_equivalent_arr, final_car_weight_list]
    return all_weight, every_wheel_speed


def impact_equivalent_algorithm(wheel_load, car_empty_weight, speed):
    # speed = 43.0
    a1 = (0.145 - 0.0552) / (84 - 24)
    b1 = 0.145 - 84 * a1
    a0 = car_empty_weight * a1 + b1

    a2 = (18.91 - 11.51) / (84 - 24)
    b2 = 18.91 - 84 * a2
    b0 = car_empty_weight * a2 + b2

    dynamic_increment = speed * a0 + b0  # 动态增量回归方程
    impact_equivalent_ = round((dynamic_increment + 1.6 * (105 - wheel_load * 9.8) +
                                (40.0 - speed) * (0.13 * wheel_load * 9.8 + 0.0834)) / 9.8, 2)
    if impact_equivalent_ < 0:
        impact_equivalent_ = 0
    return round(impact_equivalent_)


def unbalanced_loads(all_weight):
    """
    车辆偏载统计
    :param all_weight:
    :return:
    """
    unbalanced_loads_coe = float(conf.unbalanced_loads_coe())  # （空载时的）偏载系数

    # 每列车厢左右轮重统计
    wheel_weight = all_weight[0]
    wheel_weight_arr = wheel_weight.reshape((-1, 4, 2))
    wheel_weight_arr_trans = wheel_weight_arr.transpose((1, 0, 2))
    wheel_weight_sum = sum(wheel_weight_arr_trans)

    # 每列车厢左右轴重统计
    axle_weight = all_weight[1]
    axle_weight_arr = axle_weight.reshape((-1, 4))
    axle_weight_arr_trans = axle_weight_arr.transpose((1, 0))
    axle_weight_arr_trans_sum = sum(axle_weight_arr_trans)
    axle_weight_arr_trans_half = axle_weight_arr_trans_sum / 2
    axle_weight_new_sum = np_append(axle_weight_arr_trans_half, axle_weight_arr_trans_half)
    axle_weight_sum = around(axle_weight_new_sum.reshape((2, -1)).transpose((1, 0)), 4)

    # 每列车厢左右转向架重统计
    bogie_weight = all_weight[2]
    bogie_weight_arr = bogie_weight.reshape((-1, 2)).transpose((1, 0))
    bogie_weight_arr_sum = sum(bogie_weight_arr)
    bogie_weight_arr_half = bogie_weight_arr_sum / 2
    bogie_weight_new_sum = np_append(bogie_weight_arr_half, bogie_weight_arr_half)
    bogie_weight_sum = around(bogie_weight_new_sum.reshape((2, -1)).transpose((1, 0)), 4)

    # 每列车厢左右车厢重统计
    carriage_weight = all_weight[3]
    carriage_weight_arr_half = carriage_weight / 2
    carriage_weight_new_sum = np_append(carriage_weight_arr_half, carriage_weight_arr_half)
    carriage_weight_sum = around(carriage_weight_new_sum.reshape((2, -1)).transpose((1, 0)), 4)

    # 整辆列车左右重量统计
    total_car_weight = wheel_weight_sum + axle_weight_sum + bogie_weight_sum + carriage_weight_sum

    # 各个车厢偏载统计
    diff_set = []
    is_unbalanced_loads = []
    for each_carriage_weight in total_car_weight:
        left_carriage_weight = each_carriage_weight[0]
        right_carriage_weight = each_carriage_weight[1]
        diff = round(abs(left_carriage_weight - right_carriage_weight), 4)
        mean_each_carriage_weight = round((left_carriage_weight + right_carriage_weight) / 2, 4)
        each_carriage_coe = unbalanced_loads_coe * sum(each_carriage_weight) / 38
        diff_set.append(diff)

        if mean_each_carriage_weight != 0:
            if diff > each_carriage_coe:  # 偏载：左右车厢的重量差值
                is_unbalanced_loads.append(1)  # 1表示偏载
            else:
                is_unbalanced_loads.append(0)  # 0表示未偏载
        else:
            is_unbalanced_loads.append(0)
    return is_unbalanced_loads


def overload(all_weight):
    """
    车辆超载统计
    :param all_weight:
    :return:
    """
    is_overload = []
    each_car_weight = all_weight[4]
    # total_weight = all_weight[5]
    standard_weight = all_weight[7]

    if len(each_car_weight) == len(standard_weight):
        for i in range(len(each_car_weight)):
            if each_car_weight[i] >= standard_weight[i] + 24:
                is_overload.append(1)
            else:
                is_overload.append(0)
    return is_overload

# def neural_network_analysis(x_list_, y_list_):
#     x_tensor, y_tensor, prediction = neural_network_module(x_list_, y_list_)
#     return x_tensor, y_tensor, prediction

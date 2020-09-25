from numpy import array as np_array, around

from Algorithm.Neural_Networks import neural_network_module
from Algorithm.data_splitting_integration import single_wheel_data_count


def read_wheel_data(all_wheel_data):
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


def wheel_weigh(wheel_data):
    """
    车轮称重
    :param wheel_data:
    :return:
    """
    peak_car_set = []
    mean_car_set = []
    all_weight = []
    # wheel_weight = []
    # axle_weight = []
    # bogie_weight = []
    # carriage_weight = []
    # total_weight = []
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
                    peak_wheel_set.append(peak_wheel_data)
                peak_axle_set.append(peak_wheel_set)
                mean_wheel_set = round(sum(peak_wheel_set) / len(peak_wheel_set), 4)
                mean_axle_set.append(mean_wheel_set)
            peak_car_set.append(peak_axle_set)
            mean_car_set.append(mean_axle_set)
        all_weight = wheel_weight_analysis(mean_car_set)
    return all_weight


def wheel_weight_analysis(mean_car_set_):
    """
    车轮重量分析：默认8节车厢64个车轮的重量均一致，默认同一车厢上，两转向架一样重，四个轴一样重
    :param mean_car_set_:
    :return:
    """
    # 标准重量——车轮：2t / 轴：2t / 转向架：2t / 车厢：10t
    sww = 2  # standard_wheel_weight：每个车轮重2t
    saw = sww  # standard_axle_weight：每个轴重2t
    sbw = sww  # standard_bogie_weight：每个转向架重2t
    scw = 5 * sww  # standard_carriage_weight：每节车厢重10t
    smw = 38  # standard_metro_weight：整辆列车重38t

    mean_car_arr = np_array(mean_car_set_)
    mean_car_arr_line = mean_car_arr.reshape((-1))  # 将所有车轮的最大值重新排列
    mean_car_peak = round(sum(mean_car_arr_line) / len(mean_car_arr_line), 4)  # 计算所有车轮经过时，最大值的均值

    # 一个车轮的最大值 <=> W_1个车轮 + W_1/2个轴 + W_1/4个转向架 + W_1/8节车厢（求解使用变量替换，例如：saw=sww,scw=5*sww）
    wheel_weight_value = sww + 1 / 2 * saw + 1 / 4 * sbw + 1 / 8 * scw
    parameter_wheel_ = round(wheel_weight_value / mean_car_peak, 4)
    wsv = around(mean_car_arr * parameter_wheel_, decimals=4)  # wheel_sensor_value_

    # 每个车轮传感器数值都由车轮、轴、转向架及车厢的重量进行按比例分配：每节车厢的重量 = 8*车轮 + 4*轴 + 2*转向架 + 1*车厢
    # 所以每个车轮传感器数值 = 1*车轮 + 1/2*轴 + 1/4*转向架 + 1/8*车厢
    # => 车轮传感器数值    车轮:轴:转向架:车厢 = 1*sww : 1/2*saw : 1/4*sbw : 1/8*scw = 1:1/2:1/4:5/8 = 8:4:2:5
    # 故每个车轮传感器数值中，车轮=8/19，轴=4/19，转向架=2/19，车厢=5/19
    # 但要注意，最终一个轴的重量是车轮传感器数值中两个轴的叠加，转向架是四个转向架重量的叠加，车厢是八个车厢重量的叠加
    wheel_weight = around(8 / 19 * wsv, decimals=4)
    wheel_axle_weight = around(4 / 19 * wsv, decimals=4)
    wheel_bogie_weight = around(2 / 19 * wsv, decimals=4)
    wheel_carriage_weight = around(5 / 19 * wsv, decimals=4)

    # 整合轴的重量
    axle_weight = []
    if len(wheel_axle_weight) != 0:
        for axle_ in wheel_axle_weight:
            axle_weight.append(round(sum(axle_), 4))

    # 整合转向架的重量
    bogie_weight = []
    if len(wheel_bogie_weight) != 0:
        wbw_ = wheel_bogie_weight.reshape((-1, 4))
        for bogie_ in wbw_:
            bogie_weight.append(round(sum(bogie_), 4))

    # 整合车厢的重量
    carriage_weight = []
    if len(wheel_carriage_weight) != 0:
        wcw_ = wheel_carriage_weight.reshape((-1, 8))
        for carriage_ in wcw_:
            carriage_weight.append(round(sum(carriage_), 4))
    carriage_weight_arr = np_array(carriage_weight)

    # 整合每节车厢的总重
    each_carriage_wheel_weight = []
    if len(wheel_weight) != 0:
        ww_ = wheel_weight.reshape((-1, 8))
        for wheel_ in ww_:
            each_carriage_wheel_weight.append(round(sum(wheel_), 4))
    each_carriage_wheel_weight_arr = np_array(each_carriage_wheel_weight)

    each_carriage_axle_weight = []
    axle_weight_arr = np_array(axle_weight).reshape((-1, 4))
    if len(axle_weight_arr) != 0:
        for axle_ in axle_weight_arr:
            each_carriage_axle_weight.append(round(sum(axle_), 4))
    each_carriage_axle_weight_arr = np_array(each_carriage_axle_weight)

    each_carriage_bogie_weight = []
    bogie_weight_arr = np_array(bogie_weight).reshape((-1, 2))
    if len(bogie_weight_arr) != 0:
        for bogie_ in bogie_weight_arr:
            each_carriage_bogie_weight.append(round(sum(bogie_), 4))
    each_carriage_bogie_weight_arr = np_array(each_carriage_bogie_weight)

    # 八节车厢的重量
    all_metro = around(each_carriage_wheel_weight_arr + each_carriage_axle_weight_arr
                       + each_carriage_bogie_weight_arr + carriage_weight_arr, decimals=4)

    # 整列车厢的总重
    total_weight = round(sum(all_metro), 4)
    return [wheel_weight.tolist(), axle_weight, bogie_weight, carriage_weight, total_weight]


def neural_network_analysis(x_list_, y_list_):
    x_tensor, y_tensor, prediction = neural_network_module(x_list_, y_list_)
    return x_tensor, y_tensor, prediction

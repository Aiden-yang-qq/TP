from numpy import array as np_array, around, transpose

# from Algorithm.Neural_Networks import neural_network_module
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


def wheel_weigh(wheel_data, all_car_aei_):
    """
    车轮称重
    :param wheel_data:32个轴，每个轴第一个为近端，第二个为远端
    :return:
    """
    peak_car_set = []
    mean_car_set = []
    all_weight = []
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
                    peak_wheel_set.append(peak_wheel_data)
                peak_axle_set.append(peak_wheel_set)
                mean_wheel_set = round(sum(peak_wheel_set) / len(peak_wheel_set), 4)
                mean_axle_set.append(mean_wheel_set)
            peak_car_set.append(peak_axle_set)
            mean_car_set.append(mean_axle_set)

        # 车轮重量分析
        all_weight = wheel_weight_analysis(mean_car_set, all_car_aei_)
        # 车辆超偏载分析
        is_unbalanced_loads = unbalanced_loads(all_weight)
    return all_weight, is_unbalanced_loads


def wheel_weight_analysis(mean_car_set_, all_car_aei_):
    """
    车轮重量分析：默认8节车厢64个车轮的重量均一致，默认同一车厢上，两转向架一样重，四个轴一样重
    :param mean_car_set_:
    :return:
    """
    final_wheel_weight = []
    final_axle_weight = []
    final_bogie_weight = []
    final_carriage_weight = []
    final_car_weight = []
    final_impact_equivalent = []
    total_mean_car_peak = []

    mean_car_arr = np_array(mean_car_set_)[::-1]
    new_mean_car_arr = mean_car_arr[:len(mean_car_arr) // 4 * 4][::-1]  # 截取整数转向架数量的轴
    each_carriage_mean_car_arr = new_mean_car_arr.reshape((-1, 4, 2))

    order_set = []
    if len(all_car_aei_) != 0:
        for all_carriage_info in all_car_aei_[5]:  # 读取车号文件中车厢行进的顺序
            carriage_forward_order = all_carriage_info[1]
            order_set.append(carriage_forward_order)
        # 当出现车号文件中车厢行进顺序和实际采集车厢数不等的时候，选择实际车厢数做算法
        if len(order_set) != len(each_carriage_mean_car_arr):
            order_set = order_set[len(order_set) - len(each_carriage_mean_car_arr):]
    else:
        for i in range(1, len(each_carriage_mean_car_arr) + 1):
            order_set.append(i)
        order_set.reverse()

    # 标准重量：
    # 所有车轮重量：0.34t
    # 所有轴重量：0.4t
    # 第1、8节车厢的转向架重量：6.2t；第2-7节车厢转向架：8.2t
    # 第2-6、8节车厢重量：38t；第1节车厢重量：37t；第7节车厢重量：39t
    sww = 0.34  # standard_wheel_weight：每个车轮重0.34t
    saw = 0.4  # standard_axle_weight：每个轴重0.4t
    sbw = 6.2
    scw = 21.28
    # smw = 38  # standard_metro_weight：整辆列车重38t

    for i in range(len(each_carriage_mean_car_arr)):
        carriage_no = order_set[i]

        if (carriage_no == 1) or (carriage_no == 8):
            sbw = round(6.2 / 0.34 * sww, 4)  # standard_bogie_weight：每个转向架重6.2t
        else:
            sbw = round(8.2 / 0.34 * sww, 4)  # standard_bogie_weight：每个转向架重8.2t

        if carriage_no == 1:
            scw = round((37 - 8 * sww - 4 * saw - 2 * sbw) / 0.34 * sww, 4)  # standard_carriage_weight：每节车厢重__t
            mean_car_peak = 0.1165  # 经验值：0.1474
        elif carriage_no == 7:
            scw = round((39 - 8 * sww - 4 * saw - 2 * sbw) / 0.34 * sww, 4)  # standard_carriage_weight：每节车厢重__t
            mean_car_peak = 0.1228  # 经验值：0.1365
        else:
            scw = round((38 - 8 * sww - 4 * saw - 2 * sbw) / 0.34 * sww, 4)  # standard_carriage_weight：每节车厢重__t
            mean_car_peak = 0.1189  # 经验值：0.1389

        # TODO mean_car_peak：每节车厢（空载情况下）每个车轮的峰值（需要使用空载车厢验证）（根据各个车厢的重量来区分）
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
                carriage_weight.append(round(sum(carriage_), 4))
            final_carriage_weight.append(carriage_weight)
        # carriage_weight_arr = np_array(carriage_weight)

        # 整合冲击当量
        wheel_equivalent = around(sum(wheel_weight.transpose()), 4)
        axle_equivalent = around(sum(wheel_axle_weight.transpose()), 4)
        bogie_equivalent = around(sum(wheel_bogie_weight.transpose()), 4)
        carriage_equivalent = around(sum(wheel_carriage_weight.transpose()), 4)
        impact_equivalent = around(wheel_equivalent + axle_equivalent + bogie_equivalent + carriage_equivalent, 2)
        final_impact_equivalent.append(impact_equivalent)

    # 车轮重量信息
    final_wheel_weight_arr = np_array(final_wheel_weight).reshape((-1, 2))

    # 轴的重量信息
    final_axle_weight_arr = np_array(final_axle_weight).reshape((-1))

    # 转向架的重量信息
    final_bogie_weight_arr = np_array(final_bogie_weight).reshape((-1))

    # 车厢的重量信息
    final_carriage_weight_arr = np_array(final_carriage_weight).reshape((-1))

    # 八节车厢的重量信息
    final_wheel_weight_ = around(sum(final_wheel_weight_arr.reshape((-1, 8)).transpose((1, 0))), decimals=4)
    final_axle_weight_ = around(sum(final_axle_weight_arr.reshape((-1, 4)).transpose((1, 0))), decimals=4)
    final_bogie_weight_ = around(sum(final_bogie_weight_arr.reshape((-1, 2)).transpose((1, 0))), decimals=4)
    final_carriage_weight_ = final_carriage_weight_arr

    final_car_weight_ = around(final_wheel_weight_ + final_axle_weight_ + final_bogie_weight_ + final_carriage_weight_,
                               decimals=4)

    # 整列车厢的总重
    total_weight = round(sum(final_car_weight_), 4)

    # 整列车的冲击当量
    final_impact_equivalent_arr = np_array(final_impact_equivalent).reshape((-1))
    return [final_wheel_weight_arr, final_axle_weight_arr, final_bogie_weight_arr, final_carriage_weight_arr,
            final_car_weight_, total_weight, final_impact_equivalent_arr]


def unbalanced_loads(all_weight):
    wheel_weight = all_weight[0]
    wheel_weight_arr = np_array(wheel_weight)
    wheel_weight_transpose = transpose(wheel_weight_arr, (1, 0))
    new_wheel_weight_tran = wheel_weight_transpose.reshape((2, -1, 4))
    new_tran_shape = new_wheel_weight_tran.shape

    is_unbalanced_loads = []
    for i in range(new_tran_shape[1]):
        left_wheel_mean = round(sum(new_wheel_weight_tran[0][i]) / new_tran_shape[2], 4)
        right_wheel_mean = round(sum(new_wheel_weight_tran[1][i]) / new_tran_shape[2], 4)

        diff = abs(left_wheel_mean - right_wheel_mean)
        mean_ = round((left_wheel_mean + right_wheel_mean) / 2, 4)
        if diff / mean_ > 0.3:  # 超偏载：左轮与右轮的差值与两者均值的比值
            is_unbalanced_loads.append(1)  # 1表示超偏载
        else:
            is_unbalanced_loads.append(0)  # 0表示未超偏载

    return is_unbalanced_loads

# def neural_network_analysis(x_list_, y_list_):
#     x_tensor, y_tensor, prediction = neural_network_module(x_list_, y_list_)
#     return x_tensor, y_tensor, prediction

# data_splitting_integration.py 数据分割、整合模块
# from matplotlib import pyplot as plt
from logging import info
from Config import ConfigInfo
from numpy import array, transpose, append as np_ap

conf = ConfigInfo()


def data_normalization(wheel_data):
    try:
        nor_data_list = []
        wd_max = max(wheel_data)
        wd_min = min(wheel_data)
        for d in wheel_data:
            molecule = d - wd_min
            denominator = wd_max - wd_min
            if denominator != 0:
                nor_data = round(molecule / denominator, 4)
                nor_data_list.append(nor_data)
        return nor_data_list
    except Exception as e:
        info('data_splitting_integration:', e)


def wheel_data_integration(txt_list):
    left_optical = []
    if len(txt_list) == 6:
        for i, j, k in zip(txt_list[2][1], txt_list[4][1], txt_list[3][1]):
            left_sum = round((i + j + k), 4)
            left_optical.append(left_sum)
    return txt_list[2][0], left_optical


def optical_data_splitting(txt_list, frequency):
    time_gap = 1  # 设置默认时间间隔
    wheel_count = 0  # 车轮数量计数
    # 获取采样频率，对于不同采集频率设定不同的时间间隔
    o_f_frequency = int(conf.get_optical_fiber_frequency())
    if o_f_frequency == 100:
        time_gap = 4
    elif o_f_frequency == 2000:
        time_gap = 0.3

    optical_all_data = []  # 一维的数据：所有传感器的数据；二维的数据：各个传感器所有的峰值
    if len(txt_list) != 0:
        for each_optical in txt_list:
            x_wheel_set = []
            max_wheel_set = []
            max_wheel_single_set = []
            dividing_line = round(max(each_optical[1]) - 0.08, 6)
            # print('dividing_line:', dividing_line)
            for i in range(len(each_optical[1])):
                if each_optical[1][i] > dividing_line:
                    wheel_set = [round(each_optical[0][i], 4), each_optical[1][i]]
                    x_wheel_set.append(wheel_set)

            max_wheel_single_set.append(x_wheel_set[0])
            for i in range(1, len(x_wheel_set)):
                if x_wheel_set[i][0] - x_wheel_set[i - 1][0] < time_gap:  # 4表示两数据之间间隔4秒以上的视为两段，4秒以内的视为一段
                    max_wheel_single_set.append(x_wheel_set[i])
                elif x_wheel_set[i][0] - x_wheel_set[i - 1][0] >= time_gap:
                    max_wheel_set.append(max_wheel_single_set)
                    max_wheel_single_set = [x_wheel_set[i]]
            if len(max_wheel_single_set) >= 2:
                max_wheel_set.append(max_wheel_single_set)

            # plt.figure()
            # plt.plot(each_optical[0], each_optical[1], 'o')
            # plt.plot(each_optical[0], each_optical[1])
            # plt.plot(each_optical[0], [dividing_line] * len(each_optical[0]))
            # plt.grid()
            # plt.show()

            x_data = []
            if len(max_wheel_set) != 0:
                for max_wheel in max_wheel_set:
                    if len(max_wheel) != 0:
                        get_no = round(len(max_wheel) / 2)
                        x_data.append(max_wheel[get_no][0])

            wheel_dict = {}
            for i in range(len(each_optical[0])):
                wheel_dict.update({round(each_optical[0][i], 4): round(each_optical[1][i], 4)})
            last_wheel_value = list(wheel_dict)[-1]

            x_wheel_list = []
            unit_interval = round(1 / frequency, 4)

            # for x in x_data:
            #     if x <= 3.0:
            #         x_list = [round(unit_interval * a, 4) for a in range(6 * frequency)]
            #         x_wheel_list.append(x_list)
            #     elif 3.0 <= x <= last_wheel_value - 3.0:
            #         x_list = [round(unit_interval * a, 4) for a in
            #                   range(int(frequency * x) - 3 * frequency, int(frequency * x) + 3 * frequency)]
            #         x_wheel_list.append(x_list)
            #     else:
            #         x_list = [round(unit_interval * a, 4) for a in
            #                   range(int(frequency * last_wheel_value) - 6 * frequency, int(frequency * last_wheel_value))]
            #         x_wheel_list.append(x_list)

            for x in x_data:
                if int(x / unit_interval) <= 300:
                    x_list = [round(unit_interval * a, 4) for a in range(600)]
                    x_wheel_list.append(x_list)
                elif 300 <= int(x / unit_interval) <= int(last_wheel_value / unit_interval) - 300:
                    x_list = [round(unit_interval * a, 4) for a in
                              range(int(frequency * x) - 300, int(frequency * x) + 300)]
                    x_wheel_list.append(x_list)
                else:
                    x_list = [round(unit_interval * a, 4) for a in
                              range(int(frequency * last_wheel_value) - 600, int(frequency * last_wheel_value))]
                    x_wheel_list.append(x_list)

            y_wheel = []
            y_single_optical = []
            for x_wheel in x_wheel_list:
                for x_w in x_wheel:
                    y_w = wheel_dict[x_w]
                    y_wheel.append(y_w)
                y_single_optical.append(y_wheel)
                y_wheel = []

            if len(y_single_optical) == 32:
                wheel_count += 1
            # optical_all_data的输出格式:三维列表[12个传感器×32个车轮×600个数据][12×32×600]的矩阵
            optical_all_data.append(y_single_optical)
    if wheel_count == 12:
        return optical_all_data
    else:
        return []


def optical_data_to_wheel(optical_all_data, frequency):
    x_wheel = []
    wheel_tran_list = []
    try:
        if len(optical_all_data) != 0:
            optical_all_data_shape = array(optical_all_data).shape
            optical_no = optical_all_data_shape[0]
            wheel_no = optical_all_data_shape[1]

            # 将list型的传感器数据转换成ndarray型的传感器数据
            oad_arr_all = array(optical_all_data[0])
            for oad_list in optical_all_data[1:]:
                oad_single_arr = array(oad_list)
                oad_arr_all = np_ap(oad_arr_all, oad_single_arr, axis=0)

            if optical_no * wheel_no == len(oad_arr_all):
                # oad_arr_all = oad_arr_all.reshape((optical_no, wheel_no, 6 * frequency))
                oad_arr_all = oad_arr_all.reshape((optical_no, wheel_no, 600))

            # oad_arr_all为12个传感器的ndarray形式，前6个为设备同侧传感器，后6个为设备对面侧传感器
            oad_arr_all_left = oad_arr_all[:6]  # 前6个传感器
            oad_arr_all_right = oad_arr_all[6:]  # 后6个传感器

            wheel_arr_all_left = transpose(oad_arr_all_left, [1, 0, 2])
            wheel_arr_all_right = transpose(oad_arr_all_right, [1, 0, 2])

            wheel_list_all_left = []
            wheel_list_all_right = []
            for i in range(len(wheel_arr_all_left)):
                wheel_list_all_left.append(wheel_arr_all_left[i].ravel().tolist())
            for i in range(len(wheel_arr_all_right)):
                wheel_list_all_right.append(wheel_arr_all_right[i].ravel().tolist())

            wheel_arr_left = array(wheel_list_all_left)
            wheel_arr_right = array(wheel_list_all_right)
            wheel_arr_all = np_ap(wheel_arr_left, wheel_arr_right, axis=0)  #
            axle_no = int(wheel_arr_all.shape[0] / 2)
            wheel_data_count = wheel_arr_all.shape[1]
            wheel_arr_all_new = wheel_arr_all.reshape(
                (2, axle_no, wheel_data_count))  # shape=(2, 8, 3600) 2:两侧（0：左侧；1：右侧）8:轴数
            wheel_tran = transpose(wheel_arr_all_new, [1, 0, 2])
            wheel_tran_list = wheel_tran.tolist()

            # 计算每个车轮的横坐标（因为每个车轮的shape都一样，故计算一次）
            wheel_count = wheel_tran.shape[2]
            unit_interval = round(1 / frequency, 4)
            x_wheel = [round(unit_interval * x, 4) for x in range(wheel_count)]
    except Exception as e:
        info(e)
        print(e)
    return x_wheel, wheel_tran_list

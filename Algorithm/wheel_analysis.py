from numpy import array as np_array
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

        x_tensor, y_tensor, prediction = neural_network_module(x, ss)
    all_wheel_new_data = []
    for axle_data in all_wheel_data:
        pass

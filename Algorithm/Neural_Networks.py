from matplotlib import pyplot as plt, image as mp_img
from torch import unsqueeze, Tensor, optim
from torch.nn import functional as func, MSELoss, Linear, Module

from Algorithm import Image_extraction as Ie


class Net(Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = Linear(n_feature, n_hidden)
        self.predict = Linear(n_hidden, n_output)

    def forward(self, x_input):
        x_input = self.hidden(x_input)
        x_input = func.relu(x_input)
        x_input = self.predict(x_input)
        return x_input


def tensor_unsqueeze(x_list_, y_list_):
    x_tensor_ = unsqueeze(Tensor(x_list_), 1)
    y_tensor_ = unsqueeze(Tensor(y_list_), 1)
    return x_tensor_, y_tensor_


def optimizer_choose(net_, opt=None):
    lr = 0.05
    momentum = 0.7
    alpha = 0.9
    betas = (0.92, 0.99)

    if str(opt) == '1':
        print('SGD')
        optimizer_ = optim.SGD(net_.parameters(), lr=lr)
    elif str(opt) == '2':
        print('Momentum')
        optimizer_ = optim.SGD(net_.parameters(), lr=lr, momentum=momentum)
    elif str(opt) == '3':
        print('RMSprop')
        optimizer_ = optim.RMSprop(net_.parameters(), lr=lr, alpha=alpha)
    else:
        print('Adam')
        optimizer_ = optim.Adam(net_.parameters(), lr=lr, betas=betas)
    return optimizer_


def visualization(i, loss_, x_tensor_, y_tensor_, prediction_):
    if i % 100 == 0:
        print(i, float('%.6f' % loss_.data.numpy()))
        plt.cla()
        plt.grid()
        plt.scatter(x_tensor_.data.numpy(), y_tensor_.data.numpy())
        plt.plot(x_tensor_.data.numpy(), prediction_.data.numpy(), 'k-.', lw=3)
        # plt.text(0, -0.4, 'Loss=%.6f' % loss_.data.numpy(), fontdict={'size': 20, 'color': 'black'})
        plt.pause(0.05)


def train_neural_network(x_tensor_, y_tensor_, net_, optimizer_, loss_func_):
    prediction_ = None
    for i in range(35001):
        prediction_ = net_(x_tensor_)
        loss_ = loss_func_(prediction_, y_tensor_)
        optimizer_.zero_grad()
        loss_.backward()
        optimizer_.step()
        # 曲线拟合，可视化展示
        visualization(i, loss_, x_tensor_, y_tensor_, prediction_)
    return prediction_


def neural_network_module(x_list_, y_list_):
    # 将列表型的数据转换成tensor类型的数据
    x_tensor_, y_tensor_ = tensor_unsqueeze(x_list_, y_list_)

    # 建立神经网络
    net_ = Net(1, 100, 1)
    optimizer_ = optimizer_choose(net_, opt=None)
    loss_func_ = MSELoss()

    # 神经网络曲线拟合展示
    # plt.plot(x_list_, y_list_)
    plt.ion()

    # 使用神经网络进行训练
    prediction_ = train_neural_network(x_tensor_, y_tensor_, net_, optimizer_, loss_func_)

    plt.ioff()
    # plt.show()

    return x_tensor_, y_tensor_, prediction_


if __name__ == '__main__':
    # pic_path = getcwd()

    # pic_ = mp_img.imread('2020-11-19_163900.jpg')
    # pic_ = mp_img.imread('2020-11-19_165229.jpg')
    pic_ = mp_img.imread('2020-11-20_092529.jpg')
    # pic_ = mp_img.imread('pic4.jpg')
    # pic_ = mp_img.imread('Figure_1.jpg')

    pic_gray = Ie.gray_scale(pic_)
    xList, yList = Ie.extraction(pic_, 60)

    """
    # x_tensor = torch.unsqueeze(torch.Tensor(xList), 1)
    # y_tensor = torch.unsqueeze(torch.Tensor(yList), 1)
    x_tensor, y_tensor = tensor_unsqueeze(xList, yList)

    net = Net(1, 645, 1)
    # optimizer = torch.optim.SGD(net.parameters(), lr=0.05, momentum=0.7)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.05, betas=(0.9, 0.99))
    loss_func = torch.nn.MSELoss()

    # plt.figure()
    # plt.imshow(pic_)
    plt.plot(xList, yList)
    plt.ion()

    for t in range(10001):
        prediction = net(x_tensor)
        loss = loss_func(prediction, y_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if t % 100 == 0:
            print(t, float('%.6f' % loss.data.numpy()))
            plt.cla()
            plt.grid()
            plt.scatter(x_tensor.data.numpy(), y_tensor.data.numpy())
            plt.plot(x_tensor.data.numpy(), prediction.data.numpy(), 'k-.', lw=3)
            plt.text(0, -0.4, 'Loss=%.6f' % loss.data.numpy(), fontdict={'size': 20, 'color': 'black'})
            plt.pause(0.1)
    plt.ioff()
    plt.show()
    
    """
    x_tensor, y_tensor, prediction = neural_network_module(xList, yList)
    print('Done!')

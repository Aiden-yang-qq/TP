import matplotlib.pyplot as plt
import matplotlib.image as mp_img
import numpy as np
import torch
import torch.nn.functional as func


class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.predict = torch.nn.Linear(n_hidden, n_output)

    def forward(self, x_input):
        x_input = self.hidden(x_input)
        x_input = func.relu(x_input)
        x_input = self.predict(x_input)
        return x_input


def extraction(pic_):
    count = 0
    x_list = []
    y_list = []
    pic = np.swapaxes(pic_, 1, 0)
    shape_i = pic.shape[0]
    shape_j = pic.shape[1]
    for i in range(0, shape_i, 5):
        for j in range(shape_j):
            if pic[i][j][0] <= 10 and pic[i][j][1] <= 10 and pic[i][j][2] >= 245:
                count += 1
                x_list.append(i)
                y_list.append(-1 * j)
                # print(i, j)
                break
    return x_list, y_list


if __name__ == '__main__':
    pic_4 = mp_img.imread('pic4.jpg')
    plt.imshow(pic_4)
    plt.grid()
    plt.show()

    xList, yList = extraction(pic_4)
    plt.figure()
    plt.plot(xList, yList, '.')
    plt.grid()

    xTensor = torch.Tensor(xList)
    x = torch.unsqueeze(torch.Tensor(xList), 1)
    y = torch.unsqueeze(torch.Tensor(yList), 1)

    net = Net(1, 500, 1)
    # optimizer = torch.optim.SGD(net.parameters(), lr=0.05, momentum=0.7)
    # optimizer = torch.optim.RMSprop(net.parameters(), lr=0.1, alpha=0.9)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.1, betas=(0.9, 0.99))
    loss_func = torch.nn.MSELoss()

    plt.figure()
    plt.ion()

    for t in range(10001):
        prediction = net(x)
        loss = loss_func(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if t % 100 == 0:
            print(t, float('%.6f' % loss.data.numpy()))
            plt.cla()
            plt.grid()
            plt.scatter(x.data.numpy(), y.data.numpy())
            plt.plot(x.data.numpy(), prediction.data.numpy(), 'k-.', lw=3)
            plt.text(0, -0.4, 'Loss=%.6f' % loss.data.numpy(), fontdict={'size': 20, 'color': 'black'})
            plt.pause(0.1)
    plt.ioff()
    plt.show()

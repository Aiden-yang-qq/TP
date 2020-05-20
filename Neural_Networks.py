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


if __name__ == '__main__':
    import matplotlib.image as mp_img
    import matplotlib.pyplot as plt
    import Image_extraction as Ie
    import numpy as np

    # pic_ = mp_img.imread('pic4.jpg')
    pic_ = mp_img.imread('Figure_1.jpg')

    pic_gray = Ie.gray_scale(pic_)
    xList, yList = Ie.extraction(pic_, 60)

    x_tensor = torch.unsqueeze(torch.Tensor(xList), 1)
    y_tensor = torch.unsqueeze(torch.Tensor(yList), 1)

    net = Net(1, 645, 1)
    # optimizer = torch.optim.SGD(net.parameters(), lr=0.05, momentum=0.7)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.05, betas=(0.9, 0.99))
    loss_func = torch.nn.MSELoss()

    # plt.figure()
    plt.imshow(pic_)
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

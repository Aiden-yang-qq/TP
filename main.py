import torch
import matplotlib.image as mp_img
import matplotlib.pyplot as plt
import Image_extraction as Ie
import Neural_Networks as Neural

if __name__ == '__main__':
    pic_4 = mp_img.imread('pic4.jpg')
    xList, yList = Ie.extraction(pic_4)

    # plt.imshow(pic_4)
    # plt.grid()
    # plt.show()

    # plt.figure()
    # plt.plot(xList, yList, '.')
    # plt.grid()

    xTensor = torch.Tensor(xList)
    x = torch.unsqueeze(torch.Tensor(xList), 1)
    y = torch.unsqueeze(torch.Tensor(yList), 1)

    net = Neural.Net(1, 500, 1)
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

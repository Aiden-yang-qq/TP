# 将通信协议写成调用模块
import serial
import serial.tools.list_ports as lps
import time


class SerialRS485:
    def __init__(self, port, bps=115200, timeout=5):
        # 配置参数
        self.port = port  # 端口号
        self.bps = bps  # 波特率
        self.timeout = timeout  # 超时时间
        self.ser = serial.Serial(port, bps, timeout=timeout)  # 开启串口

    def port_open(self):
        if not self.ser.isOpen():
            self.ser.open()

    def port_close(self):
        self.ser.close()

    def port_read(self):
        received_all = ''
        if self.ser.isOpen():
            print('read串口已经打开')
            while True:
                # print('循环等待数据接收')
                count = self.ser.inWaiting()
                # print('count的类型', type(count))  # count的类型 <class 'int'>
                if count > 0:
                    print('接收到%d字节的数据' % count)
                    received_data = self.ser.read(count)
                    # print(type(received_data))
                    print('received_data:', received_data, type(received_data))
                    if received_data == b'exit':
                        print('--------------- 数据接收完毕 --------------- ')
                        self.port_close()
                        break
                    else:
                        received_all += str(received_data)
        return received_all


def check_ports():
    ports = []
    available_ports = []
    serial_ports = lps.comports()
    for p in serial_ports:
        ports.append(p.device)

    if len(ports) > 0:
        print(ports)
        for port in ports:
            try:
                main_ser = SerialRS485(port)
                available_ports.append(main_ser.ser.port)
                print('可用串口号：', main_ser.ser.port, '\t波特率：', main_ser.ser.baudrate)
            except Exception as e:
                print('异常：', e)
                err = e.args[0]
                if err[:19] == 'could not open port':
                    print('串口号：%s被占用' % err[21:25])
    return available_ports


def select_port(available_ports):
    send_ports = []
    if len(available_ports) >= 1:
        for ava_port in available_ports:
            if int(ava_port[3]) % 2 == 0:
                print('串口号：%s可以用来接收数据' % ava_port)
                send_ports.append(ava_port)
            else:
                print('串口号：%s应该用来发送数据' % ava_port)
    return send_ports


if __name__ == '__main__':
    ap = check_ports()  # 检测可用串口
    sp = select_port(ap)  # 选择串口进行数据接收
    if len(sp) >= 1:
        my_ser = SerialRS485(sp[0])
        rec_all = my_ser.port_read()
    else:
        print('无可用于接收数据的串口')

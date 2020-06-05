# 将通信协议写成调用模块
import serial
import serial.tools.list_ports as lps
import time


class SerialRS485:
    def __init__(self, port, bps=115200, timeout=0):
        # 配置参数
        self.port = port  # 端口号
        self.bps = bps  # 波特率
        self.timeout = timeout  # 超时时间
        self.ser = serial.Serial(port, bps, timeout=timeout)  # 开启串口
        self.set_buffer = serial.Serial.set_buffer_size(self.ser, rx_size=8192)  # 重新配置接收缓存大小

    def port_open(self):
        if not self.ser.is_open:
            self.__init__(self.port, self.bps, self.timeout)

    def port_close(self):
        self.ser.close()

    def port_read(self):
        count_all = 0
        received_all = b''
        if self.ser.is_open:
            print('--------------- 串口已经打开，等待接收数据 ---------------')
            while True:
                count = self.ser.in_waiting
                if count > 0:
                    received_data = self.ser.read(count)
                    if received_data == b'exit':
                        print('--------------- 共接收到%d字节的数据，数据已接收完毕，串口关闭 --------------- ' % count_all)
                        self.port_close()
                        break
                    else:

                        received_all += received_data
                        count_all += count
                        print('本次接收到%4d字节的数据，目前共计接收%g字节的数据' % (count, count_all))
        return received_all

    def reopen_read(self):
        self.port_open()
        print('该串口再次开启')
        self.port_read()


def check_ports():
    ports = []
    available_ports = []
    serial_ports = lps.comports()
    for p in serial_ports:
        ports.append(p.device)

    if len(ports) > 0:
        print('该设备有以下串口：', ports)
        print('--------------- 各个串口信息如下 ---------------')
        for port in ports:
            try:

                main_ser = SerialRS485(port)
                available_ports.append(main_ser.ser.port)
                print('%s串口可用，波特率为：%d' % (main_ser.ser.port, main_ser.ser.baudrate))
            except Exception as e:
                # print('异常：', e)
                err = e.args[0]
                if err[:19] == 'could not open port':
                    print('%s串口被占用' % err[21:25], '异常信息：', e)
    return available_ports


def select_port(available_ports):
    send_ports = []
    if len(available_ports) >= 1:
        for ava_port in available_ports:
            if int(ava_port[3]) % 2 == 0:
                print('%s串口可以用来接收数据' % ava_port)
                send_ports.append(ava_port)
            else:
                print('%s串口应该用来发送数据' % ava_port)
    return send_ports


def main():
    ap = check_ports()  # 检测可用串口
    sp = select_port(ap)  # 选择串口进行数据接收
    if len(sp) >= 1:
        my_ser = SerialRS485(sp[0])
        print('当前使用的串口为：%s' % my_ser.port)
        rec_all = my_ser.port_read()
        return rec_all
    else:
        print('无可用于接收数据的串口')


if __name__ == '__main__':
    ra = main()

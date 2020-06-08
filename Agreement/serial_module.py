# 将通信协议写成调用模块
import serial
import serial.tools.list_ports as lps
import time


class SerialRS485:
    def __init__(self, port, bps=115200, timeout=0):
        """
        串口初始化，配置参数
        :param port:端口号
        :param bps: 波特率
        :param timeout: 超时时间
        """
        self.port = port  # 端口号
        self.bps = bps  # 波特率
        self.timeout = timeout  # 超时时间
        self.ser = serial.Serial(port, bps, timeout=timeout)  # 开启串口
        self.set_buffer = serial.Serial.set_buffer_size(self.ser, rx_size=8192)  # 重新配置接收缓存大小

    def port_open(self):
        """
        打开串口
        """
        if not self.ser.is_open:
            self.__init__(self.port, self.bps, self.timeout)    # 这里我直接进行串口初始化，替代直接打开串口

    def port_close(self):
        self.ser.close()

    def port_read(self):
        """
        接收数据，即读串口
        :return: 接收到的数据
        """
        count_all = 0
        received_all = b''
        if self.ser.is_open:
            print('--------------- 串口已经打开，等待接收数据 ---------------')
            while True:
                count = self.ser.in_waiting
                if count > 0:
                    received_data = self.ser.read(count)
                    if received_data == b'exit':    # 串口调试助手是以“bytes”的类型发送的数据，所以做退出判定的时候要注意！
                        print('--------------- 共接收到%d字节的数据，数据已接收完毕，串口关闭 --------------- ' % count_all)
                        time.sleep(5)   # 延时5s关闭串口
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
    """
    检查设备中有无端口，以及各个端口是否能够使用
    :return: 可用端口
    """
    ports = []
    available_ports = []
    serial_ports = lps.comports()   # 系统端口的列表
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
                err = e.args[0]
                if err[:19] == 'could not open port':
                    print('%s串口被占用' % err[21:25], '异常信息：', e)
    return available_ports


def select_port(available_ports):
    """
    从可用端口中选择可以接收数据的端口
    :param available_ports: 可用端口（两种端口不混用）
    :return: 可用于接收数据的端口
    """
    rec_ports = []
    if len(available_ports) >= 1:
        for ava_port in available_ports:
            if int(ava_port[3]) % 2 == 0:
                print('%s串口可以用来接收数据' % ava_port)
                rec_ports.append(ava_port)
            else:
                print('%s串口应该用来发送数据' % ava_port)
    return rec_ports


def main():
    """
    串口通信主程序
    :return: 返回接收到的数据
    """
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
    main()

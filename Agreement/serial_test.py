import serial
import serial.tools.list_ports

# == 简单串口程序实现 ==
# try:
#     portx = 'COM1'  # 端口设定，windows上的COM3等
#     bps = 115200  # 波特率，标准：50，75，110，134，150，200，300，600，1200，1800，2400，4800，9600，19200，38400，57600，115200
#     timex = 5  # 超时设置，None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间（单位为秒）
#     ser = serial.Serial(portx, bps, timeout=timex)  # 打开串口并得到串口对象
#
#     result = ser.write("我是艾登".encode('gbk'))  # 写数据
#     print('写总字节数：', result)
#     ser.close()  # 关闭串口
# except Exception as e:
#     print('---异常---:', e)

# == 获取可用串口列表 ==
# port_list = list(serial.tools.list_ports.comports())
# print(port_list)
# if len(port_list) == 0:
#     print('无可用串口')
# else:
#     print('----以下串口可用----')
#     for i in range(0, len(port_list)):
#         print(port_list[i])

# == 十六进制处理 ==
# try:
#     portx = 'COM1'
#     bps = 115200
#     timex = None
#     ser = serial.Serial(portx, bps, timeout=timex)
#     print('串口详情参数：', ser)
#     result = ser.write(chr(0x06).encode('utf-8'))  # 十六进制的发送
#     print('写总字节数：', result)
#     print(ser.read().hex())  # 读一个字节
#     print('-------------------')
#     ser.close()
# except Exception as e:
#     print('---异常---：', e)

# == 其他细节补充 ==
# try:
#     portx = 'COM1'
#     bps = 115200
#     timex = 5
#     ser = serial.Serial(portx, bps, timeout=timex)
#     print('串口详情参数：', ser)
#     print(ser.port)  # 获取到当前打开的串口名
#     print(ser.baudrate)  # 获取波特率
#     result = ser.write('我是艾登'.encode('gbk'))
#     print('写总字节数：', result)
#     # 循环接收数据，此为死循环，可用线程实现
#     while True:
#         if ser.in_waiting:
#             str = ser.read(ser.in_waiting).decode('gbk')
#             if str == 'exit':
#                 break
#             else:
#                 print('收到数据', str)
#     print('-------------------')
#     ser.close()
# except Exception as e:
#     print('---异常---:', e)

# 部分封装
import threading

STRGLO = ''  # 读取的数据
BOOL = True  # 读取标志位


# 读取代码本体实现
def ReadData(ser):
    """
    读取代码本体实现
    :param ser:
    :return:
    """
    global STRGLO, BOOL
    # 循环接受数据，此为死循环，可用线程实现
    while BOOL:
        if ser.in_waiting:
            STRGLO = ser.read(ser.in_waiting).decode('gbk')
            print(STRGLO)


def DOpenPort(portx, bps, timeout):
    """
    打开串口，超时设置，None：永远等待操作，0：立即返回请求结果，其他值：等待超时时间（单位：秒）
    :param portx:
    :param bps:
    :param timeout:
    :return:
    """
    ret = False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
        # 判断是否打开成功
        if ser.is_open:
            ret = True
            threading.Thread(target=ReadData, args=(ser,)).start()
        return ser, ret
    except Exception as e:
        print('---异常---:', e)


def DClosePort(ser):
    """
    关闭串口
    :param ser:
    :return:
    """
    global BOOL
    BOOL = False
    ser.close()


def DWritePort(ser, text):
    """
    写数据
    :param ser:
    :param text:
    :return:
    """
    result = ser.write(text.encode('gbk'))
    return result


def DReadPort():
    global STRGLO
    str = STRGLO
    STRGLO = ''  # 清空当次读取
    return str


if __name__ == '__main__':
    ser, ret = DOpenPort('COM1', 115200, None)
    if ret:  # 判断串口是否成功打开
        count = DWritePort(ser, '我是艾登')
        print('写入字节数：', count)
        DReadPort()  # 读取串口数据
        DClosePort(ser)  # 关闭串口

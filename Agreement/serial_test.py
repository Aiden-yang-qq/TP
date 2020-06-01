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
try:
    portx = 'COM1'
    bps = 115200
    timex = None
    ser = serial.Serial(portx, bps, timeout=timex)
    print('串口详情参数：', ser)

    result = ser.write(chr(0x06).encode('utf-8'))  # 十六进制的发送
    print('写总字节数：', result)

    print(ser.read().hex())  # 读一个字节

    print('-------------------')
    ser.close()

except Exception as e:
    print('---异常---：', e)

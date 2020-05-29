#!/usr/bin/python3
# File name:server.py
import socket
import numpy as np
# import time
import os
import sys
import math


def progressbar(cur, total):
    """
    服务器端文件传输进度条和百分比显示
    :param cur: 当前已经传输的数据量
    :param total: 需要传输的数据总量
    :return: 系统自动刷新，无需return
    """
    percent = '{:.2%}'.format(cur / total)
    sys.stdout.write('\r')
    sys.stdout.write('[%-80s] %s' % ('=' * int(math.floor(cur * 80 / total)), percent))
    sys.stdout.flush()
    if cur == total:
        sys.stdout.write('\n')


def replace(string=None, old_word='\\t', new_word=' '):
    """
    字符串特殊符号替换
    :param string:   待去除特殊符号的字符串
    :param old_word: 需要去除的符号
    :param new_word: 用于替换的符号，这里使用的是空格
    :return:         返回已经去除特殊符号后的字符串
    """
    string = string.replace(old_word, new_word)
    string = string.replace('\', b\'', '')
    string = string.replace('[b\'', '')
    string = string.replace('\\r\\n\\r\\n\']', '')
    string = string.replace('\\r\\n\']', '')
    string = string.replace('\' b\'', '')
    string = string.replace('\']', '')
    return string


def transform(data_total):
    """
    数据转换
    :param data_total:  待转换的数据，原数据类型为bytes
    :return:            转换后的数据，其类型为字符串str类型
    """
    data_total_array = np.array(data_total)         # 将“bytes”类型的数据转换成“ndarray”类型的数组矩阵
    data_total_list = data_total_array.tolist()     # 将“ndarray”类型的数组矩阵转换成列表list
    data_total_str = str(data_total_list)           # 将列表转换成字符串
    data_total_string = replace(data_total_str)     # 使用函数replace将字符串中的无用符号进行剔除
    return data_total_string


if __name__ == '__main__':
    s = socket.socket()
    s.bind(('192.168.10.112', 9990))
    s.listen(5)
    print('\nWaiting for connection ...')
    while True:
        conn, addr = s.accept()
        print("\nConnection Successfully!\n"
              "\nAccept connect from %s:%s\n" % addr)       # 服务器端显示“已连接”
        conn.send(b'Connection Successfully!')              # 返回给客户端消息，显示“已连接成功！”

        file_size = os.path.getsize('./20190613-10-11-00-data.txt')     # 获取已知接收文件的大小
        print('需要接收的文件大小: %.2f KB' % (file_size / 1024))
        data_total = []
        data_total = np.array(data_total)
        print('\nDownloading, Waiting for a moment ...\n')
        data_total_string_count = 0
        while True:
            size = data_total_string_count
            progressbar(size, file_size)                    # 设置进度条和百分比显示
            data = conn.recv(8192)
            if not data or data.decode('utf-8') == 'exit':
                conn.send(b'The data is invalid, resend please!')   # 数据无效，请重新发送
                print('\n客户端发送的数据无效，已请求客户端重新发送数据！\n')
                break
            else:
                data_total = np.append(data_total, data)    # 将服务器每次接收到的数据进行数据拼接
                data_total_string = transform(data_total)   # 调用transform函数进行数据格式的转换
                data_total_count = len(data_total)
                data_total_string_count = len(data_total_string)
                str_count_float = float('%.2f' % (data_total_string_count / 1024))
                mark_num = '**'                             # 数据接收完成标识
                mark_res = data_total_string.find(mark_num)
                if mark_res == -1:                          # find函数：找不到指定内容则返回“-1”
                    continue
                else:
                    file_data = open('data_string.txt', 'w')
                    data_total_string = data_total_string.strip(' **')
                    file_data.write(data_total_string)
                    file_data.close()
                    conn.send(b'The server receives %d packets in total, \r\nand total data volume is %.2f KB.\n '
                              b' ---------------- Transfer Completed! ---------------- '
                              % (data_total_count, str_count_float))        # 给客户端发送“数据传输完成”信息
                    break
        progressbar(data_total_string_count, file_size)
        print('\n\r\n服务器累计接收 %s 次数据包，总数据量共 %.2f KB' % (data_total_count, str_count_float))
        print('\n数据已传输完成并已保存至电脑！')
        print('\n客户端已断开连接！')
        conn.close()

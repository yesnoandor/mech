#! /home/wenyu/anaconda3/bin/python3
# -*- coding: utf-8 -*-


"""
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---=' 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
         佛祖保佑       永无BUG 

'''
  

Created on 


@author: wenyu_xu
@mail:wenyu__xu@163.com




"""

import time
from utils import const
import datetime
import socket
import json
import random
from utils.bytes import *
from protocol.ModuleProtocol import ModuleProtocol
from simu.simu_build_protocol import build_heart_beat_bin
from simu.simu_build_protocol import build_system_info_bin
from simu.simu_build_protocol import build_event_info_bin


def simu_device_client(conn):
    start_time = datetime.datetime.now()

    rtc_protocol = ModuleProtocol()
    while True:
         data = client.recv(1024)
         # print(type(data))
         # print_bytes(data)
         ret = rtc_protocol.parse_data(data)
         if ret == const.RTC_SYNC:
             break

    random_index = [build_heart_beat_bin, build_system_info_bin, build_event_info_bin, build_event_info_bin]

    serial_id = bytearray([0x31, 0x32, 0x33, 0x22, 0x36, 0x37])
    module_protocol = ModuleProtocol(serial_id=serial_id)

    while True:
        func = random.choice(random_index)
        if func is build_system_info_bin:
            bin = func(module_protocol, start_time)
        else:
            bin = func(module_protocol)
        # bin = build_heart_beat_bin(module_protocol)
        # bin = build_system_info_bin(module_protocol)
        # bin = build_event_info_bin(module_protocol)
        print(type(bin))
        #bin = random_function()
        print(bin)
        conn.send(bin)
        time.sleep(5)

        bin = build_heart_beat_bin(module_protocol)
        conn.send(bin)
        time.sleep(0.02)


if __name__ == '__main__':
    client = socket.socket()  # 默认是AF_INET、SOCK_STREAM
    client.connect(("localhost", 9999))

    simu_device_client(client)

    client.close()
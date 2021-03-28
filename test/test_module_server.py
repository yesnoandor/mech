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
import json
import datetime
import socket
import random
from utils.bytes import *
from protocol.ModuleProtocol import ModuleProtocol


def test_heart_beat_client(conn):
    heart_beat = "7e 01 00 00 00 20 01 00 00 00 00 00 00 00 00 00 00 c7 74 7e"

    heart_beat_bin = hexStringTobytes(heart_beat)
    print(heart_beat_bin)
    print_bytes(heart_beat_bin)

    while True:
        conn.send(heart_beat_bin)
        time.sleep(random.randint(1, 12))


def test_event_client(conn):
    event = [
        "7e 02 00 51 00 20 01 00 00 00 00 00 00 01 00 00 00 7b 22 65 76 65 6e 74 22 3a 5b 7b 22 64" \
        "61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 35 22 2c 22 6d 6f 64 22 3a 22 45" \
        "4d 43 5f 4d 4f 44 5f 4d 43 55 5f 43 41 4e 35 22 2c 22 69 6e 66 6f 22 3a 22 53 54 41 54 55" \
        "53 5f 4f 4b 22 7d 01 5d 7d 01 6e 7a 7e",
        "7e 02 00 51 00 20 01 00 00 00 00 00 00 03 00 00 00 7b 22 65 76 65 6e 74 22 3a 5b 7b 22 64" \
        "61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 35 22 2c 22 6d 6f 64 22 3a 22 45" \
        "4d 43 5f 4d 4f 44 5f 4d 43 55 5f 43 41 4e 32 22 2c 22 69 6e 66 6f 22 3a 22 53 54 41 54 55" \
        "53 5f 4f 4b 22 7d 01 5d 7d 01 79 e5 7e",
        "7e 02 00 51 00 20 01 00 00 00 00 00 00 03 00 00 00 7b 22 65 76 65 6e 74 22 3a 5b 7b 22 64" \
        "61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 35 22 2c 22 6d 6f 64 22 3a 22 45" \
        "4d 43 5f 4d 4f 44 5f 4d 43 55 5f 43 41 4e 32 22 2c 22 69 6e 66 6f 22 3a 22 53 54 41 54 55" \
        "53 5f 4f 4b 22 7d 01 5d 7d 01 79 e5 7e",
        "7e 02 00 79 02 20 01 00 00 00 00 00 00 05 00 00 00 7b 22 65 76 65 6e 74 22 3a 5b 7b 22 64" \
        "61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22 45" \
        "4d 43 5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 30 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44 43" \
        "5f 43 48 5f 56 42 41 54 5f 4d 4f 4e 3a 31 2e 31 30 34 20 76 2c 22 7d 01 2c 7b 22 64 61 74" \
        "65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22 45 4d 43" \
        "5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 31 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44 43 5f 43" \
        "48 5f 50 38 56 30 5f 43 41 4d 5f 4d 4f 4e 3a 33 2e 39 39 36 20 76 2c 22 7d 01 2c 7b 22 64" \
        "61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22 45" \
        "4d 43 5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 32 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44 43" \
        "5f 43 48 5f 52 45 46 5f 4d 4f 4e 5f 47 30 3a 33 2e 33 30 38 20 76 2c 22 7d 01 2c 7b 22 64" \
        "61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22 45" \
        "4d 43 5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 33 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44 43" \
        "5f 43 48 5f 50 35 56 30 5f 4d 4f 4e 3a 32 2e 35 30 34 20 76 2c 22 7d 01 2c 7b 22 64 61 74" \
        "65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22 45 4d 43" \
        "5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 34 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44 43 5f 43" \
        "48 5f 50 33 56 33 41 5f 4d 43 55 5f 4d 4f 4e 3a 33 2e 32 39 34 20 76 2c 22 7d 01 2c 7b 22" \
        "64 61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22" \
        "45 4d 43 5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 35 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44" \
        "43 5f 43 48 5f 52 45 46 5f 4d 4f 4e 5f 47 31 3a 33 2e 33 30 38 20 76 2c 22 7d 01 2c 7b 22" \
        "64 61 74 65 22 3a 22 32 30 32 30 30 37 30 31 30 30 30 30 33 36 22 2c 22 6d 6f 64 22 3a 22" \
        "45 4d 43 5f 4d 4f 44 5f 4d 43 55 5f 41 44 43 36 22 2c 22 69 6e 66 6f 22 3a 22 45 56 41 44" \
        "43 5f 43 48 5f 50 31 56 30 5f 4d 4f 4e 3a 30 2e 39 39 36 20 76 2c 22 7d 01 5d 7d 01 84 fa" \
        "7e"
    ]

    random_index = [0, 1, 2, 3]

    while True:
        index = random.choice(random_index)
        print("index = ", index)
        event_bin = hexStringTobytes(event[index])
        print_bytes(event_bin)
        conn.send(event_bin)
        time.sleep(5)


def test_rtc_sync_bin(conn):
    while True:
        data = client.recv(1024)
        print(type(data))
        print_bytes(data)

        #module_protocol = ModuleProtocol()
        #module_protocol.parse_data(data)


if __name__ == '__main__':
    client = socket.socket()  # 默认是AF_INET、SOCK_STREAM
    client.connect(("localhost", 9999))

    # test_heart_beat_client(client)
    # test_event_client(client)
    test_rtc_sync_bin(client)

    client.close()

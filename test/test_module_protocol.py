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

import os
import threading
from ui.MechIIViewer import MechIIViewer
from protocol.ModuleProtocol import *


def test_heart_beat_protocol():
    heart_beat = "7e 01 00 00 00 20 01 00 00 00 00 00 00 00 00 00 00 c7 74 7e"
    heart_beat_bin = hexStringTobytes(heart_beat)
    print(heart_beat_bin)
    print_bytes(heart_beat_bin)
    module_protocol = ModuleProtocol()
    module_protocol.parse_data(heart_beat_bin)


def test_module_event_protocol():
    module_event = "7e 02 00 45 00 20 01 00 00 00 00 00 00 02 00 00 00 7b 22 65 76 65 6e 74" \
                   "22 3a 7b 22 64 61 74 65 22 3a 22 32 30 31 39 30 32 31 36 30 39 32 38 31" \
                   "35 22 2c 22 6d 6f 64 22 3a 22 43 43 43 22 2c 22 77 61 72 6e 69 6e 67 22" \
                   "3a 22 49 4d 55 5f 45 52 52 4f 52 22 7d 01 7d 01 34 24 7e "
    module_event_bin = hexStringTobytes(module_event)
    print(module_event_bin)
    print_bytes(module_event_bin)
    module_protocol = ModuleProtocol()
    module_protocol.parse_data(event_bin)



def test_system_info_protocol():
    cmd = {"system":
                {"version":
                    {"sw": "1.0",
                     "hw": "2.0"
                    },
                 "temperature": "56.4",
                 "cpu":
                     {"cpu0": "78",
                      "cpu1": "29",
                      "cpu2": "100",
                      "cpu3": "84",
                      "cpu4": "37",
                      "cpu5": "56",
                      "cpu6": "82",
                      "cpu7": "67",
                     },
                 "memory":
                     {"total": "2048M",
                      "used": "1024M"
                     },
                 "network": "86",
                }
            }
    print(cmd)
    jsoninfo = json.dumps(cmd)
    print(type(jsoninfo))
    print(jsoninfo)
    body = jsoninfo.encode("utf-8")
    print(body)

    serial_id = bytearray([0x31, 0x32, 0x33, 0x22, 0x36, 0x37])

    module_protocol = ModuleProtocol()
    header = module_protocol.build_header(const.SYSTEM_INFO_UPLOAD, len(body), serial_id=serial_id)
    system_info_bin = module_protocol.build_bin(header, body)
    print_bytes(system_info_bin)

    module_protocol.parse_data(system_info_bin)
    pass


def test_rtc_sync_protocol():
    module_rtc_sync = "7e 04 80 61 00 20 01 00 00 00 00 00 00 00 00 00 00 7b 22 53 65 74 74 69" \
                      "6e 67 22 3a 20 7b 22 4d 4f 44 5f 52 54 43 22 3a 20 7b 22 79 65 61 72 22" \
                      "3a 20 32 30 32 31 2c 20 22 6d 6f 6e 74 68 22 3a 20 32 2c 20 22 64 61 79" \
                      "22 3a 20 31 34 2c 20 22 68 6f 75 72 22 3a 20 32 31 2c 20 22 6d 69 6e 22" \
                      "3a 20 32 31 2c 20 22 73 65 63 22 3a 20 32 37 7d 01 7d 01 7d 01 8f 0b 7e"
    module_rtc_sync_bin = hexStringTobytes(module_rtc_sync)
    print(module_rtc_sync_bin)
    print_bytes(module_rtc_sync_bin)
    module_protocol = ModuleProtocol()
    module_protocol.parse_data(module_rtc_sync_bin)


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")
    # 返回当前工作目录
    print(os.getcwd())


    '''
    devices_info = {'1111': ['2222', '3333'], '1112': ['4444', '5555'], '1113': ['6666', '7777']}
    # devices_info = {'1111': ['2222', '3333'], '1112': ['4444', '5555']}
    # devices_info = {'1111': ['2222', '3333']}
    focus_device = '1111'
    focus_node = '2222'

    app = wx.App()
    frame = MechIIViewer(devices_info=devices_info,
                         focus_device=focus_device,
                         focus_node=focus_node,
                         parent=None, title='Mech-II', name="DemoFrame", style=wx.DEFAULT_FRAME_STYLE,
                         size=(1920, 1080))
    frame.Center()
    frame.Show()

    thread = threading.Thread(target=test_system_info_protocol)
    thread.start()

    app.MainLoop()
    '''

    test_heart_beat_protocol()
    # test_module_event_protocol()
    # test_system_info_protocol()
    # test_rtc_sync_protocol()
    pass

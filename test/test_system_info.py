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
import time
import wx
import threading
import random
from pubsub import pub
from ui.MechIIViewer import MechIIViewer


def test_system_info():
    system_info = {}
    while True:
        # 模拟系统信息 --------------------

        # 模拟 CPU 占用率
        cpu_utilization = []
        for i in range(8):
            # 随机产生8个0-100浮点数，作为CPU占有率
            cpu_utilization.append(random.uniform(0, 100))
        print(cpu_utilization)

        # 模拟 MEMORY 占用率
        memory_utilization = ['64M', '128M', '256M', '512M', '1024M', '1280M', '1408M', '1536M', '2048M']

        # 模拟网速
        network_speed = 60.0 + random.uniform(0, 20)

        # 填充模拟系统信息
        system_info['version'] = {'sw': '2.3', 'hw': '1.0'}
        system_info['temperature'] = '37.9'
        system_info['cpu'] = {'cpu0': str(cpu_utilization[0]), 'cpu1': str(cpu_utilization[1]), 'cpu2': str(cpu_utilization[2]), 'cpu3': str(cpu_utilization[3]),
                              'cpu4': str(cpu_utilization[4]), 'cpu5': str(cpu_utilization[5]), 'cpu6': str(cpu_utilization[6]), 'cpu7': str(cpu_utilization[7])}
        system_info['memory'] = {'total': '2048M', 'used': random.choice(memory_utilization)}
        system_info['network'] = str(network_speed)
        wx.CallAfter(pub.sendMessage, 'system_info_event', info=system_info)

        # 模拟心跳
        mode = True
        wx.CallAfter(pub.sendMessage, 'heart_beat_event', mode=mode)

        time.sleep(5.0)


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")
    # 返回当前工作目录
    print(os.getcwd())

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

    thread = threading.Thread(target=test_system_info)
    thread.start()

    app.MainLoop()

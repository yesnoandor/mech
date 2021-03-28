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
from random import choice
from pubsub import pub
from ui.MechIIViewer import MechIIViewer


def test_heart_beat():
    while True:
        foo = [True, False]
        mode = choice(foo)
        wx.CallAfter(pub.sendMessage, 'heart_beat_event', mode=mode)
        time.sleep(10.0)


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

    thread = threading.Thread(target=test_heart_beat)
    thread.start()

    app.MainLoop()




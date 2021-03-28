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


import wx
from hw.devices import DevicesInfo
from ui.MechIIViewer import MechIIViewer
from ui.SplashViewer import SplashViewer


class FrameManager:
    """
    管理多个Frame的创建以及切换
    """
    def __init__(self, UpdateFrame):
        self.UpdateFrame = UpdateFrame
        self.frameDict = {}         # 用来装载已经创建的Frame对象

    def GetFrame(self, index):
        frame = self.frameDict.get(index)

        if frame is None:
            frame = self.CreateFrame(index)
            self.frameDict[index] = frame

        # print(frame)
        # print(self.frameDict)
        return frame

    def CreateFrame(self, index):
        frame = None
        if index == 0:
            frame = SplashViewer(UpdateFrame=self.UpdateFrame,
                                parent=None,
                                title='Mech-II',
                                name="Start Frame",
                                style=wx.DEFAULT_FRAME_STYLE,
                                size=(1920, 1080))

        elif index == 1:
            devices_info = DevicesInfo()
            devices_info = devices_info.get_devices_name()
            focus_device = list(devices_info.keys())[0]
            focus_node = devices_info[focus_device][0]

            frame = MechIIViewer(devices_info=devices_info,
                                 focus_device=focus_device,
                                 focus_node=focus_node,
                                 UpdateFrame=self.UpdateFrame,
                                 parent=None,
                                 title='Mech-II',
                                 name="Mech-II Frame",
                                 style=wx.DEFAULT_FRAME_STYLE,
                                 size=(1920, 1080))

        return frame


if __name__ == '__main__':
    pass

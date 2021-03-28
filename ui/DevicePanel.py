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
from ui.MechIIEvent import *


class DevicePanel(wx.Panel):
    """
    单个设备信息
    """
    def __init__(self, name, focus, status, *args, **kwargs):
        super(DevicePanel, self).__init__(*args, **kwargs)

        self.name = name        # 当前Device信息名称
        self.focus = focus      # 当前Device信息处于聚焦背景色状态与否
        self.status = status    # 当前Device信息处于折叠状态还是打开状态

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        # 箭头图标
        if self.status:
            self.arrow_image = wx.StaticBitmap(parent=self,
                                               id=wx.ID_ANY,
                                               bitmap=wx.Bitmap('res//Device-arrow-white-up.png'),
                                               size=(30, 56))
        else:
            self.arrow_image = wx.StaticBitmap(parent=self,
                                               id=wx.ID_ANY,
                                               bitmap=wx.Bitmap('res//Device-arrow-white-down.png'),
                                               size=(30, 56))
        self.sizer.Add(self.arrow_image, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)

        # 设备图标
        self.device_image = wx.StaticBitmap(parent=self,
                                            id=wx.ID_ANY,
                                            bitmap=wx.Bitmap('res//Device-icon-white.png'),
                                            size=(30, 56))
        self.sizer.Add(self.device_image, proportion=1, flag=wx.ALIGN_CENTER | wx.LEFT, border=8)

        # 设备名
        label = "Device-"+name
        self.device_name = wx.StaticText(parent=self, id=wx.ID_ANY, label=label, style=wx.ALIGN_RIGHT, size=(30, 30))
        self.device_name.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))

        self.sizer.Add(self.device_name, proportion=2, flag=wx.ALIGN_CENTER | wx.ALL, border=0)

        # 绑定双击事件
        self.arrow_image.Bind(wx.EVT_LEFT_DCLICK, self.OnArrayImageDoubleClicked)
        self.device_image.Bind(wx.EVT_LEFT_DCLICK, self.OnDeviceImageDoubleClicked)
        self.device_name.Bind(wx.EVT_LEFT_DCLICK, self.OnDeviceNameDoubleClicked)

        pass

    def OnArrayImageDoubleClicked(self, event):
        """
        双击Item的事件处理
        :param event:
        :return:
        """
        # 向Device信息区域发送选中Node的信息
        evt = DeviceEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().device_info_panel, evt)

    def OnDeviceImageDoubleClicked(self, event):
        """
        双击Item的事件处理
        :param event:
        :return:
        """
        # 向Device信息区域发送选中Node的信息
        evt = DeviceEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().device_info_panel, evt)

    def OnDeviceNameDoubleClicked(self, event):
        """
        双击Item的事件处理
        :param event:
        :return:
        """
        print("double click OnDeviceName")

        # 向Device信息区域发送选中Node的信息
        evt = DeviceEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().device_info_panel, evt)


if __name__ == '__main__':
    pass

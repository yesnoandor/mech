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


class NodePanel(wx.Panel):
    """
    设备信息区域节点面板
    """
    def __init__(self, name, focus, *args, **kwargs):
        super(NodePanel, self).__init__(*args, **kwargs)

        self.name = name

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        # label = "Node-" + self.name
        label = self.name
        self.node_name = wx.StaticText(parent=self, id=wx.ID_ANY,  size=(248, -1), label=label, style=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL)
        self.node_name.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.node_name, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)


        #self.device_name = wx.StaticText(parent=self, id=wx.ID_ANY, label="Device-1234", style=wx.ALIGN_CENTER)
        #self.device_name.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        #self.sizer.Add(self.device_name, proportion=2, flag=wx.ALIGN_CENTER, border=5)

        # self.sizer.Add(self.device_name, proportion=2, flag=wx.EXPAND | wx.ALL, border=5)

        '''
        if focus:
            self.SetBackgroundColour((0xfe, 0xd3, 0x63))
            self.SetForegroundColour("BLACK")
        else:
            self.SetBackgroundColour("GREY")
            self.SetForegroundColour((250, 255, 255))
        '''

        self.node_name.Bind(wx.EVT_LEFT_DCLICK, self.OnNodeDoubleClicked)
        pass

    def OnNodeDoubleClicked(self, event):
        """
        双击Node的事件处理
        :param event:
        :return:
        """

        # 向Device信息区域, 发送选中Node的信息
        evt = NodeEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().device_info_panel, evt)

        # 向Chart图表区域, 发送选中Node的信息
        evt = NodeEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().chart_panel, evt)

        # 向ModuleList信息区域，发送选中Node的信息
        evt = NodeEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().module_panel.list, evt)

        # 向Tab信息区域发送选中Node的信息
        evt = NodeTabEvent(
            name=self.name,
        )
        wx.QueueEvent(wx.GetApp().GetTopWindow().tab_info_panel, evt)


if __name__ == '__main__':
    pass

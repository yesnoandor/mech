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


class NodeInfoPanel(wx.Panel):
    """

    """
    def __init__(self, *args, **kwargs):
        super(NodeInfoPanel, self).__init__(*args, **kwargs)

        self.sizer = wx.GridBagSizer(0, 0)
        self.SetSizer(self.sizer)

        self.uuid = wx.StaticText(parent=self, id=wx.ID_ANY, label="Device UUID : 1234567812345678",
                                  style=wx.ALIGN_LEFT)
        self.uuid.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.uuid, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=15)

        self.ip = wx.StaticText(parent=self, id=wx.ID_ANY, label="IP : 192.168.1.127", style=wx.ALIGN_LEFT)
        self.ip.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.ip, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=15)

        self.hw_version = wx.StaticText(parent=self, id=wx.ID_ANY, label="HW Version : V1.0", style=wx.ALIGN_LEFT)
        self.hw_version.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.hw_version, pos=(0, 2), flag=wx.EXPAND | wx.ALL, border=15)

        self.sw_version = wx.StaticText(parent=self, id=wx.ID_ANY, label="SW Version : V1.0", style=wx.ALIGN_LEFT)
        self.sw_version.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.sw_version, pos=(0, 3), flag=wx.EXPAND | wx.ALL, border=15)

        self.Bind(EVT_NODE_INFO, self.OnNodeInfoEvent)

        '''
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        self.uuid = wx.StaticText(parent=self, id=wx.ID_ANY, label="Device UUID : 1234567812345678", style=wx.ALIGN_LEFT)
        self.uuid.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.uuid, proportion=1, flag=wx.LEFT | wx.TOP, border=10)

        self.ip = wx.StaticText(parent=self, id=wx.ID_ANY, label="IP : 192.168.1.127", style=wx.ALIGN_LEFT)
        self.ip.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.ip, proportion=1, flag=wx.TOP, border=10)

        self.hw_version = wx.StaticText(parent=self, id=wx.ID_ANY, label="HW Version : V1.0", style=wx.ALIGN_LEFT)
        self.hw_version.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.hw_version, proportion=1, flag=wx.TOP, border=10)

        self.sw_version = wx.StaticText(parent=self, id=wx.ID_ANY, label="SW Version : V1.0", style=wx.ALIGN_LEFT)
        self.sw_version.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.sw_version, proportion=1, flag=wx.TOP, border=10)
        '''

    def OnNodeInfoEvent(self, evt):
        print("hw = ", evt.hw)
        print("sw = ", evt.sw)
        print("ip = ", evt.ip)
        print("uuid = ", evt.uuid)

        label = "HW Version : V%s" % evt.hw
        self.hw_version.SetLabelText(label)
        label = "SW Version : V%s" % evt.sw
        self.sw_version.SetLabelText(label)
        label = "IP : %s" % evt.ip
        self.ip.SetLabelText(label)
        label = "Device UUID : %s" % evt.uuid
        self.uuid.SetLabelText(label)
        pass


class PerformanceInfoPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(PerformanceInfoPanel, self).__init__(*args, **kwargs)

        self.sizer = wx.GridBagSizer(0, 0)
        self.SetSizer(self.sizer)

        self.uptime_title = wx.StaticText(parent=self, id=wx.ID_ANY, label="Up Time", size=(300, 30),
                                          style=wx.ALIGN_CENTER)
        self.uptime_title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.uptime_title.SetBackgroundColour("Grey")
        self.uptime_title.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.uptime_title, pos=(0, 0), flag=wx.EXPAND | wx.LEFT, border=10)

        self.uptime_value = wx.StaticText(parent=self, id=wx.ID_ANY, label="0:00:00:000", size=(300, 62),
                                          style=wx.ALIGN_CENTER)
        self.uptime_value.SetFont(wx.Font(32, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.uptime_value.SetBackgroundColour("GREY")
        self.uptime_value.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.uptime_value, pos=(1, 0), flag=wx.EXPAND | wx.LEFT, border=10)

        self.temperature_title = wx.StaticText(parent=self, id=wx.ID_ANY, label="Device Temperature", size=(300, 30),
                                               style=wx.ALIGN_CENTER)
        self.temperature_title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.temperature_title.SetBackgroundColour("GREY")
        self.temperature_title.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.temperature_title, pos=(0, 1), flag=wx.EXPAND | wx.LEFT, border=10)

        self.temperature_value = wx.StaticText(parent=self, id=wx.ID_ANY, label="30.0 ℃", size=(300, 62),
                                               style=wx.ALIGN_CENTER)
        self.temperature_value.SetFont(wx.Font(32, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.temperature_value.SetBackgroundColour("GREY")
        self.temperature_value.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.temperature_value, pos=(1, 1), flag=wx.EXPAND | wx.LEFT, border=10)

        self.memory_title = wx.StaticText(parent=self, id=wx.ID_ANY, label="Memory", size=(300, 40),
                                          style=wx.ALIGN_CENTER)
        self.memory_title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.memory_title.SetBackgroundColour("GREY")
        self.memory_title.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.memory_title, pos=(0, 2), flag=wx.EXPAND | wx.LEFT, border=10)

        self.memory_value = wx.StaticText(parent=self, id=wx.ID_ANY, label="28%", size=(300, 62), style=wx.ALIGN_CENTER)
        self.memory_value.SetFont(wx.Font(32, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.memory_value.SetBackgroundColour("GREY")
        self.memory_value.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.memory_value, pos=(1, 2), flag=wx.EXPAND | wx.LEFT, border=10)

        self.network_title = wx.StaticText(parent=self, id=wx.ID_ANY, label="Network Speed", size=(300, 30),
                                           style=wx.ALIGN_CENTER)
        self.network_title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.network_title.SetBackgroundColour("GREY")
        self.network_title.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.network_title, pos=(0, 3), flag=wx.EXPAND | wx.LEFT, border=10)

        self.network_value = wx.StaticText(parent=self, id=wx.ID_ANY, label="16Kbps", size=(300, 62),
                                           style=wx.ALIGN_CENTER)
        self.network_value.SetFont(wx.Font(32, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.network_value.SetBackgroundColour("GREY")
        self.network_value.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.network_value, pos=(1, 3), flag=wx.EXPAND | wx.LEFT, border=10)

        self.cpu_title = wx.StaticText(parent=self, id=wx.ID_ANY, label="CPU", size=(300, 30),
                                       style=wx.ALIGN_CENTER)
        self.cpu_title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.cpu_title.SetBackgroundColour("GREY")
        self.cpu_title.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.cpu_title, pos=(0, 4), flag=wx.EXPAND | wx.LEFT, border=10)

        self.cpu_value = wx.StaticText(parent=self, id=wx.ID_ANY, label="8", size=(300, 62),
                                       style=wx.ALIGN_CENTER)
        self.cpu_value.SetFont(wx.Font(32, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.cpu_value.SetBackgroundColour("GREY")
        self.cpu_value.SetForegroundColour((255, 255, 255))
        self.sizer.Add(self.cpu_value, pos=(1, 4), flag=wx.EXPAND | wx.LEFT, border=10)

        self.Bind(EVT_PERFORMANCE_INFO, self.OnPerformanceInfoEvent)

    def OnPerformanceInfoEvent(self, evt):
        print("uptime = ", evt.uptime)
        print("temperature = ", evt.temperature)
        print("memory = ", evt.memory)
        print("network total = ", evt.network)
        print("cpu = ", evt.cpu)

        self.uptime_value.SetLabelText(evt.uptime)
        label = "%s ℃" % evt.temperature
        self.temperature_value.SetLabelText(label)
        label = "%s%%" % evt.memory
        print("memory = ", label)
        self.memory_value.SetLabelText(label)
        label = "%sBps" % evt.network
        print("network total = ", label)
        self.network_value.SetLabelText(label)
        label = "%s" % evt.cpu
        self.cpu_value.SetLabelText(label)


class SystemInfoPanel(wx.Panel):
    """
    显示图表信息的面板
    """
    def __init__(self, *args, **kwargs):
        super(SystemInfoPanel, self).__init__(*args, **kwargs)

        # 创建二维网格 wx.GridBagSizer, 列间隔为0，行间隔为0
        self.sizer = wx.GridBagSizer(0, 0)
        self.SetSizer(self.sizer)

        self.node_info = NodeInfoPanel(self)
        self.sizer.Add(self.node_info, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=0)

        self.performance_info = PerformanceInfoPanel(self)
        self.sizer.Add(self.performance_info, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=0)

        self.SetBackgroundColour((255, 255, 255))

        pass


if __name__ == '__main__':
    pass

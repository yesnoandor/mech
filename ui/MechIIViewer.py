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
import wx
from wx.lib import buttons
from random import choice
from ui.IconPanel import IconPanel
from ui.DevicePanel import DevicePanel
from ui.NodePanel import NodePanel
from ui.ModulePanel import ModulePanel
from ui.TabPanel import TabPanel
from ui.TabInfoPanel import TabInfoPanel
from ui.DeviceInfoPanel import DeviceInfoPanel
from ui.ChartPanel import ChartPanel
from ui.MechIIEvent import *


class MechIIViewer(wx.Frame):
    """
    Mech-II 主窗体
    """
    def __init__(self, devices_info={}, focus_device='', focus_node='', UpdateFrame=None, *args, **kwargs):
        self.UpdateFrame = UpdateFrame

        super(MechIIViewer, self).__init__(*args, **kwargs)

        # 获取设备节点信息
        self.devices_info = devices_info
        self.focus_device = focus_device
        self.focus_node = focus_node

        # 创建二维网格 wx.GridBagSizer, 列间隔为0，行间隔为0
        self.sizer = wx.GridBagSizer(0, 0)

        # 设置ICON图标区域 --> 指定大小 (248, 110)
        self.icon_panel = IconPanel(self)
        # 控件占满可用空间，四周都增加宽度为0的空白
        self.sizer.Add(self.icon_panel, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=0)
        self.icon_panel.SetBackgroundColour((0x38, 0x38, 0x38))

        # 设置Device信息区域
        self.device_info_panel = DeviceInfoPanel(devices=self.devices_info,
                                                 focus_device=self.focus_device,
                                                 focus_node=self.focus_node,
                                                 parent=self)
        # 控件占满可用空间，四周都增加宽度为0的空白
        self.sizer.Add(self.device_info_panel, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=0)

        # 创建TAB信息区域
        nodes = []
        for k, v in self.devices_info.items():
            nodes += v
        self.tab_info_panel = TabInfoPanel(nodes=nodes, focus_node=self.focus_node, parent=self)
        # 控件占满可用空间，底部对齐，左边增加宽度为2的空白
        self.sizer.Add(self.tab_info_panel, pos=(0, 1), flag=wx.EXPAND | wx.ALIGN_BOTTOM | wx.LEFT, border=2)

        # 创建chart图表区域 --> 默认显示
        self.chart_panel = ChartPanel(self.focus_node, self)
        self.chart_panel.SetMinSize((1600, 960))
        self.chart_panel.Hide()
        self.chart_panel.Show()
        # 控件占满可用空间，顶部对齐，左边，上边增加宽度为2的空白
        self.sizer.Add(self.chart_panel, pos=(1, 1), flag=wx.EXPAND | wx.ALIGN_TOP | wx.TOP | wx.LEFT, border=2)

        # 创建module模组区域 --> 默认隐藏
        self.module_panel = ModulePanel(self)
        self.module_panel.SetMinSize((1600, 960))
        self.module_panel.Hide()
        # self.module_panel.Show()
        # self.sizer.Add(self.module_panel, pos=(1, 1),  flag=wx.EXPAND | wx.ALIGN_TOP | wx.TOP | wx.LEFT, border=2)

        # 刷新
        self.sizer.Layout()

        # 设置窗口到当前Sizer
        self.SetSizer(self.sizer)

        # 设置整个Panel背景色 (黑色)
        self.SetBackgroundColour((0, 0, 0))

        # 绑定自定义的双击事件
        self.Bind(EVT_MODULE, self.OnModuleShow)
        self.Bind(EVT_CHART, self.OnChartShow)

    def OnModuleShow(self, evt):
        """
        切换到Module信息显示
        :param evt:
        :return:
        """
        print("OnModuleShow in MechIIViewer")
        print(evt.name)

        self.chart_panel.Hide()
        self.module_panel.Show()
        self.sizer.Replace(self.chart_panel, self.module_panel)
        self.sizer.Layout()
        pass

    def OnChartShow(self, evt):
        """
        切换到图表信息显示
        :param evt:
        :return:
        """
        print("OnChartShow")
        print(evt.name)

        self.module_panel.Hide()
        self.chart_panel.Show()
        self.sizer.Replace(self.module_panel, self.chart_panel)
        self.sizer.Layout()

    def UpdateMechIIViewer(self):
        self.sizer.Layout()

        self.UpdateFrame()
        pass


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
                         parent=None, title='Mech-II', name="DemoFrame", style=wx.DEFAULT_FRAME_STYLE, size=(1920, 1080))
    frame.Center()
    frame.Show()
    app.MainLoop()
    pass

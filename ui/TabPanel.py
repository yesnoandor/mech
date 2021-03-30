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
from utils.logger import SingleLogger


class TabPanel(wx.Panel):
    """
    单个切换信息面板
    """
    def __init__(self, focus=False, tab='Charts', name='xxxx', *args, **kwargs):
        super(TabPanel, self).__init__(*args, **kwargs)

        # 初始化日志类
        self.__logger = SingleLogger()

        self.name = name
        self.focus = focus
        self.tab = tab
        self.sizer = wx.GridBagSizer(0, 0)
        self.SetSizer(self.sizer)

        # Device
        # label = "Node-" + name
        label = name
        self.module_name = wx.StaticText(parent=self, size=(222, -1), id=wx.ID_ANY, label=label, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.module_name.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.module_name, pos=(0, 0), span=(1, 2), flag=wx.EXPAND | wx.BOTTOM, border=1)

        # Modules Tab
        self.modules = wx.StaticText(parent=self, size=(110, -1), id=wx.ID_ANY, label="Modules", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.modules.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.modules, pos=(1, 0), flag=wx.EXPAND | wx.LEFT, border=0)

        # Charts Tab
        self.charts = wx.StaticText(parent=self,  size=(110, -1), id=wx.ID_ANY, label="Charts", style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.charts.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.sizer.Add(self.charts, pos=(1, 1), flag=wx.EXPAND | wx.LEFT, border=1)

        if self.focus:
            self.module_name.SetBackgroundColour((0xfe, 0xd3, 0x63))
            self.module_name.SetForegroundColour((0, 0, 0))

            if self.tab == 'Modules':
                # self.modules.SetBackgroundColour((0x27, 0xc1, 0xf8))
                self.modules.SetBackgroundColour('DodgerBlue')
                self.modules.SetForegroundColour((250, 255, 255))

                self.charts.SetBackgroundColour("GREY")
                self.charts.SetForegroundColour((250, 255, 255))
            else:
                self.modules.SetBackgroundColour("GREY")
                self.modules.SetForegroundColour((250, 255, 255))

                # self.charts.SetBackgroundColour((0x27, 0xc1, 0xf8))
                self.charts.SetBackgroundColour('DodgerBlue')
                self.charts.SetForegroundColour((250, 255, 255))
        else:
            self.module_name.SetBackgroundColour("GREY")
            self.module_name.SetForegroundColour((250, 255, 255))

            self.modules.SetBackgroundColour("GREY")
            self.modules.SetForegroundColour((250, 255, 255))

            self.charts.SetBackgroundColour("GREY")
            self.charts.SetForegroundColour((250, 255, 255))

        self.module_name.Bind(wx.EVT_LEFT_DCLICK, self.OnNodeNameDoubleClicked)
        self.modules.Bind(wx.EVT_LEFT_DCLICK, self.OnModulesDoubleClicked)
        self.charts.Bind(wx.EVT_LEFT_DCLICK, self.OnChartsDoubleClicked)

    def SetFocus(self, focus):
        """
        设置当前TAB面板是否聚焦
        :param focus: =True, 设置当前面板聚焦
        :return:
        """
        # print("name = ", self.name)
        # print("focus = ", focus)
        # print("self.focus = ", self.focus)
        # print("self.tab = ", self.tab)
        if self.focus != focus:
            if focus:
                self.module_name.SetBackgroundColour((0xfe, 0xd3, 0x63))
                self.module_name.SetForegroundColour((0, 0, 0))

                if self.tab == 'Modules':
                    #self.modules.SetBackgroundColour((0x27, 0xc1, 0xf8))
                    self.modules.SetBackgroundColour('DodgerBlue')
                    self.modules.SetForegroundColour((250, 255, 255))

                    self.charts.SetBackgroundColour("GREY")
                    self.charts.SetForegroundColour((250, 255, 255))
                else:
                    self.modules.SetBackgroundColour("GREY")
                    self.modules.SetForegroundColour((250, 255, 255))

                    # self.charts.SetBackgroundColour((0x27, 0xc1, 0xf8))
                    self.charts.SetBackgroundColour('DodgerBlue')
                    self.charts.SetForegroundColour((250, 255, 255))

                if self.tab == 'Modules':
                    # self.modules.SetBackgroundColour((0x27, 0xc1, 0xf8))
                    self.modules.SetBackgroundColour('DodgerBlue')
                    self.modules.SetForegroundColour((250, 255, 255))

                    self.charts.SetBackgroundColour("GREY")
                    self.charts.SetForegroundColour((250, 255, 255))

                    # 发送切换Module图表
                    evt = ModuleEvent(
                        name=self.tab,
                    )

                    wx.QueueEvent(wx.GetApp().GetTopWindow(), evt)
                else:
                    self.modules.SetBackgroundColour("GREY")
                    self.modules.SetForegroundColour((250, 255, 255))

                    # self.charts.SetBackgroundColour((0x27, 0xc1, 0xf8))
                    self.charts.SetBackgroundColour('DodgerBlue')
                    self.charts.SetForegroundColour((250, 255, 255))

                    # 发送切换Chart图表
                    evt = ChartEvent(
                        name=self.tab,
                    )

                    wx.QueueEvent(wx.GetApp().GetTopWindow(), evt)
            else:
                self.module_name.SetBackgroundColour("GREY")
                self.module_name.SetForegroundColour((250, 255, 255))

                self.modules.SetBackgroundColour("GREY")
                self.modules.SetForegroundColour((250, 255, 255))

                self.charts.SetBackgroundColour("GREY")
                self.charts.SetForegroundColour((250, 255, 255))

        self.focus = focus
        pass

    def OnNodeNameDoubleClicked(self, event):
        """
        双击TAB区域中Node名字的事件处理
        :param event:
        :return:
        """
        self.__logger.info("double click Node {}".format(self.name))

        # 向Device信息区域发送选中Node的信息
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

    def OnModulesDoubleClicked(self, event):
        """
        双击Module Tab的事件处理
        :param event:
        :return:
        """
        self.__logger.info("Double click Chart --> Module")

        if not self.focus:
            return

        if self.tab == 'Charts':
            # self.modules.SetBackgroundColour((0x27, 0xc1, 0xf8))
            self.modules.SetBackgroundColour('DodgerBlue')
            self.modules.SetForegroundColour((250, 255, 255))

            self.charts.SetBackgroundColour("GREY")
            self.charts.SetForegroundColour((250, 255, 255))

            evt = ModuleEvent(
                name=self.tab,
            )

            wx.QueueEvent(wx.GetApp().GetTopWindow(), evt)

            self.tab = 'Modules'

    def OnChartsDoubleClicked(self, event):
        """
        双击Chart Tab的事件处理
        :param event:
        :return:
        """
        self.__logger.info("Double click Module  --> Chart")

        if not self.focus:
            return

        if self.tab == 'Modules':
            self.modules.SetBackgroundColour("GREY")
            self.modules.SetForegroundColour("WHITE")

            #self.charts.SetBackgroundColour((0x27, 0xc1, 0xf8))
            self.charts.SetBackgroundColour('DodgerBlue')
            self.charts.SetForegroundColour((250, 255, 255))

            evt = ChartEvent(
                name=self.tab,
            )

            wx.QueueEvent(wx.GetApp().GetTopWindow(), evt)

            self.tab = 'Charts'


if __name__ == '__main__':
    pass


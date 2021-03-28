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
from ui.CpuInfoPanel import CpuInfoPanel
from ui.HeartInfoPanel import HeartInfoPanel
from ui.MemoryInfoPanel import MemoryInfoPanel
from ui.NetworkInfoPanel import NetworkInfoPanel


class DiagramInfoPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(DiagramInfoPanel, self).__init__(*args, **kwargs)

        # 创建二维网格 wx.GridBagSizer, 列间隔为0，行间隔为0
        self.sizer = wx.GridBagSizer(0, 0)
        self.SetSizer(self.sizer)

        self.cpu_info_panel = CpuInfoPanel(self)
        self.sizer.Add(self.cpu_info_panel, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=0)
        # self.cpu_info_panel.SetBackgroundColour((80, 80, 80))
        # self.cpu_info_panel.SetMinSize((1564, 188))

        self.heart_beat_panel = HeartInfoPanel(self)
        self.sizer.Add(self.heart_beat_panel, pos=(0, 1), flag=wx.EXPAND | wx.LEFT, border=20)

        self.network_panel = NetworkInfoPanel(self)
        self.sizer.Add(self.network_panel, pos=(1, 0), flag=wx.EXPAND | wx.TOP, border=20)

        self.memory_info_panel = MemoryInfoPanel(self)
        self.sizer.Add(self.memory_info_panel, pos=(1, 1), flag=wx.EXPAND | wx.TOP | wx.LEFT, border=20)



        pass


if __name__ == '__main__':
    pass

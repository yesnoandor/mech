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
from ui.ModuleList import  ModuleList


class ModulePanel(wx.Panel):
    """
    显示所有模组信息的面板
    """
    def __init__(self, *args, **kwargs):
        super(ModulePanel, self).__init__(*args, **kwargs)

        # 创建一个容器，容器中的控件横向排列
        self.box = wx.BoxSizer(wx.HORIZONTAL)

        # 创建一个包含多列的组件
        self.list = ModuleList(parent=self, style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_HRULES | wx.LC_VRULES | wx.LC_SINGLE_SEL)

        # 将多列组件放入容器中
        self.box.Add(self.list, proportion=1, flag=wx.EXPAND | wx.ALL)

        # 使布局有效
        self.SetSizer(self.box)

        # 调整窗口大小以适合其最佳大小
        # self.Fit()


if __name__ == '__main__':
    pass

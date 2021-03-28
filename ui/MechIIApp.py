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
from ui.FrameManager import FrameManager


class MechIIApp(wx.App):
    """
    应用程序对象, 必须是类wx.App或其定制的子类的一个实例。应用程序对象的主要目的是管理幕后的主事件循环
    """

    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        super().__init__(redirect, filename, useBestVisual, clearSigInt)
        self.frame = None

        # 创建主窗体
        self.index = 0                  # 默认窗体
        self.manager = FrameManager(self.UpdateFrame)
        self.frame = self.manager.GetFrame(self.index)

        self.frame.Center()             # 在显示器中居中显示
        self.frame.Show()               # 显示

        self.SetTopWindow(self.frame)   # 当前frame设置为顶级窗口

    def UpdateFrame(self, index=0):
        """
        更新主窗体
        :param index:
        :return:
        """
        self.frame.Show(False)
        self.frame = self.manager.GetFrame(index)
        self.frame.Show(True)
        self.index = index
        self.SetTopWindow(self.frame)  # 当前frame设置为顶级窗口


if __name__ == '__main__':
    os.chdir("../")
    print(os.getcwd())

    app = MechIIApp()
    app.MainLoop()

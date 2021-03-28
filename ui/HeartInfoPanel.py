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
import numpy as np
import math
import matplotlib
from pubsub import pub
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from ui.FigureCanvasBasePanel import FigureCanvasBasePanel


class HeartInfoPanel(FigureCanvasBasePanel):
    """
    在画布上绘制CPU占用率柱状图
    """
    def __init__(self, *args, **kwargs):
        super(HeartInfoPanel, self).__init__(*args, **kwargs)

        # 创建画图板和画图区，重新设置了图形的大小
        self.figure = matplotlib.figure.Figure(figsize=(7.7, 3.4))
        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])

        # 去掉X轴，Y轴坐标
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        # 去掉对应的边框
        for key, spine in self.axes.spines.items():
            # 'left', 'right', 'bottom', 'top'
            if key == 'right' or key == 'top':
                spine.set_visible(False)

        self.FigureCanvas = FigureCanvas(self, -1, self.figure)

        self.heart_mode = False
        self.x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
        self.y = np.zeros(40, dtype=float)
        # self.y = np.array([0, 0, 0, 0.5, 0, -0.5, -1, 0, 1, 0.5, 0, -0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, -0.5, -1, 0, 1, 0.5, 0, -0.5, 0, 0, 0, 0, 0, 0, 0, 0])
        self.plot(self.x, self.y)

        # 订阅消息
        pub.subscribe(self.OnHeartBeatEvent, 'heart_beat_event')

        # 增加定时器，更新UI状态
        self._update_ui = wx.PyTimer(self.UpdateUI)
        self._update_ui.Start(1000)
        self._timeout = 0
        self._timeout_threhold = 5

    def plot(self, x, y):
        self.cla()

        # 设置标题
        self.axes.set_title('HEART', fontsize='large', fontweight='bold', color='black', loc='left')
        # self.axes.fill_between(x, -1, y, facecolor='red', alpha=0.1)    # 修改心跳柱子红色,然后透明色
        self.axes.plot(x, y, color='red')
        self.UpdatePlot()

    def set_mode(self, mode):
        if self.heart_mode is not mode:
            self.heart_mode = mode

            if self.heart_mode:
                self.y = np.array([0, 0, 0, 0.5, 0, -0.5, -1, 0, 1, 0.5, 0, -0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0, -0.5, -1, 0, 1, 0.5, 0, -0.5, 0, 0, 0, 0, 0, 0, 0, 0])
            else:
                self.y = np.zeros(40, dtype=float)

    def UpdateUI(self):
        self.y = np.roll(self.y, -1)
        self.plot(self.x, self.y)

        self._timeout = self._timeout + 1
        if self._timeout > self._timeout_threhold:
            self.set_mode(False)
        pass

    def OnHeartBeatEvent(self, mode):
        # print("OnHeartBeatEvent")
        # print("mode = ", mode)
        self.set_mode(mode)
        self._timeout = 0
        pass


if __name__ == '__main__':
    pass

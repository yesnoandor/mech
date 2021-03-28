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
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from ui.FigureCanvasBasePanel import FigureCanvasBasePanel
from ui.MechIIEvent import *


class MemoryInfoPanel(FigureCanvasBasePanel):
    """
    在画布上绘制CPU占用率柱状图
    """
    def __init__(self, *args, **kwargs):
        super(MemoryInfoPanel, self).__init__(*args, **kwargs)

        self.figure = matplotlib.figure.Figure(figsize=(7.7, 3.4))
        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.FigureCanvas = FigureCanvas(self, -1, self.figure)

        self.x = []
        self.y = []

        self.Bind(EVT_MEMORY_INFO, self.OnMemoryInfoEvent)

    def plot(self, labels, sizes):
        self.cla()

        #
        # colors = ['DodgerBlue', 'magenta']
        self.axes.set_title('MEMORY', fontsize='large', fontweight='bold', color='black', loc='left')  # 设置标题
        self.axes.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)       # autopct : 显示百分比, labels : 提供标签, shadow : 在饼图下面画阴影
        self.axes.axis('equal')                                         # 设置等比坐标轴
        self.axes.legend(labels=labels, loc='upper right')              # 设置图例， 位置偏右偏上

        self.UpdatePlot()

    def OnMemoryInfoEvent(self, evt):
        self.x = evt.labels
        self.y = list(map(float, evt.sizes))
        self.plot(self.x, self.y)
        pass


if __name__ == '__main__':
    pass

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


class CpuInfoPanel(FigureCanvasBasePanel):
    """
    在画布上绘制CPU占用率柱状图
    """
    def __init__(self, *args, **kwargs):
        super(CpuInfoPanel, self).__init__(*args, **kwargs)

        self.figure = matplotlib.figure.Figure(figsize=(7.7, 3.4))
        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.FigureCanvas = FigureCanvas(self, -1, self.figure)

        # 去掉对应的边框
        for key, spine in self.axes.spines.items():
            # 'left', 'right', 'bottom', 'top'
            if key == 'right' or key == 'top':
                spine.set_visible(False)

        #self.x = ['cpu0', 'cpu1', 'cpu2', 'cpu3', 'cpu4', 'cpu5']
        #self.y = [50, 60, 70, 80, 100, 100]
        #self.plot(self.x, self.y)
        self.x = []
        self.y = []

        self.Bind(EVT_CPU_INFO, self.OnCpuInfoEvent)

    def plot(self, x, y):
        self.cla()

        self.axes.set_title('CPU', fontsize='large', fontweight='bold', color='black', loc='left')  # 设置标题
        self.axes.bar(x, y, color="#EA8523", align='center')         # 绘制水平方向上柱状图
        self.UpdatePlot()

    def OnCpuInfoEvent(self, evt):
        print("data = ", evt.data)
        print("labels = ", evt.labels)
        self.x = evt.labels
        self.y = list(map(float, evt.data))
        self.plot(self.x, self.y)
        pass


if __name__ == '__main__':
    pass

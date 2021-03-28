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


import re
import wx
import numpy as np
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from ui.FigureCanvasBasePanel import FigureCanvasBasePanel
from ui.MechIIEvent import *


class NetworkInfoPanel(FigureCanvasBasePanel):
    """
    在画布上绘制CPU占用率柱状图
    """
    def __init__(self, *args, **kwargs):
        super(NetworkInfoPanel, self).__init__(*args, **kwargs)

        self.figure = matplotlib.figure.Figure(figsize=(7.7, 3.4))
        self.axes = self.figure.add_axes([0.1, 0.1, 0.8, 0.8])
        self.FigureCanvas = FigureCanvas(self, -1, self.figure)

        # 去掉X轴坐标
        self.axes.get_xaxis().set_visible(False)

        # 去掉对应的边框
        for key, spine in self.axes.spines.items():
            # 'left', 'right', 'bottom', 'top'
            if key == 'right' or key == 'top':
                spine.set_visible(False)

        self.x = np.linspace(0, 50)  # 创建等差素列, 数据开始点为0, 数据结束点为2Pi，样本数量默认50
        self.y = np.ones(50) * 60.0
        self.plot(self.x, self.y)

        self.Bind(EVT_NETWORK_INFO, self.OnNetworkInfoEvent)

    def plot(self, x, y):
        self.cla()

        self.axes.set_title('Network', fontsize='large', fontweight='bold', color='black', loc='left')  # 设置标题
        # self.axes.axhline(0, color='gray', linewidth=2.0)         # 在水平方向上画线
        self.axes.set_ylim(0, 100.0)                                # 设置y轴范围
        self.axes.plot(x, y)                                        # 绘制水平方向上柱状图
        self.axes.fill_between(x, 0, y, facecolor='#DC8B33', alpha=0.9)
        self.UpdatePlot()

    def OnNetworkInfoEvent(self, evt):
        non_decimal = re.compile(r'[^\d.]+')
        tx = float(non_decimal.sub('', evt.tx))
        rx = float(non_decimal.sub('', evt.rx))
        # print("network data = ", data)
        self.y = np.concatenate((self.y[1:], [tx]))
        # print(self.y)
        self.plot(self.x, self.y)


if __name__ == '__main__':
    pass

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


class FigureCanvasBasePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super(FigureCanvasBasePanel, self).__init__(*args, **kwargs)

        """
        fig, ax = pyplot.subplots(figsize=pyplot.figaspect(2.5 / 2))
        self.figure = fig
        self.axes = ax
        self.FigureCanvas = FigureCanvas(self, -1, self.figure)

        x = np.linspace(0, 2 * np.pi)  # 创建等差素列, 数据开始点为0, 数据结束点为2Pi，样本数量默认50
        y = np.sin(x)
        self.plot(x, y)
        """

    def UpdatePlot(self):
        """
        重新渲染，修改图形的任何属性后都必须重新调用来更新GUI界面
        :return:
        """
        self.FigureCanvas.draw()

    def plot(self, *args, **kwargs):
        """
        绘制画图区
        :param args:
        :param kwargs:
        :return:
        """
        self.axes.plot(*args, **kwargs)
        self.UpdatePlot()
        pass

    def scatter(self, *args, **kwargs):
        self.axes.scatter(*args, **kwargs)
        self.UpdatePlot()

    def loglog(self, *args, **kwargs):
        """
        在x和y轴上使用对数缩放比例绘制图
        :param args:
        :param kwargs:
        :return:
        """
        self.axes.loglog(*args, **kwargs)
        self.UpdatePlot()

    def semilogx(self, *args, **kwargs):
        """
        在x轴上使用对数缩放比例绘制图
        :param args:
        :param kwargs:
        :return:
        """
        self.axes.semilogx(*args, **kwargs)
        self.UpdatePlot()

    def semilogy(self, *args, **kwargs):
        """
        在y轴上使用对数缩放比例绘制图
        :param args:
        :param kwargs:
        :return:
        """
        ''''' #对数坐标绘图命令 '''
        self.axes.semilogy(*args, **kwargs)
        self.UpdatePlot()

    def set_title(self, title):
        """
        给图像添加一个标题
        :param title:
        :return:
        """
        self.axes.set_title(title)

    def set_xlabel(self, xlabel="X"):
        """
        设置x轴的标签
        :param xlabel:
        :return:
        """
        self.axes.set_xlabel(xlabel)

    def set_ylabel(self, ylabel="Y"):
        """
        设置y轴的标签
        :param ylabel:
        :return:
        """
        self.axes.set_ylabel(ylabel)

    def legend(self, *args, **kwargs):
        """
        设置图例
        :param args:
        :param kwargs:
        :return:
        """
        self.axes.legend(*args, **kwargs)

    def grid(self, on=True):
        """
        配制网格线，显示网格
        :param on:
        :return:
        """
        self.axes.grid(on)

    def xticker(self, major_ticker=1.0, minor_ticker=0.1):
        """
        设置X轴的刻度大小
        :param major_ticker:
        :param minor_ticker:
        :return:
        """
        self.axes.xaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.xaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def yticker(self, major_ticker=1.0, minor_ticker=0.1):
        """
        设置Y轴的刻度大小
        :param major_ticker:
        :param minor_ticker:
        :return:
        """
        self.axes.yaxis.set_major_locator(MultipleLocator(major_ticker))
        self.axes.yaxis.set_minor_locator(MultipleLocator(minor_ticker))

    def xlim(self, x_min, x_max):
        """
        设置X轴的显示范围
        :param x_min:
        :param x_max:
        :return:
        """
        self.axes.set_xlim(x_min, x_max)

    def ylim(self, y_min, y_max):
        """
        设置Y轴的显示范围
        :param y_min:
        :param y_max:
        :return:
        """
        self.axes.set_ylim(y_min, y_max)

    def savefig(self, *args, **kwargs):
        """
        保存图形到文件
        :param args:
        :param kwargs:
        :return:
        """
        self.Figure.savefig(*args, **kwargs)

    def cla(self):
        """
        清空原来的图形,再次画图前,必须调用该命令
        :return:
        """
        self.axes.clear()
        self.figure.set_canvas(self.FigureCanvas)
        # self.UpdatePlot()


if __name__ == '__main__':
    pass

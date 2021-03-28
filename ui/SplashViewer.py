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
import time
from pubsub import pub


class SplashViewer(wx.Frame):
    """
    Mech-II 主窗体
    """
    def __init__(self, UpdateFrame=None, *args, **kwargs):
        self.UpdateFrame = UpdateFrame

        super(SplashViewer, self).__init__(*args, **kwargs)

        # 创建Panel
        self.splash_panel = wx.Panel(self)

        # 显示图片
        self.image = wx.Image('res//splash.jpg', wx.BITMAP_TYPE_JPEG)
        self.image.Rescale(self.GetSize().GetWidth(), self.GetSize().GetHeight())
        self.bmp = self.image.ConvertToBitmap()
        wx.StaticBitmap(self.splash_panel, -1, bitmap=self.bmp)

        # 订阅消息
        pub.subscribe(self.UpdateUI, 'device_node_ready')

    def UpdateUI(self):
        # print("device node ready in SplashViewer")
        self.UpdateFrame(1)
        pass


if __name__ == '__main__':
    pass

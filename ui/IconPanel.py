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


class IconPanel(wx.Panel):
    """
    图标面板
    """
    def __init__(self, *args, **kwargs):
        super(IconPanel, self).__init__(*args, **kwargs)

        self.sizer = wx.GridBagSizer(0, 0)

        self.id_image = wx.StaticBitmap(parent=self,
                                        id=wx.ID_ANY,
                                        bitmap=wx.Bitmap('res//Mech-logo.png'),
                                        size=(248, 110))
        self.sizer.Add(self.id_image, pos=(0, 0), flag=wx.EXPAND | wx.LEFT, border=0)

        self.SetSizer(self.sizer)
        pass


if __name__ == '__main__':
    pass

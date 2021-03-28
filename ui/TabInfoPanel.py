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
from wx.lib import buttons
from ui.MechIIEvent import *
from ui.TabPanel import TabPanel
from ui.MenuPopup import MenuPopup


class TabInfoPanel(wx.Panel):
    """
    整个切换信息面板
    """
    def __init__(self, nodes, focus_node, *args, **kwargs):
        super(TabInfoPanel, self).__init__(*args, **kwargs)

        self.tab_panels = {}
        self.focus_node =focus_node

        # 创建水平方向网格 wx.BoxSizer
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.sizer)

        # 创建整个TAB信息
        for node in nodes:
            if node == focus_node:
                focus = True
            else:
                focus = False

            # 创建每一个TAB Panel
            panel = TabPanel(focus, tab='Charts', name=node, parent=self)
            self.sizer.Add(panel, flag=wx.EXPAND | wx.ALIGN_LEFT | wx.RIGHT, border=3)
            self.tab_panels[node] = panel

        # 创建菜单图标
        self.menu_image = buttons.GenBitmapButton(parent=self, id=wx.ID_ANY, bitmap=wx.Bitmap('res//Menu-icon-white.png'), size=(26, 24), style=wx.BORDER_NONE)
        self.menu_image.SetBackgroundColour('BLACK')
        # border = 140
        border = 1710 - 248 - (len(nodes) * 220)
        self.sizer.Add(self.menu_image, flag=wx.EXPAND | wx.LEFT, border=border)
        pos = self.menu_image.GetPosition()
        # print("pos = ", pos)
        # self.menu_image.Bind(wx.EVT_MOTION, self.onMotion)
        self.menu_image.Bind(wx.EVT_ENTER_WINDOW, self.onEnterWindow)
        self.menu_image.Bind(wx.EVT_LEAVE_WINDOW, self.onExitWindow)

        self.Bind(EVT_TAB_NODE, self.OnTabNodeShow)
        pass

    def OnTabNodeShow(self, evt):
        """

        :param evt:
        :return:
        """
        print("OnNodeShow in TabInfoPanel")
        print(self.focus_node)
        print(evt.name)

        if self.focus_node != evt.name:
            panel = self.tab_panels[self.focus_node]
            panel.SetFocus(False)

            panel = self.tab_panels[evt.name]
            panel.SetFocus(True)

            self.focus_node = evt.name
            pass

    def onMotion(self, evt):
        # print("onMotion")
        pass

    def onEnterWindow(self, evt):
        print("onEnterWindow")
        print(evt.GetPosition())
        pos = evt.GetPosition()
        pos = self.ScreenToClient(pos)
        print("pos = ", pos)
        self.main_popup_menu = MenuPopup(self)
        #self.PopupMenu(self.main_popup_menu, pos)
        self.PopupMenu(self.main_popup_menu, (1350, 60))
        self.main_popup_menu.Destroy()
        # evt.Skip()

        #

        '''
        try:
            self.win.GetTopLevelParent()
        except:
            self.win = MenuPopup(self.GetTopLevelParent(), wx.SIMPLE_BORDER)

            btn = evt.GetEventObject()
            pos = btn.ClientToScreen((0, 0))
            sz = btn.GetSize()

            # 设置弹窗的位置
            self.win.Position((300, 300), (500, 500))
            self.win.Show(True)
        '''
        pass

    def onExitWindow(self, evt):
        print("onExitWindow")
        # evt.Skip()
        # self.Destroy()


        pass


if __name__ == '__main__':
    pass

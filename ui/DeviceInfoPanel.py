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
from ui.MechIIEvent import *
from ui.DevicePanel import DevicePanel
from ui.NodePanel import NodePanel


class DeviceInfoPanel(wx.Panel):
    """
    设备信息面板, 包含多个设备信息
    """
    def __init__(self, devices={}, focus_device='', focus_node='', *args, **kwargs):
        super(DeviceInfoPanel, self).__init__(*args, **kwargs)

        self.devices_info = devices
        self.focus_device = focus_device
        self.focus_node = focus_node

        self.devices_panel = {}
        self.devices_status = {}                     # 描述每个Device信息的打开关闭状态
        self.nodes_panel = {}

        # 创建垂直方向网格 wx.BoxSizer,
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        for device_name, nodes_name in devices.items():
            self.devices_status[device_name] = True  # 默认Device信息都是打开状态

            # print("device name = ", device_name)
            if focus_device == device_name:
                focus = True
            else:
                focus = False

            device_panel = DevicePanel(name=device_name, focus=focus, status=self.devices_status[device_name],
                                       parent=self)

            if focus:
                device_panel.SetBackgroundColour('DodgerBlue')
                # device_panel.SetBackgroundColour((0x27, 0xc1, 0xf8))
                device_panel.SetForegroundColour((250, 255, 255))
            else:
                device_panel.SetBackgroundColour("GREY")
                device_panel.SetForegroundColour((250, 255, 255))

            self.sizer.Add(device_panel, flag=wx.EXPAND | wx.TOP, border=1)
            self.devices_panel[device_name] = device_panel

            for node_name in nodes_name:
                # print("node name = ", node_name)
                if focus_node == node_name:
                    focus = True
                else:
                    focus = False

                node_panel = NodePanel(name=node_name, focus=focus, parent=self)

                if focus:
                    node_panel.SetBackgroundColour((0xfe, 0xd3, 0x63))
                    node_panel.SetForegroundColour("BLACK")
                else:
                    node_panel.SetBackgroundColour("GREY")
                    node_panel.SetForegroundColour((250, 255, 255))

                if self.devices_status[device_name]:
                    node_panel.Show()
                    self.sizer.Add(node_panel, flag=wx.EXPAND | wx.ALL, border=0)
                else:
                    node_panel.Hide()
                # self.node_panel.SetBackgroundColour((80, 80, 80))
                # self.node_panel.SetForegroundColour((255, 255, 0))

                self.nodes_panel[node_name] = node_panel

                # print(self.nodes_panel)
                # print(self.devices_panel)

        self.SetSizer(self.sizer)
        self.sizer.Layout()
        # self.GetParent().Show()
        self.GetParent().sizer.Layout()

        self.Bind(EVT_NODE, self.OnNodeShow)
        self.Bind(EVT_DEVICE, self.OnDeviceShow)
        pass

    def GetDeviceFromNode(self, node):
        for device_name, nodes_name in self.devices_info.items():
            for node_name in nodes_name:
                if node == node_name:
                    return device_name
        pass

    def OnNodeShow(self, evt):
        """

        :param evt:
        :return:
        """
        print("OnNodeShow in DeviceInfoPanel")
        print(evt.name)

        if self.focus_node != evt.name:
            # 取消原来聚焦的device
            focus_device = self.GetDeviceFromNode(self.focus_node)
            device_panel = self.devices_panel[focus_device]
            device_panel.SetBackgroundColour("GREY")
            device_panel.SetForegroundColour((250, 255, 255))

            # 设置当前聚焦的device
            focus_device = self.GetDeviceFromNode(evt.name)
            device_panel = self.devices_panel[focus_device]
            # device_panel.SetBackgroundColour((0x27, 0xc1, 0xf8))
            device_panel.SetBackgroundColour('DodgerBlue')
            device_panel.SetForegroundColour((250, 255, 255))

            # 更新最新聚焦的device名
            self.focus_device = focus_device

            # 取消原来聚焦的node
            node_panel = self.nodes_panel[self.focus_node]
            node_panel.SetBackgroundColour("GREY")
            node_panel.SetForegroundColour((250, 255, 255))

            # 设置当前聚焦的node
            node_panel = self.nodes_panel[evt.name]
            node_panel.SetBackgroundColour((0xfe, 0xd3, 0x63))
            node_panel.SetForegroundColour("BLACK")

            # 更新最新聚焦的node名
            self.focus_node = evt.name
        pass

    def OnDeviceShow(self, evt):
        """

        :param evt:
        :return:
        """
        print("OnDeviceShow in  DeviceInfoPanel")
        print(evt.name)

        children = self.sizer.GetChildren()

        for child in children:
            widget = child.GetWindow()
            self.sizer.Hide(widget)
            self.sizer.Detach(widget)
            widget.Destroy()

        # self.GetParent().sizer.Layout()
        # self.GetParent().Fit()

        '''
        # 设置
        for node_name, node_panel in self.nodes_panel.items():
            node_panel.Hide()
            node_panel.Destroy()

        for device_name, device_panel in self.devices_panel.items():
            device_panel.Hide()
            device_panel.Destroy()
        '''

        self.devices_panel = {}
        self.nodes_panel = {}

        self.devices_status[evt.name] = (self.devices_status[evt.name] == False)
        print("devices_status = ", self.devices_status)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        for device_name, nodes_name in self.devices_info.items():
            print("device name = ", device_name)
            if self.focus_device == device_name:
                focus = True
            else:
                focus = False

            print("status = ", self.devices_status[device_name])
            device_panel = DevicePanel(name=device_name, focus=focus, status=self.devices_status[device_name],
                                       parent=self)

            if focus:
                # device_panel.SetBackgroundColour((0x27, 0xc1, 0xf8))
                device_panel.SetBackgroundColour('DodgerBlue')
                device_panel.SetForegroundColour((250, 255, 255))
            else:
                device_panel.SetBackgroundColour("GREY")
                device_panel.SetForegroundColour((250, 255, 255))

            device_panel.Show()
            self.sizer.Add(device_panel, flag=wx.EXPAND | wx.ALL, border=1)
            self.devices_panel[device_name] = device_panel

            # if not self.devices_status[device_name]:
            #    continue

            for node_name in nodes_name:
                # print("node name = ", node_name)
                if self.focus_node == node_name:
                    focus = True
                else:
                    focus = False

                node_panel = NodePanel(name=node_name, focus=focus, parent=self)

                if focus:
                    node_panel.SetBackgroundColour((0xfe, 0xd3, 0x63))
                    node_panel.SetForegroundColour("BLACK")
                else:
                    node_panel.SetBackgroundColour("GREY")
                    node_panel.SetForegroundColour((250, 255, 255))

                if self.devices_status[device_name]:
                    node_panel.Show()
                    self.sizer.Add(node_panel, flag=wx.EXPAND | wx.ALL, border=0)
                else:
                    node_panel.Hide()

                # self.node_panel.SetBackgroundColour((80, 80, 80))
                # self.node_panel.SetForegroundColour((255, 255, 0))

                self.nodes_panel[node_name] = node_panel

        self.SetSizerAndFit(self.sizer)
        # self.sizer.Layout()

        self.Hide()
        self.Show()

        # self.GetParent().Show()
        self.GetParent().sizer.Layout()
        self.GetParent().Fit()


if __name__ == '__main__':
    pass

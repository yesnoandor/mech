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
import re
from pubsub import pub
from ui.MechIIEvent import *
from wx.lib import scrolledpanel
from ui.SystemInfoPanel import SystemInfoPanel
from ui.DiagramInfoPanel import DiagramInfoPanel
from hw.devices import DevicesInfo


class ChartPanel(wx.Panel):
    """
    显示图表信息的面板
    """
    def __init__(self, focus_node, *args, **kwargs):
        super(ChartPanel, self).__init__(*args, **kwargs)

        self.focus_node = focus_node

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.system_info_panel = SystemInfoPanel(self)
        self.system_info_panel.SetMinSize((1564, 188))
        self.sizer.Add(self.system_info_panel, flag=wx.ALL, border=20)

        self.diagram_info_panel = DiagramInfoPanel(self)
        self.sizer.Add(self.diagram_info_panel, flag=wx.RIGHT | wx.LEFT, border=20)

        self.SetBackgroundColour((200, 200, 200))

        self.system_info = {}

        self.non_decimal = re.compile(r'[^\d.]+')

        # 订阅消息
        pub.subscribe(self.OnSystemInfoEvent, 'system_info_event')

        # device_params = DevicesInfo()
        # for uuid in device_params.get_uuid():
        #     pub.subscribe(self.OnSystemInfoEvent, uuid[-4:] + '_system_info_event')
        #     print(uuid[-4:] + '_system_info_event')

        # 绑定
        self.Bind(EVT_NODE, self.OnNodeShow)

    def OnNodeShow(self, evt):
        """

        :param evt:
        :return:
        """
        print("OnNodeShow in ChartPanel")
        print("evt name = ", evt.name)
        if self.focus_node != evt.name:
            self.focus_node = evt.name

            uuid = self.focus_node[-4:]

            # 刷新设备性能信息
            print(self.system_info)
            cpu_core = len(self.system_info[uuid]["cpu"].keys())
            print("system info : cpu core = ", cpu_core)
            memory_percent = "48"

            network_tx = float(self.non_decimal.sub('', self.system_info[uuid]["network"]["tx"]))
            if self.system_info[uuid]["network"]["tx"][-1] == 'M':
                network_tx * 1024
            network_rx = float(self.non_decimal.sub('', self.system_info[uuid]["network"]["rx"]))
            if self.system_info[uuid]["network"]["rx"][-1] == 'M':
                network_rx * 1024

            if (network_tx + network_rx) > 1024 :
                network_total = "%.2fM" % ((network_tx + network_rx) / 1024)
            else:
                network_total = "%.2fK" % (network_tx + network_rx)
            #network_tx = float(self.system_info[uuid]["network"]["tx"])
            #network_rx = float(self.system_info[uuid]["network"]["rx"])


            evt = PerformanceInfoEvent(
                uptime=self.system_info[uuid]["uptime"],
                temperature=self.system_info[uuid]["temperature"],
                memory=memory_percent,
                network=network_total,
                cpu=cpu_core
            )
            wx.QueueEvent(self.system_info_panel.performance_info, evt)

            # 刷新设备节点信息
            evt = NodeInfoEvent(
                hw=self.system_info[uuid]["version"]['hw'],
                sw=self.system_info[uuid]["version"]['sw'],
                ip=self.system_info[uuid]["ip"],
                uuid=self.system_info[uuid]["uuid"]
            )
            wx.QueueEvent(self.system_info_panel.node_info, evt)

            # 刷新设备CPU图表
            if self.system_info[uuid]["cpu"]:
                print("labels = ", self.system_info[uuid]["cpu"].keys())
                print("values = ", self.system_info[uuid]["cpu"].values())

                evt = CpuInfoEvent(
                    data=self.system_info[uuid]["cpu"].values(),
                    labels=self.system_info[uuid]["cpu"].keys()
                )

                wx.QueueEvent(self.diagram_info_panel.cpu_info_panel, evt)

            # 刷新设备Memory图表
            if self.system_info[uuid]["memory"]:
                sizes = []
                memory_sizes = []
                memory_labels = ['used', 'unused']

                for size in self.system_info[uuid]['memory'].values():
                    sizes.append(int(size[:-1]))

                total = int(sizes[0])
                used = int(sizes[1])

                print("total = ", total)
                print("used = ", used)

                used_percent = (used * 100) // total

                memory_sizes.append(used_percent)
                memory_sizes.append(100 - used_percent)

                evt = MemoryInfoEvent(
                    sizes=memory_sizes,
                    labels=memory_labels
                )

                wx.QueueEvent(self.diagram_info_panel.memory_info_panel, evt)

            # 刷新设备网络信息图表
            if self.system_info[uuid]["network"]:
                evt = NetworkInfoEvent(
                    tx=self.system_info[uuid]["network"]["tx"],
                    rx=self.system_info[uuid]["network"]["rx"]
                )

                wx.QueueEvent(self.diagram_info_panel.network_panel, evt)


        pass

    def OnSystemInfoEvent(self, info):
        """
        接收监控System的信息，并刷新界面
        :param info:
        :return:
        """
        print("system info : sw version = ", info["version"]['sw'])
        print("system info : hw version = ", info["version"]['hw'])
        print("system info : temperature = ", info["temperature"])
        print("system info : ip = ", info["ip"])
        print("system info : uuid = ", info["uuid"])
        print("system info : memory = ", info["memory"])
        print("system info : cpu = ", info["cpu"])
        print("system info : network = ", info["network"])
        print("system info : uptime = ", info["uptime"])
        # print("system info : storage = ", info["storage"])

        uuid = info["uuid"][-4:]
        print("focus node = ", self.focus_node[-4:])
        print("uuid =", uuid)

        self.system_info[uuid] = info               # 每个设备根据UUID保存一份系统信息
        if uuid != self.focus_node[-4:]:
            print("not focus node chart!")
            return

        # 刷新设备性能信息
        cpu_core = len(info["cpu"].keys())
        memory_percent = "48"

        network_tx = float(self.non_decimal.sub('', self.system_info[uuid]["network"]["tx"]))
        if self.system_info[uuid]["network"]["tx"][-1] == 'M':
            network_tx * 1024
        network_rx = float(self.non_decimal.sub('', self.system_info[uuid]["network"]["rx"]))
        if self.system_info[uuid]["network"]["rx"][-1] == 'M':
            network_rx * 1024

        if (network_tx + network_rx) > 1024:
            network_total = "%.2fM" % ((network_tx + network_rx) / 1024)
        else:
            network_total = "%.2fK" % (network_tx + network_rx)

        # 刷新某个设备节点的性能信息
        evt = PerformanceInfoEvent(
            uptime=info["uptime"],
            temperature=info["temperature"],
            memory=memory_percent,
            network=network_total,
            cpu=cpu_core
        )
        wx.QueueEvent(self.system_info_panel.performance_info, evt)

        # 刷新某个设备节点的设备信息
        evt = NodeInfoEvent(
            hw=info["version"]['hw'],
            sw=info["version"]['sw'],
            ip=info["ip"],
            uuid=info["uuid"]
        )
        wx.QueueEvent(self.system_info_panel.node_info, evt)

        # 刷新设备CPU图表
        if info["cpu"]:
            print("labels = ", info["cpu"].keys())
            print("values = ", info["cpu"].values())

            evt = CpuInfoEvent(
                data=info["cpu"].values(),
                labels=info["cpu"].keys()
            )

            wx.QueueEvent(self.diagram_info_panel.cpu_info_panel, evt)

        # 刷新设备Memory图表
        if info["memory"]:
            sizes = []
            memory_sizes = []
            memory_labels = ['used', 'unused']

            for size in info['memory'].values():
                sizes.append(int(size[:-1]))

            total = int(sizes[0])
            used = int(sizes[1])

            print("total = ", total)
            print("used = ", used)

            used_percent = (used * 100) // total

            memory_sizes.append(used_percent)
            memory_sizes.append(100 - used_percent)

            evt = MemoryInfoEvent(
                sizes=memory_sizes,
                labels=memory_labels
            )

            wx.QueueEvent(self.diagram_info_panel.memory_info_panel, evt)

        # 刷新设备网络信息图表
        if info["network"]:
            print("network++++++++++++++++++++++++++++++++")

            evt = NetworkInfoEvent(
                tx=info["network"]["tx"],
                rx=info["network"]["rx"]
            )

            wx.QueueEvent(self.diagram_info_panel.network_panel, evt)

            print("network--------------------------------")


if __name__ == '__main__':
    pass

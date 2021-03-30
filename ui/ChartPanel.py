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
from utils.logger import SingleLogger
from hw.devices import DevicesInfo


class ChartPanel(wx.Panel):
    """
    显示图表信息的面板
    """
    def __init__(self, focus_node, *args, **kwargs):
        super(ChartPanel, self).__init__(*args, **kwargs)

        # 初始化日志类
        self.__logger = SingleLogger()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.system_info_panel = SystemInfoPanel(self)
        self.system_info_panel.SetMinSize((1564, 188))
        self.sizer.Add(self.system_info_panel, flag=wx.ALL, border=20)

        self.diagram_info_panel = DiagramInfoPanel(self)
        self.sizer.Add(self.diagram_info_panel, flag=wx.RIGHT | wx.LEFT, border=20)

        self.SetBackgroundColour((200, 200, 200))

        self.system_info = {}
        self.focus_node = focus_node
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
        self.__logger.info("Switch Node = {} --> {}".format(self.focus_node, evt.name))

        if self.focus_node != evt.name:
            self.focus_node = evt.name

            uuid = self.focus_node[-4:]

            # 计算cpu核数
            cpu_core = len(self.system_info[uuid]["cpu"].keys())
            self.__logger.debug("cpu core = {}".format(cpu_core))

            # 计算内存占有率
            total = int(self.system_info[uuid]['memory']['total'][:-1])
            used = int(self.system_info[uuid]['memory']['used'][:-1])
            memory_usage = (used * 100) // total
            self.__logger.debug("memory usage = {}".format(memory_usage))

            # 计算网络速率
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

            # 刷新设备性能信息
            evt = PerformanceInfoEvent(
                uptime=self.system_info[uuid]["uptime"],
                temperature=self.system_info[uuid]["temperature"],
                memory=memory_usage,
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
                # print("labels = ", self.system_info[uuid]["cpu"].keys())
                # print("values = ", self.system_info[uuid]["cpu"].values())

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

                # print("total = ", total)
                # print("used = ", used)

                memory_usage = (used * 100) // total

                memory_sizes.append(memory_usage)
                memory_sizes.append(100 - memory_usage)

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
        self.__logger.debug("sw version = %s" % info["version"]['sw'])
        self.__logger.debug("hw version = %s" % info["version"]['hw'])
        self.__logger.debug("temperature = %s" % info["temperature"])
        self.__logger.debug("ip = %s" % info["ip"])
        self.__logger.debug("uuid = %s" % info["uuid"])
        self.__logger.debug("memory = %s" % info["memory"])
        self.__logger.debug("cpu = %s" % info["cpu"])
        self.__logger.debug("network = %s" % info["network"])
        self.__logger.debug("uptime = %s" % info["uptime"])

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
        """

        uuid = info["uuid"][-4:]
        self.__logger.debug("uuid = %s" % uuid)
        self.__logger.debug("focus uuid = %s" % self.focus_node[-4:])

        self.system_info[uuid] = info               # 每个设备根据UUID保存一份系统信息
        if uuid != self.focus_node[-4:]:            # 不是当前焦点的uuid，则不显示系统信息
            # print("not focus node chart!")
            return

        # 计算CPU核数
        cpu_core = len(info["cpu"].keys())
        self.__logger.debug("cpu core = %d" % cpu_core)

        # 计算内存占有率
        total = int(int(info["memory"]["total"][:-1]))
        used = int(int(info["memory"]["used"][:-1]))

        memory_usage = (used * 100) // total
        self.__logger.debug("memory usage = %d" % memory_usage)

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
            memory=memory_usage,
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
            # print("labels = ", info["cpu"].keys())
            # print("values = ", info["cpu"].values())

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

            memory_usage = (used * 100) // total

            memory_sizes.append(memory_usage)
            memory_sizes.append(100 - memory_usage)

            evt = MemoryInfoEvent(
                sizes=memory_sizes,
                labels=memory_labels
            )

            wx.QueueEvent(self.diagram_info_panel.memory_info_panel, evt)

        # 刷新设备网络信息图表
        if info["network"]:
            evt = NetworkInfoEvent(
                tx=info["network"]["tx"],
                rx=info["network"]["rx"]
            )

            wx.QueueEvent(self.diagram_info_panel.network_panel, evt)


if __name__ == '__main__':
    pass

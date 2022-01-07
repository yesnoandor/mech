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


import os
import wx
import sys
from pubsub import pub
from ui.MechIIEvent import *
from ui.LoggerView import LoggerFrame
from hw.devices import DevicesInfo
from utils.logger import SingleLogger
from db.sql import db_sql


class ModuleList(wx.ListCtrl):
    def __init__(self, *args, **kwargs):
        super(ModuleList, self).__init__(*args, **kwargs)

        # 初始化日志类
        self.__logger = SingleLogger()

        # 创建数据库管理类
        self.__sql = db_sql()

        # 当前Module Tab显示的列名
        self.AddColumns()

        # 初始化私有变量
        self._monitor_modules_list = {}               # 对应每个设备(uuid), 记录这个设备的每个module的名字和位置的对应关系
        # self._monitor_modules_log = {}              # 对应每个设备(uuid), 记录这个设备的每个module的名字和日志的对应关系
        # self._monitor_modules_max_state = {}        # 对应每个设备(uuid), 记录这个设备的每个module的名字和状态的对应关系

        # 默认的焦点设备，节点和设备的uuid
        devices_info = DevicesInfo()
        devices = devices_info.get_devices_name()
        self.__logger.debug("all devices list = {}".format(devices))

        #
        self.__focus_device = list(devices.keys())[0]
        self.__focus_node = devices[self.__focus_device][0]
        self.__focus_uuid = devices_info.get_uuid()[0]

        # 初始化每个设备，必须监控的模块
        for uuid in devices_info.get_uuid():
            # 当前Module Tab监控的模块
            self._monitor_modules_list[uuid] = {}           # {name : index} --> 记录每个module的名字和位置的对应关系
            # self._monitor_modules_max_state[uuid] = {}      # {name : state} --> 记录每个module的名字和最差状态的对应关系
            # self._monitor_modules_log[uuid] = {}            # {name : log} --> 记录每个module的名字和日志的对应关系

            # self.__focus_uuid = uuid

            # 显示当前节点必须监控的模块
            for module in devices_info.get_module_monitor_name_from_uuid(uuid):
                item = (module, '')
                index = self.AddItem(item)

                self._monitor_modules_list[self.__focus_uuid][module] = {}
                self._monitor_modules_list[self.__focus_uuid][module]["index"] = index
                self._monitor_modules_list[self.__focus_uuid][module]["log"] = ''
                self._monitor_modules_list[self.__focus_uuid][module]["state"] = "none"

                self.__sql.create_table(uuid=uuid, name=module)

        # 订阅消息 (module信息传输触发事件消息)
        self.__pub_module_info_msg_name = 'module_info_event'
        pub.subscribe(self.OnReceiveModuleEvent, self.__pub_module_info_msg_name)

        # 绑定公共事件处理
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemDoubleClicked)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnItemRightClicked)

        # 绑定自定义事件处理
        self.Bind(EVT_NODE, self.OnNodeShow)

    def OnItemSelected(self, event):
        pass
        # item = event.GetIndex()

        # self.Select(item, False)
        # wx.MessageBox("Single Cilcked", "Single cilck", wx.YES_NO)

    def OnItemDeselected(self, event):
        pass
        # event.Skip()
        # wx.MessageBox("Double Cilcked", "Double cilck", wx.YES_NO)

    def OnItemDoubleClicked(self, event):
        """
        双击Item的事件处理
        :param event:
        :return:
        """

        item_index = event.GetIndex()
        # 获取当前item第一列的文本内容
        item_name = self.GetItem(item_index, 0)
        module_name = item_name.GetText()
        # 获取当前item第二列的文本内容
        # item_log = self.GetItem(item_index, 1)
        # module_log = item_log.GetText()

        path = "log" + os.sep + self.__focus_uuid

        print("focus uuid = ", self.__focus_uuid)
        print("module_name = ", module_name)
        print("path = ", path)

        frm = LoggerFrame(module=module_name, path=path, mode='all', parent=None, style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE, title='Change wxTextCtrl colors example')
        frm.Show()
        pass

    def OnItemRightClicked(self, event):
        pass

    def AddColumns(self):
        """
        增加列格式，包含列标题
        :return: None
        """
        # width = self.GetSize().GetWidth()
        self.InsertColumn(0, 'Module', wx.LIST_FORMAT_CENTER, width=600)
        self.InsertColumn(1, 'Log', wx.LIST_FORMAT_CENTER, width=1000)

    def AddItem(self, item):
        """
        增加行记录
        :param item: 一条行记录 (name, log)
        :return: None
        """
        name = item[0]
        log = item[1]
        index = self.InsertItem(sys.maxsize, name)
        self.SetItem(index, 1, log)

        # print("uuid = ", self.__focus_uuid)
        # self._monitor_modules_list[self.__focus_uuid] = {}
        # self._monitor_modules_list[self.__focus_uuid][name] = {}
        # self._monitor_modules_list[self.__focus_uuid][name]["index"] = index
        # self._monitor_modules_list[self.__focus_uuid][name]["log"] = log
        # self._monitor_modules_list[self.__focus_uuid][name]["state"] = "none"

        # self._monitor_modules_log[self.__focus_uuid][name] = log

        # if name not in self._monitor_modules_max_state[self.__focus_uuid].keys():
        #    self._monitor_modules_max_state[self.__focus_uuid][name] = 0         # 默认白色

        # print("monitor modules list = ", self._monitor_modules_list)
        # print("monitor module max state = ", self._monitor_modules_max_state)
        # print("monitor module log = ", self._monitor_modules_log)
        return index

    def UpdateItemStatus(self, name, status):
        """
        更新每一行记录的状态
        :param name:
        :param status:
        :return:
        """
        if status == 'warning':
            self.UpdateItemBackground(name, 'yellow')
        elif status == 'error':
            self.UpdateItemBackground(name, 'red')
        elif status == 'info':
            self.UpdateItemBackground(name, 'green')

    def UpdateItemBackground(self, item_name, color):
        """
        更新每一行记录的背景色
        :param item_name:
        :param color:
        :return:
        """
        index = self._monitor_modules_list[self.__focus_uuid][item_name]["index"]
        self.SetItemBackgroundColour(index, color)

    def OnSize(self, event):
        """
        包含多列的组件大小变化的事件触发的处理
        :param event: 大小变化的事件
        :return: None
        """
        # print(type(event))
        width = self.GetSize().GetWidth()

        self.SetColumnWidth(0, width * 0.3)
        self.SetColumnWidth(1, width * 0.7)

        event.Skip()
        pass

    def OnNodeShow(self, evt):
        """
        切换Node的事件触发
        :param evt:
        :return:
        """
        self.__logger.info("Switch Node = {} --> {}".format(self.__focus_node, evt.name))
        # print("focus_uuid = ", self.__focus_uuid)

        #
        if self.__focus_node != evt.name:
            if self.DeleteAllItems() is not True:
                self.__logger.error("error in DeleteAllItems")
            else:
                self.__logger.debug("ok in DeleteAllItems")

            devices_info = DevicesInfo()
            # print(devices_info.get_uuid())
            for uuid in devices_info.get_uuid():
                if uuid[-4:] == evt.name[-4:]:
                    # print("match evt.name and uuid", uuid[-4:], evt.name[-4:])
                    # print("modules list = ", self._monitor_modules[uuid])
                    # print("monitor_modules = ", self._monitor_modules)
                    # print("monitor modules list = ", self._monitor_modules_list)
                    self.__logger.debug("monitor modules list = {}".format(self._monitor_modules_list))
                    # print("monitor modules log = ", self._monitor_modules_log)
                    # print("monitor modules max state = ", self._monitor_modules_max_state)

                    self.__focus_node = evt.name
                    self.__focus_uuid = uuid

                    # 显示当前节点必须监控的模块
                    for name in self._monitor_modules_list[self.__focus_uuid]:
                        log = self._monitor_modules_list[self.__focus_uuid][name]["log"]
                        item = (name, log)
                        index = self.AddItem(item)

                        # self._monitor_modules_list[self.__focus_uuid][name] = {}
                        # self._monitor_modules_list[self.__focus_uuid][name]["index"] = index
                        # self._monitor_modules_list[self.__focus_uuid][name]["log"] = log
                        # self._monitor_modules_list[self.__focus_uuid][name]["state"] = "none"

                        status = self._monitor_modules_list[self.__focus_uuid][name]["state"]
                        self.UpdateItemStatus(name, status)

                        """
                        if state == 'warning':
                            self.UpdateItemBackground(name, 'yellow')
                        elif state == 'error':
                            self.UpdateItemBackground(name, 'red')
                        elif state == 'info':
                            self.UpdateItemBackground(name, 'green')
                        """

                        """
                        # 判断当前item最恶劣的状态
                        level = self._monitor_modules_max_state[self.__focus_uuid][name]
                        if level == 2:
                            self.UpdateItemBackground(name, 'yellow')
                        elif level == 3:
                            self.UpdateItemBackground(name, 'red')
                        elif level == 1:
                            self.UpdateItemBackground(name, 'green')
                        """
    """
    def get_module_state_level(self, state):
        state_level = {
            'info': 1,
            'warning': 2,
            'error': 3
        }
        return state_level[state]
    """

    def OnReceiveModuleEvent(self, uuid, name, log, status, time):
        """
        接收监控Module的信息，并刷新界面
        :param uuid:
        :param name:
        :param log:
        :param status:
        :param time:
        :return:
        """
        self.__logger.debug("uuid = {}".format(uuid))
        self.__logger.debug("name = {}".format(name))
        self.__logger.debug("log = %s" % log)
        self.__logger.debug("status = %s" % status)
        self.__logger.debug("timestamp = %s" % time)

        # print("self uuid = ", self.__focus_uuid)
        # print("uuid = ", uuid)
        # print("name = ", name)
        # print("log = ", log)
        # print("status = ", status)
        # print("time = ", time)

        if name not in self._monitor_modules_list[uuid].keys():
            self.__sql.create_table(uuid=uuid, name=name)
        self.__sql.insert_record(uuid=uuid,
                                 name=name,
                                 log=log,
                                 state=status,
                                 date=time)

        if self.__focus_uuid != uuid:
            return

        if name in self._monitor_modules_list[uuid].keys():
            index = self._monitor_modules_list[uuid][name]["index"]

            # print("++++++++++++++++++++++++++++++++")
            # print("index = ", index)
            # print("uuid = ", uuid)
            # print("name = ", name)
            # print("log = ", log)
            # print("status = ", status)
            # print("monitor modules list = ", self._monitor_modules_list)
            # print("---------------------------------")

            self.SetItem(index, 0, name)                            # 更新Module的名字
            self.SetItem(index, 1, log)                             # 更新Module的日志

            self._monitor_modules_list[uuid][name]["log"] = log     # 更新Module的日志信息
        else:
            item = (name, log, status)
            index = self.AddItem(item)

            self._monitor_modules_list[self.__focus_uuid][name] = {}
            self._monitor_modules_list[self.__focus_uuid][name]["index"] = index    # 更新Module的索引信息
            self._monitor_modules_list[self.__focus_uuid][name]["log"] = log        # 更新Module的日志信息

        self._monitor_modules_list[self.__focus_uuid][name]["state"] = status       # 更新Module的状态信息
        self.UpdateItemStatus(name, status)

        # print("monitor modules list = ", self._monitor_modules_list)

        """
        if status == 'warning':
            self.UpdateItemBackground(name, 'yellow')
        elif status == 'error':
            self.UpdateItemBackground(name, 'red')
        elif status == 'info':
            self.UpdateItemBackground(name, 'green')
        """


if __name__ == '__main__':
    pass

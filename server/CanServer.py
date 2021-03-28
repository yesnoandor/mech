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
import os

import threading
from pubsub import pub
from utils.bytes import print_bytes, bytesToHexString
from utils.crc import crc8
from queue import Queue
from hw.canfd import CanAnalyze_ZLG
from protocol.ModuleProtocol import *
from gaea.config import system_params


class CANServerThread(threading.Thread):
    """
    CAN 服务器
        1. Echo功能
        2. 发送休眠唤醒
        3. 根据配置，发送数据
    """
    def __init__(self, name, data, event):
        super().__init__(name=name)         # 调用父类(超类)的__init__()方法

        # 初始化日志类
        # self.__logger = Logger('log/mech.log', logging.DEBUG, logging.ERROR)

        # 外部通讯参数
        self.__queue = data                 # 用于向外部传输队列数
        self.__event = event                # 用于触发外部事件

        # 控制线程参数初始化
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.set()                   # 设置为True,默认线程运行
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()                # 将running设置为True

        # 获取系统参数
        self.__system_config = system_params()

        # CAN分析仪的初始化
        vid, pid = self.__system_config.get_can_analyzer_info()
        self.__canfd = CanAnalyze_ZLG(vid, pid)
        self.__canfd.StartAll()

        # 协议初始化
        self.protocol = ModuleProtocol()

        # 获取CAN服务器的运行方式
        self.__policy = self.__system_config.get_can_protocol()

        # 服务器不同的协议处理方式
        self.__canfd_protocol_treat = {"echo": self.echo, "monitor": self.monitor, "uds": self.uds}

        # 每个CAN通道的变量
        self.msg = dict()                   # 每个CAN通道的数据bytearray
        self.start_flag = dict()            # 每个CAN通道的数据魔术字状态

        # CAN Tree
        self.__can_node_info = self.__system_config.get_can_all_module_info()

        # CAN服务器的状态机 ('idle', 'echo', 'monitor', 'uds')
        self.state = 'idle'

    def __del__(self):
        print("__del__")

    def pause(self):
        print("pause CAN server thread!")
        self.__flag.clear()         # 设置为False, 让线程阻塞

    def resume(self):
        print("resume CAN server thread!")
        self.__flag.set()           # 设置为True, 让线程停止阻塞

    def stop(self):
        print("stop CAN server thread!")
        self.__flag.set()           # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()      # 设置为False

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()              # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

            # 根据不同的配置，CAN Server不同的协议处理方式 (默认echo模式)
            self.__canfd_protocol_treat.get(self.__policy, self.echo)()

            # id, msg = self.canfd.Receive(index=0, channel=0, mode='CANFD')
            # can_tx_id = system_config.get_can_tx_id(id)
            # self.canfd.Send(index=0, channel=0, can_id=can_tx_id, mode='CANFD')

            # print(type(id))
            # print(id)
            # print(type(msg))
            # print(msg)
            # print_hex(msg)

            # if self.verify_crc(msg):
            #    log = "OK"
            #    status = "info"
            #    print("crc ok!")
            # else:
            #    log = "CRC Failed"
            #    status = "error"
            #    print("crc failed!")

            # name = "MODULE_CAN{}_TX".format(id)

            # device_config.get_ip_from_uuid("abcdefgh")
            # wx.CallAfter(pub.sendMessage, self.__pub_message_name, name=name, log=log, status=status)


            #   self.__exit.wait(0.01)                           # 等待退出事件, 0.01s超时退出
            #   if self.__exit.isSet():
            #       self.__exit.clear()

            #        self.__found.clear()
            #        self.__found_label.clear()

            #        self.pause()                                # 暂停线程

            #else:
            #    break

    def verify(self):
        print("pause CAN server thread!")

    def verify_crc(self, data):
        print(data)
        res = crc8(data)
        if res == 0:
            return True
        else:
            return False

    def parse_uuid(self, msg):
        """
        根据CAN报文，获取当前消息的uuid
        :param msg:
        :param can_tx_id:
        :param can_rx_id:
        :return:
        """
        uuid = None
        if int(msg[0]) == const.MAGIC_NUMBER:
            token = const.MAGIC_NUMBER.to_bytes(length=1, byteorder='big', signed=False)

            pos = msg.find(token, 1)
            print("pos = ", pos)
            print("data = ", msg[:pos+1])
            uuid = self.protocol.parse_uuid(msg[:pos+1])
            print("uuid = ", uuid)

        return uuid

    def echo(self):
        """
        应答处理
        :return:
        """
        for sn in self.__canfd.GetSN():  # 获取所有的CAN分析仪设备SN号
            # print("sn = ", sn)
            index = self.__canfd.GetDevIDFromSN(sn)  # 获取所有的CAN分析仪设备的索引号

            for channel in self.__canfd.GetChannelFromSN(sn):  # 获取所有的CAN分析仪设备
                can_rx_id, msg = self.__canfd.Receive(index=index, channel=channel, mode='CANFD', timeout=0)
                if can_rx_id == 0x00:
                    continue

                print("index = ", index)
                print("channel = ", channel)
                can_tx_id = self.__system_config.get_can_tx_id(id)
                print("can rx id = ", hex(can_rx_id))
                print("can tx id = ", hex(can_tx_id))
                print_bytes(msg)

                self.__canfd.Send(index=index, channel=channel, can_id=can_tx_id, mode='CANFD', data=msg)

                uuid = self.parse_uuid(msg)
                if uuid is not None:
                    for name in self.__can_node_info.keys():
                        if self.__can_node_info[name]['tx_id'] == can_tx_id:
                            if self.__can_node_info[name].get('uuid', True):
                                print("name = ", name)
                                print(self.__can_node_info)

                                self.__can_node_info[name]['uuid'] = uuid
                                self.__can_node_info[name]['index'] = index
                                self.__can_node_info[name]['channel'] = channel
                                print("can node info++++++++++++++++++++")
                                print(self.__can_node_info)
                                print("can node info--------------------")

    def monitor(self):
        """

        :return:
        """
        pass

        """
        print("monitor::++++++++++")
        monitor_can_id = system_config.get_can_monitor_id()
        while True:
            for sn in self.canfd.GetSN():               # 获取所有的CAN分析仪设备SN号
                # print("sn = ", sn)
                index = self.canfd.GetDevIDFromSN(sn)   # 获取所有的CAN分析仪设备的索引号

                for channel in self.canfd.GetChannelFromSN(sn):     # 获取所有的CAN分析仪设备
                    # print("index = ", index)
                    # print("channel = ", channel)
                    id, datas = self.canfd.Receive(index=index, channel=channel, mode='CANFD', timeout=1)

                    if id == 0x00:
                        continue

                    if id != monitor_can_id:
                        print("id = ", hex(id))
                        print_bytes(datas)

                        can_tx_id = system_config.get_can_tx_id(id)
                        print("can rx id = ", hex(id))
                        print("can tx id = ", hex(can_tx_id))
                        print_bytes(datas)
                        self.canfd.Send(index=index, channel=channel, can_id=can_tx_id, mode='CANFD', data=datas)

                        continue
                    else:
                        # print("id = ", id)
                        # print("datas = ", datas)

                        if id not in self.msg.keys():
                            self.msg[id] = b''
                            wx.CallAfter(pub.sendMessage, 'socket_setup_event', ip=str(id))
                        if id not in self.start_flag.keys():
                            self.start_flag[id] = False

                        for data in datas:
                            # print("msg[id] = ", self.msg[id])
                            print("start_flag[id] = ", self.start_flag[id])
                            if int(data) == 126:
                                # 将int(0~255)的值 转化为单字节的bytes类型
                                self.msg[id] += data.to_bytes(length=1, byteorder='big', signed=False)
                                if self.start_flag[id]:
                                    print("msg[id] = ", self.msg[id])
                                    print("len msg[id]", len(self.msg[id]))
                                    print_bytes(self.msg[id])
                                    self.protocol.parse_data(self.msg[id])

                                    print("\r\n")

                                    self.start_flag[id] = False
                                    self.msg[id] = b''
                                    break
                                else:
                                    self.start_flag[id] = True

                                    print("find magic char")
                                    # print("type data = ", type(data))
                                    # print("data = ", data)
                                    # print("type datas = ", type(datas))
                                    # print("datas = ", datas)
                                    # print_hex(datas)
                                    # print("id = ", id)

                            elif self.start_flag[id]:
                                #print("len msg[id] ", len(self.msg[id]))
                                #print("len data", len(data))
                                #print_hex(self.msg[id])
                                # 将int(0~255)的值 转化为单字节的bytes类型
                                self.msg[id] += data.to_bytes(length=1, byteorder='big', signed=False)
                                #print("data = ", data)
                                #print("len2 msg[id] ", len(self.msg[id]))
                                #print_hex(self.msg[id])

                            else:
                                continue

        print("monitor::----------")
        pass
        """

    def uds(self):
        pass

    def send(self, index, channel, data):
        """
        跨物理帧的CAN数据传输
        :param index:
        :param channel:
        :param data:
        :return:
        """
        head = 0
        end = head + 64
        while head < len(data):
            msg = data[head:end]
            self.canfd.Send(index=index, channel=channel, mode='CANFD', data=msg)
            head = end
            end = end + 64


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    queue = Queue()
    event = threading.Event()
    can_server_thread = CANServerThread("CANServer", queue, event)
    can_server_thread.start()

    can_server_thread.join()
    pass

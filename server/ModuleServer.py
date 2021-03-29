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
import time
import threading
import logging
from pubsub import pub
from queue import Queue
from socketserver import ThreadingTCPServer, TCPServer, BaseRequestHandler
from protocol.ModuleProtocol import *
from gaea.config import system_params
from utils.bytes import *
from utils.logger import SingleLogger
from hw.devices import DevicesInfo
from ui.MechIIViewer import MechIIViewer

g_client_pool = []      # 客户端IP池， 用于保留连接的IP地址
g_conn_pool = {}        # 连接池，用于操作对应的Socket
g_protocol_pool = {}    # 协议对象池，用于解析对应Socket的协议


class ModuleServerHandler(BaseRequestHandler):
    start_flag = False
    msg = bytearray()


    def setup(self):
        """
        每一个连接建立后的初始化
        :return:
        """
        super().setup()

        g_client_pool.append(self.client_address[0])                                            # 加入客户端IP地址
        g_conn_pool[self.client_address[0]] = self.request                                      # 加入连接池
        g_protocol_pool[self.client_address[0]] = ModuleProtocol(self.client_address[0])        # 加入协议对象池

        #
        # wx.CallAfter(pub.sendMessage, 'socket_setup_event', ip=self.client_address[0])

        # print('socket(%s) setup!' % self.client_address[0])
        single_logger = SingleLogger()
        single_logger.info('socket(%s) setup!' % self.client_address[0])

    def finish(self):
        """
        每一个连接断开后的清理
        :return:
        """
        super().finish()

        print(self.client_address)

        # wx.CallAfter(pub.sendMessage, 'socket_finish_event', ip=self.client_address[0])

        g_client_pool.remove(self.client_address[0])        # 从客户端IP池移除当前IP地址
        del g_conn_pool[self.client_address[0]]             # 清除连接池中当前socket句柄
        del g_protocol_pool[self.client_address[0]]         # 清除协议对象池中当前协议对象

        # print('socket(%s) finish!' % self.client_address[0])
        single_logger = SingleLogger()
        single_logger.info('socket(%s) finish!' % self.client_address[0])

    def handle(self):
        """
        每一次连接请求的处理
        :return:
        """
        super().handle()

        #
        ip = self.client_address[0]

        #
        time.sleep(5)

        # 发送RTC时间同步信息
        module_protocol = g_protocol_pool[self.client_address[0]]
        msg = module_protocol.build_rtc_sync()
        self.request.sendall(msg)

        # 接受各种事件信息
        msg = b''
        try:
            while True:
                # 接受单个数据
                data = self.request.recv(1)
                # print(type(data))
                # print(data)
                # print_bytes(data)
                # print(int(data[0]))
                # print(hex(int(data[0])))

                if int(data[0]) == const.MAGIC_NUMBER:
                    msg += data
                    if self.start_flag:
                        self.start_flag = False
                        # print("start flag = ", self.start_flag)
                        # print("msg = ", msg)
                        # print_bytes(msg)

                        # 解析完整的一条消息
                        g_protocol_pool[self.client_address[0]].parse_data(msg)
                        msg = b''
                    else:
                        self.start_flag = True
                        # print("start flag = ", self.start_flag)

                elif self.start_flag:
                    msg += data
                    # print("msg = ", msg)
                else:
                    continue

        except Exception as e:
            print(e)

        finally:
            print('socket(%s) exit!' % self.client_address[0])


class ModuleTCPServer(ThreadingTCPServer):
    """
    支持端口重置的ThreadingTCPServer
    """
    allow_reuse_address = True              # 设置端口重置
    daemon_threads = True

    def __init__(self, *args, **kwargs):
        """Set up an initially empty mapping between a user' s nickname
        and the file-like object used to send data to that user."""
        super().__init__(*args, **kwargs)


class ModuleServerThread(threading.Thread):
    """
    Module Server 独立线程
    """
    def __init__(self, name, data, event):
        super().__init__(name=name)         # 调用父类(超类)的__init__()方法

        # 初始化日志类
        self.__logger = SingleLogger()

        # 外部通讯参数
        self.__queue = data                 # 用于向外部传输队列数
        self.__event = event                # 用于触发外部事件

        # 控制线程参数初始化
        self.__flag = threading.Event()     # 用于暂停线程的标识
        self.__flag.clear()                 # 设置为False
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()                # 将running设置为True

        # 获取Module Server的IP和Port
        system_config = system_params()
        self.__ip, self.__port = system_config.get_module_server_info()

        self.__logger.debug("ip = %s" % self.__ip)
        self.__logger.debug("port = %s" % self.__port)

    def __del__(self):
        self.__logger.info("__del__")

    def pause(self):
        self.__logger.info("pause module server thread!")
        self.__flag.clear()         # 设置为False, 让线程阻塞

    def resume(self):
        self.__logger.info("resume module server thread!")
        self.__flag.set()           # 设置为True, 让线程停止阻塞， 继续运行

    def stop(self):
        self.__logger.info("stop module server thread!")
        self.__flag.set()           # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()      # 设置为False

    def run(self):
        # 启动Module Server
        server = ModuleTCPServer((self.__ip, self.__port), ModuleServerHandler)

        server_thread = threading.Thread(target=server.serve_forever, name='ModuleServer', daemon=True)
        server_thread.start()

        while self.__running.isSet():
            self.__flag.wait()              # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    # devices_info = {'#1': ['#1-TC397-2222', '#1-H3-3333'], '#2': ['#2-TC397-4444', '#2-H3-5555'], '#3': ['#3-TC397-6666', '#3-H3-7777']}
    # devices_info = {'#1': ['TC397-2222', 'H3-3333'], '#2': ['TC397-4444', 'H3-5555'], '#3': ['TC397-5555', 'H3-6666']}
    # devices_info = {'1111': ['2222', '3333'], '1112': ['4444', '5555']}
    # devices_info = {'1111': ['2222', '3333']}

    devices_info = DevicesInfo()
    devices_info.set_uuid("127.0.0.1", "2001313233223637")
    # devices_info.set_uuid("192.168.1.101", "2001353137626261")
    devices_info.set_uuid("192.168.1.101", "2001333836373665")

    # print("++++++++++++++++++++")
    # print(devices_info.devices_ready())
    # print(devices_info.get_devices_name())
    # print(devices_info.get_uuid())
    # print("--------------------")
    devices_info = devices_info.get_devices_name()
    focus_device = list(devices_info.keys())[0]
    focus_node = devices_info[focus_device][0]
    print("focus_device = ", focus_device)
    print("focus_node = ", focus_node)

    app = wx.App()
    frame = MechIIViewer(devices_info=devices_info,
                         focus_device=focus_device,
                         focus_node=focus_node,
                         parent=None, title='Mech-II', name="DemoFrame", style=wx.DEFAULT_FRAME_STYLE,
                         size=(1920, 1080))
    frame.Center()
    frame.Show()

    # 创建Module Server独立线程
    queue = Queue()
    event = threading.Event()

    thread = ModuleServerThread("ModuleServer", queue, event)
    thread.start()

    app.MainLoop()
    pass

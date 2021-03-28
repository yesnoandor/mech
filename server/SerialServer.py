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
import threading
from gaea.config import system_params
from hw.tty import tty


class SerialServerThread(threading.Thread):
    """
       Serial 服务器
           1. Echo 功能
           2. Power 控制功能
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
        self.__device, self.__bps = self.__system_config.get_serial_server_info()
        print("device = ", self.__device)
        print("bps = ", self.__bps)

        # 串口的初始化
        self.__tty = tty(port=self.__device, bps=self.__bps)

        # 获取Serial服务器的运行方式
        self.__policy = self.__system_config.get_serial_server_protocol()

        # 服务器不同的协议处理方式
        self.__serial_server_protocol_treat = {"echo": self.echo, "power": self.monitor}

    def __del__(self):
        print("__del__")

    def pause(self):
        print("pause serial server thread!")
        self.__flag.clear()         # 设置为False, 让线程阻塞

    def resume(self):
        print("resume serial server thread!")
        self.__flag.set()           # 设置为True, 让线程停止阻塞

    def stop(self):
        print("stop serial server thread!")
        self.__flag.set()           # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()      # 设置为False

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()              # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

            # 根据不同的配置，CAN Server不同的协议处理方式 (默认echo模式)
            self.__serial_server_protocol_treat.get(self.__policy, self.echo)()

    def echo(self):
        pass

    def power(self):
        pass

    def parse(self, msg):
        print(type(msg))
        pass


if __name__ == '__main__':
    pass

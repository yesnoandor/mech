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

from queue import Queue
import threading
from utils.logger import logger
from utils.logger import SingleLogger
from gaea.config import system_params
from ui.MechIIApp import MechIIApp
from server.ModuleServer import ModuleServerThread
from server.CanServer import CANServerThread


if __name__ == '__main__':
    single_logger = SingleLogger()
    single_logger.info('--主线程开始--')
    single_logger.debug('debug')
    single_logger.info('info')
    single_logger.warning('warning')
    single_logger.error('error')
    single_logger.critical('critical')

    app = MechIIApp()

    queue = Queue()
    event = threading.Event()

    # 创建Module Server独立线程
    module_server_thread = ModuleServerThread("ModuleServer", queue, event)
    module_server_thread.start()

    # 创建CAN Server独立线程
    system_config = system_params()
    vid, pid = system_config.get_can_analyzer_info()
    print("pid = ", pid)
    print("vid = ", vid)
    if vid != 0 and pid != 0:
        can_server_thread = CANServerThread("CANServer", queue, event)
        can_server_thread.start()

    app.MainLoop()





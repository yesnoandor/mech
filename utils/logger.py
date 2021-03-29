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
import logging
import colorlog


class logger(logging.Logger):
    """
    日志管理类
        1. 支持console和文件双输出
        2. console支持多颜色输出
    """
    def __init__(self):
        # 默认的日志路径和名字
        self.__filename = "log/mech-II.log"

        # 默认的色彩表
        self.__colors_table = {
            'DEBUG': 'green',
            'INFO': 'blue',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }

        super(logger, self).__init__( self.__filename)

        # 日志文件的输出格式
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S'
        )

        # 控制台的输出格式
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=self.__colors_table
        )

        # 创建一个handler，用于输出到文件
        file_handler = logging.FileHandler(self.__filename, encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)

        # 创建一个handler，用于输出到控制台
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(console_formatter)
        stream_handler.setLevel(logging.DEBUG)

        # 给logger添加handler
        self.addHandler(file_handler)
        self.addHandler(stream_handler)


class SingleLogger:
    """
    单例模式的日志管理
    """
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwd):
        if SingleLogger.__instance is None:
            SingleLogger.__instance = logger()
        return SingleLogger.__instance


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    single_logger = SingleLogger()

    single_logger.debug('debug')
    single_logger.info('info')
    single_logger.warning('warning')
    single_logger.error('error')
    single_logger.critical('critical')
    pass

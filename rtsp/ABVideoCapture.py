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



Created on


@author: wenyu_xu
@mail:wenyu__xu@163.com

"""


import os
import gc
import abc
from abc import *
from multiprocessing import Process, Manager
import cv2


class ABVideoCapture(abc.ABC):
    """
    视频捕捉的抽象基类  (abc.ABC ：声明抽象基类)
    """
    def __init__(self, cam, top=100):
        """
        :param cam: rtsp视频流源网址  （rtsp://192.168.1.100:8554/stream）
        :param top: 共享缓冲栈容器中最大的帧数
        """
        # 创建一个 Manager 对象， 该对象控制一个服务器进程，可以获取共享缓冲栈
        self.stack = Manager().list()
        # 获取共享缓冲栈容器中最大的帧数
        self.max_cache = top
        # 创建一个 Process 对象
        self.write_process = Process(target=self.__class__.write, args=(self.stack, cam, top))
        # 创建子进程
        self.write_process.start()
        # 生成器函数
        self.__read_gen = self.read_gen()

    @abc.abstractmethod
    def process_image(self, image):
        """
        对输入的图片进行处理并返回处理后的图片 (abc.abstractmethod ：强制子类实现父类中指定的一个方法)
        """
        pass

    def read_gen(self):
        """
        生成器函数, 可以一个一个的生成经过自定义算法处理过后的缓存栈顶的图片
        """
        while True:
            if len(self.stack) != 0:
                img = self.process_image(self.stack.pop( ))
                yield img

    def read(self):
        """
        读取一帧数据
        """
        try:
            return True, next(self.__read_gen)
        except StopIteration:
            return False, None
        except TypeError:
            raise TypeError('{}.read_gen必须为生成器函数'.format(self.__class__.__name__))

    def __iter__(self):
        """
        实现迭代器协议  （委托生成器）
        yield from + 生成器函数 ： 子生成器，同时也是一个迭代器， 可以把可迭代对象里的每个元素一个一个的yield出来
        """
        yield from self.__read_gen

    def release(self):
        self.write_process.terminate()

    def __del__(self):
        self.release()

    @staticmethod
    def write(stack, cam, top):
        """
        向共享缓冲栈中写入数据
        :param cam:
        :param top:
        :return:
        """
        cap = cv2.VideoCapture(cam)
        while True:
            _, img = cap.read()
            if _:
                stack.append(img)
                # 每到一定容量清空一次缓冲栈
                # 利用gc库，手动清理内存垃圾，防止内存溢出
                if len(stack) >= top:
                    del stack[:]
                    gc.collect()

    def __enter__(self):
        """
        实现上下文管理器协议 __enter__ ： 在with语句出现(实例化对象)时执行
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        实现上下文管理器协议 __exit__ ： 在with语句的代码块执行完毕之后才会执行
        """
        self.release()


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")
    pass

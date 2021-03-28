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


class Relay:
    def __init__(self):
        pass

    @staticmethod
    def on(index):
        """
        得到继电器打开通道的命令
        :param index: 通道号
        :return: 命令列表
        """
        if index < 0x05 or index > 0x00:
            cmd = [0xAA, index, 0x01, 0xA8]
        else:
            cmd = [0xAB, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0xA9],
        return cmd

    @staticmethod
    def off(index):
        """
        得到继电器关闭通道的命令
        :param index: 通道号
        :return: 命令列表
        """
        if index < 0x05 or index > 0x00:
            cmd = [0xAA, index, 0x00, 0xA8]
        else:
            cmd = [0xAB, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA9],
        return cmd


if __name__ == '__main__':
    pass

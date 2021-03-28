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


def hexStringTobytes(string):
    """
    字符串数据转化为bytes类型数据
    :param string:
    :return:
    """
    string = string.replace(" ", "")
    return bytes.fromhex(string)


def bytesToHexString(bs):
    """
    将bytes类型数据转化为字符串
    :param bs:
    :return:
    """
    return ''.join(['%02X' % b for b in bs])


def bytesTobcd(bs):
    """
    将bytes类型数据转化为BCD码
    :param bs:
    :return:
    """
    for char in bs:
        for val in (char >> 4, char & 0xF):
            yield str(val)


def print_bytes(data):
    """
    打印byte类型数据
    :param data:
    :return:
    """
    l = [hex(int(i)) for i in data]
    print(" ".join(l))


if __name__ == '__main__':
    pass

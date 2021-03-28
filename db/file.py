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
import json


class db_file:
    """
    用文件的形式保存日志数据库
    """
    def __init__(self, uuid):
        self.__uuid = uuid

        # 根据uuid创建日志目录
        if not os.path.exists(self.__uuid):
            os.makedirs(self.__uuid)

        # print('uuid = ', self.__uuid)
        pass

    def save(self, event):
        """
        用文件追加的方式，保存事件信息
        :param event:
        :return:
        """
        # print('db_file :: save+++++++++')
        # print('event = ', event)
        for k, v in event.items():
            if k == "mod":
                path = self.__uuid + os.sep + v + '.log'
                # print("log path = ", path)
                try:
                    with open(path, 'a+', encoding='utf-8') as f:
                        content = json.dumps(event) + '\r\n'
                        # print("content = ", content)
                        f.write(content)
                except Exception as e:
                    print(e)
        # print('db_file :: save---------')

    def read(self, module, mode='all'):
        """
        读取文件
        :param module:
        :param mode:
            = "all", 读出所有的记录
            = "info",  读出info等级的记录
            = "warning", 读出warning等级的记录
            = "error", 读出error等级的记录

        :return:
        """
        # print("mode = ", mode)
        path = self.__uuid + os.sep + module + '.log'
        # print("path = ", path)
        # print('db_file :: read+++++++++')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:

                    if mode == 'all':
                        yield line
                    else:
                        print("modew = ", mode)
                        print("line = ", line.strip())
                        print(type(line))
                        event = json.loads(line.strip())
                        print(type(event))
                        print("event = ", event)
                        for k, v in event.items():
                            print("k = ", k)
                            if k == mode:
                                yield line

        except Exception as e:
            print(e)
        print('db_file :: read----------')


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    a = {"date": "20190215092812", "mod": 'AAA', "error": "NET_ERRROR"}
    log_file = db_file("log//abc")
    log_file.save(a)

    for line in log_file.read('AAA', 'warning'):
        print("data=", line)

    for line in log_file.read('AAA'):
        print("data all =", line)
    pass

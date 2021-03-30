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
from utils.db import db_sql_tool


class db_sql:
    """
    用SQLite的形式保存日志数据库
    """
    def __init__(self):
        self.__sql = db_sql_tool("log/mech-II")

    def create_table(self, uuid, name):
        table_name = name + '_' + uuid
        cmd = '''create table if not exists %s(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name text,
                        uuid text,
                        log text,
                        state text,
                        date text
                        )''' % table_name
        # print("cmd = ", cmd)
        self.__sql.execute(cmd)
        pass

    def insert_record(self, uuid, name, state, log, date):
        table_name = name + '_' + uuid
        cmd = "insert into %s (name,uuid,log,state,date) values (?,?,?,?,?);" % table_name
        self.__sql.execute(cmd, (name, uuid, log, state, date))
        pass

    def __del__(self):
        self.__sql.close()


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    sql = db_sql()
    sql.create_table(uuid="2001313233223637", name="EMC_MODULE_ADC0")

    sql.insert_record(uuid="2001313233223637",
                      name="EMC_MODULE_ADC0",
                      log="test error",
                      state="error",
                      date="20210324102523")

    sql.insert_record(uuid="2001313233223637",
                      name="EMC_MODULE_ADC0",
                      log="test error",
                      state="error",
                      date="20210324102530")

    sql.insert_record(uuid="2001313233223637",
                      name="EMC_MODULE_ADC0",
                      log="test error",
                      state="info",
                      date="20210324102536")

    sql.insert_record(uuid="2001313233223637",
                      name="EMC_MODULE_ADC0",
                      log="test error",
                      state="warning",
                      date="20210324102542")


    pass

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
import sqlite3


class db_sql_tool:
    """
    db_sql_tool for sqlite3
    简单数据库工具类
    编写这个类主要是为了封装sqlite，继承此类复用方法
    """
    def __init__(self, filename="mech"):
        """
        初始化数据库，默认文件名 mech.db
        filename：文件名
        """
        self.filename = filename + ".db"
        self.db = sqlite3.connect(self.filename)
        self.c = self.db.cursor()

    def close(self):
        """
        关闭数据库
        """
        self.c.close()
        self.db.close()

    def execute(self, sql, param=None):
        """
        执行数据库的增、删、改
        sql：sql语句
        param：数据，可以是list或tuple，亦可是None
        retutn：成功返回True
        """
        try:
            if param is None:
                self.c.execute(sql)
            else:
                if type(param) is list:
                    self.c.executemany(sql, param)
                else:
                    self.c.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e
        if count > 0:
            return True
        else:
            return False

    def query(self, sql, param=None):
        """
        查询语句
        sql：sql语句
        param：参数,可为None
        retutn：成功返回True
        """
        if param is None:
            self.c.execute(sql)
        else:
            self.c.execute(sql, param)
        return self.c.fetchall()


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    sql = db_sql_tool("log/mech-II")

    cmd = '''create table if not exists EMC_MODULE_ADC0_2001313233223637(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text,
            uuid text,
            log text,
            state text,
            date text
            )'''
    f = sql.execute(cmd)

    # 插入数据
    sql.execute("insert into EMC_MODULE_ADC0_2001313233223637 (name,uuid,log,state,date) values (?,?,?,?,?);",
                [('EMC_MODULE_ADC0', '2001313233223637', 'test error', 'error', '20210324102523'),
                 ('EMC_MODULE_ADC0', '2001313233223637', 'test error', 'error', '20210324102530'),
                 ('EMC_MODULE_ADC0', '2001313233223637', 'test warning', 'warning', '20210324102536'),
                 ('EMC_MODULE_ADC0', '2001313233223637', 'test info', 'info', '20210324102542'),
                 ('EMC_MODULE_ADC0', '2001313233223637', 'test info', 'info', '20210324102548'),
                 ('EMC_MODULE_ADC0', '2001313233223637', 'test warning', 'warning', '20210324102554')])

    # 查询统计数据
    uuid = '2001313233223637'
    cmd = "select COUNT(*) from %s where uuid=?" % "EMC_MODULE_ADC0_2001313233223637"
    res = sql.query(cmd, (uuid, ))

    # 获取查询结果：
    print(res)
    print(res[0][0])

    sql.close()

    pass

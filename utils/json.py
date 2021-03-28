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


def json_bottom_dict(data, dic):
    """
    获取json数据格式中最底层的key，val组成的字典
    :param data:
    :param dic:
    :return:
    """
    if isinstance(data, dict):  # 判断是否是字典类型isinstance 返回True False
        for key in data:
            if isinstance(data[key], dict):  # 如果dic_json[key]依旧是字典类型
                # print("****key--：%s value--: %s" % (key, data[key]))
                json_bottom_dict(data[key], dic)
                # dic[key] = dic_json[key]
            else:
                # print("****key--：%s value--: %s" % (key, data[key]))
                dic[key] = data[key]


if __name__ == '__main__':
    pass

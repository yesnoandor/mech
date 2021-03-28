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


import socket


def test_echo_server():
    client = socket.socket()  # 默认是AF_INET、SOCK_STREAM
    client.connect(("localhost", 9988))
    while True:
        s = input(">>")
        print(s)  # 字符数据
        print(s.encode("utf-8"))  # 把字符数据根据utf-8编码成bytes数据
        client.send(s.encode("utf-8"))

        data = client.recv(1024)
        print("-------")
        print(type(data))
        print(data)
        print(data.decode("utf-8"))  # 把bytes数据根据utf-8转化为字符数据
    client.close()


if __name__ == '__main__':
    test_echo_server()
    pass

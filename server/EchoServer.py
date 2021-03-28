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

import re
import sys
import socket
from socketserver import ThreadingTCPServer, BaseRequestHandler
import threading
from utils.bytes import *


g_client_pool = []   # 客户端IP池
g_conn_pool = []     # 连接池


def main_menu():
    """ 显示主菜单 """

    # 设置高亮,字体为紫色显示
    print("""\033[1;35m
    *********************************************************************
                               Echo 服务器功能
    *********************************************************************
           1. 查看当前在线人数
           2. 给指定客户端发送消息
           3. 给所有客户端发送消息
           4. 发送查询命令
           0. 关闭服务端
    ====================================================================
    说明: 通过数字键选择菜单
    ====================================================================
    \033[0m
    """)


def menu_treat(index_str):
    """ 菜单处理程序 """
    if index_str == '1':
        print("当前在线人数：", len(g_conn_pool))

    elif index_str == '2':
        index, msg = input("请输入“索引,消息”的形式：").split(",")
        g_conn_pool[int(index)].sendall(msg.encode(encoding='utf8'))

    elif index_str == '3':
        msg = input("请输入消息：")
        for conn in g_conn_pool:
            conn.sendall(msg.encode(encoding='utf8'))

    elif index_str == '4':
        data = "hello"
        for conn in g_conn_pool:
            conn.sendall(data)


class EchoHandler(BaseRequestHandler):
    # 每一个连接初始化
    def setup(self):
        super().setup()

        # 加入连接池
        g_client_pool.append(self.client_address[0])
        g_conn_pool.append(self.request)

    # 每一个连接清理
    def finish(self):
        super().finish()

        print(self.client_address)

        g_client_pool.remove(self.client_address[0])
        g_conn_pool.remove(self.request)

    # 每一次请求处理
    def handle(self):
        super().handle()

        try:
            while True:
                # 接受数据
                data = self.request.recv(1024)

                print(type(data))                   # --> <class 'bytes'>
                print_bytes(data)
                print(data.decode("utf-8"))

                msg = '{}{}'.format(self.client_address, data.decode("utf-8")).encode("utf-8")
                print("msg =", msg)

                # 回显收到的数据
                self.request.send(data)
        except Exception as e:
            print(e)

        finally:
            print('=== echo server exit ====')


class EchoServer(ThreadingTCPServer):
    """
    支持端口重置的ThreadingTCPServer
    """
    # allow_reuse_address = True              # 设置支持端口重置
    # daemon_threads = True

    def __init__(self, *args, **kwargs):
        """Set up an initially empty mapping between a user' s nickname
        and the file-like object used to send data to that user."""
        super().__init__(*args, **kwargs)


    def server_bind(self):
        """
        Called by constructor to bind the socket.
        May be overridden.
        设置支持端口重置
        """
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()


def start_echo_server(port=9988):
    server = EchoServer(('127.0.0.1', port), EchoHandler)

    server_thread = threading.Thread(target=server.serve_forever, name='EchoServer', daemon=True)
    server_thread.start()

    try:
        while True:
            main_menu()
            index = input("\033[1;32m 请输入您要操作的菜单选项: \033[0m")  # 设置高亮,字体为绿色显示
            if len(index) != 0:
                index = re.sub(r'\D', "", index[0])
                if '1' <= index <= '4':
                    menu_treat(index)
                    continue
                elif index == '0':
                    print("\033[1;34m 退出Echo服务器! \033[0m")          # 设置高亮,字体为蓝色显示
                    server.shutdown()
                    server.server_close()
                    break
                else:
                    print("\033[1;31m 输入非法,请重新输入! \033[0m")         # 设置高亮,字体为红色显示

            else:
                print("\033[1;31m 输入非法,请重新输入! \033[0m")  # 设置高亮,字体为红色显示

    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    finally:
        print('exit')
        sys.exit(0)
    pass


if __name__ == '__main__':
    start_echo_server(9988)
    pass


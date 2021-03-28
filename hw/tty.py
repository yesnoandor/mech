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

import serial
import time


class tty:
    """
    """

    def __init__(self, port, bps="115200"):
        """

        :param port:
        """
        self.ser = serial.Serial(port=port,
                                 baudrate=bps,
                                 bytesize=8,
                                 parity='N',
                                 stopbits=1,
                                 timeout=0.5)

    def send(self, cmd):
        """
        发送字符串 or bytes
        :param cmd:
        :return:
        """
        if type(cmd) is bytes:
            self.ser.write(cmd)
        else:
            self.ser.write(cmd.encode())
        # print(cmd.encode())
        # time.sleep(0.3)
        self.ser.flush()

    def send_file(self, file):
        """
        发送文件
        :param file:
        :param 文件名:
        :return:
        """
        with open(file, "r") as f:
            if self.ser.isOpen():
                print("program the image : %s " % file)

                count = 0
                for line in f.readlines():
                    if not line:
                        print("%s send over!" % file)
                        break
                    self.ser.write(line.encode())
                    # print(i, "：", flash_line.encode())
                    time.sleep(0.001)
                    self.ser.flush()

                    count = count + 1
                    if count % 100 == 0:
                        # print('count = ', count)
                        print('.', end='', flush=True)

                print('')
                print("program %s successfully !" % file)
            else:
                print("The device serial port is not open")

    def recv(self, timeout=1000):
        """
        接受
        :return:
        """
        start_time = time.time()
        while True:
            end_time = time.time()
            if end_time - start_time > timeout:
                break
            data = self.ser.read(self.ser.inWaiting())
            if not data:
                continue
            else:
                break
        return data


if __name__ == '__main__':
    pass


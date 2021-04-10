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
import binascii
import datetime
from gaea.config import system_params
from Crypto.Cipher import AES
from crypt.AesCrypt import AesCrypt


def aes_decrypt():
    system_config = system_params()
    license_eth = system_config.get_license_eth()
    license_path = system_config.get_license_path()
    file_path = license_path + os.sep + "license.lic"
    print("file path = ", file_path)

    mac_info = system_config.get_eth_mac(license_eth)

    date = datetime.datetime.now()
    detester = date.strftime('%Y-%m-%d')

    passwd = "j1w#E~n0y^U4X7uI:"
    iv = '1111111111111111'
    aescryptor = AesCrypt(passwd, AES.MODE_CBC, iv)  # CBC模式
    # aescryptor = Aescrypt(passwd,AES.MODE_ECB,"") # ECB模式

    with open(file_path, "rb") as licFile:
        encryptText = licFile.read()
        licFile.close()

    text = aescryptor.aesdecrypt(encryptText)

    mac_info, detester = str(text, encoding='utf-8').split('_')
    date = datetime.datetime.strptime(detester, '%Y-%m-%d')
    print("mac_info = ", mac_info)
    print("detester = ", detester)
    print("date = ", date)
    print(type(date))

    return mac_info, date


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    system_config = system_params()
    license_eth = system_config.get_license_eth()
    print("license_eth = ", license_eth)
    license_path = system_config.get_license_path()
    print("license_path = ", license_path)

    file_path = license_path + os.sep + "license.lic"
    print("file path = ", file_path)

    mac_info = system_config.get_eth_mac(license_eth)
    print("mac info = ", mac_info)

    data = mac_info
    print(data)
    data = binascii.b2a_hex(data.encode("utf8"))        # 字符串 --> 十六进制
    datas = data.decode(encoding='utf-8')
    print(type(data))
    print(data)
    print(type(datas))
    print(datas)

    text = binascii.a2b_hex(datas)                      # 十六进制 --> 字符串
    print(type(text))
    print(text)
    text = text.decode(encoding='utf-8')
    print(type(text))
    print(text)
    pass

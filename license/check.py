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
import time
import ntplib
from utils import const
from utils.logger import SingleLogger
from gaea.config import system_params
from license.decrypt import aes_decrypt


const.EXPIRATION = 31536000


def mac_verify(mac):
    system_config = system_params()
    license_eth = system_config.get_license_eth()
    print("license_eth = ", license_eth)

    mac_info = system_config.get_eth_mac(license_eth)
    if mac == mac_info:
        return True
    return False


def date_verify(date):
    c = ntplib.NTPClient()
    ntp_server_list = ['cn.ntp.org.cn', 'pool.ntp.org', 'cn.pool.ntp.org', 'ntp1.aliyun.com', 'ntp2.aliyun.com']
    for server in ntp_server_list:
        try:
            response = c.request(server)
            break
        except Exception as e:
            print("Exception server = ", server)
            print(e)
    ts = response.tx_time
    seconds = time.mktime(date.timetuple())
    diff = ts - seconds
    if diff > const.EXPIRATION:
        return False

    return True


def license_verify():
    logger = SingleLogger()

    mac_info, date = aes_decrypt()

    if not mac_verify(mac_info):
        logger.error("使用MAC地址无法通过校验")
        return False

    if not date_verify(date):
        logger.error("使用期限已过期")
        return False

    logger.info("校验已通过，请放心使用")
    return True


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    status = license_verify()
    print("license status = ",  status)

    pass

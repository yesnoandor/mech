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
import psutil
from utils.json import *
from utils.logger import SingleLogger
from kylin.default import DEFAULT_SYSTEM_CONFIG


class system_params:
    """
    系统默认配置
    """
    def __init__(self, file="kylin/config.json"):
        self.__logger = SingleLogger()

        self._cfg = DEFAULT_SYSTEM_CONFIG
        path = os.getcwd() + "/" + file
        # print("path = ", path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    self._cfg = json.load(f)
                    # print(self._cfg)
                except Exception as e:
                    print(e)
                    self._cfg = DEFAULT_SYSTEM_CONFIG
        except Exception as e:
            print(e)
            self._cfg = DEFAULT_SYSTEM_CONFIG

        # 获取各个网卡的mac地址
        self.__mac_dict = dict()
        dic = psutil.net_if_addrs()
        # print("dic = ", dic)
        for adapter in dic:
            # print("adapter = ", adapter)
            sniclist = dic[adapter]
            for snic in sniclist:
                # print(type(snic))
                # print("snic = ", snic)
                # print(snic.address)
                self.__mac_dict[adapter] = snic.address
        # print(self.__mac_dict)

        # self.__logger.info('configuration = {}'.format(self._cfg))

    def get_module_server_info(self):
        """
        获取module server的IP和Port
        :return:
        """
        ip = self._cfg['module_server']['ip']
        port = int(self._cfg['module_server']['port'])

        return ip, port

    def get_module_monitor_name(self):
        """
        获取module server必须的监控模块
        :return:
        """
        modules = []
        dic = {}

        json_module = self._cfg.get('modules_monitor', None)

        if json_module is not None:
            json_bottom_dict(json_module, dic)
            # print(dic)
            for k, v in dic.items():
                modules += v

        return modules

    def get_devices_info(self):
        """
        获取接入服务器的设备基础信息
        :return:
        """
        devices_info = self._cfg['devices_info']

        return devices_info

    def get_can_protocol(self):
        # print("can server protocol = %s" % self._cfg['can_server']['protocol'])
        return self._cfg['can_server']['protocol']

    def get_can_analyzer_info(self):
        """
        获取CAN分析仪的USB设备VID，PID
        :return:
        """
        vid = pid = 0
        if 'can_server' in self._cfg.keys():
            vid = int(self._cfg['can_server']['can_analyze']['vendor_id'], 16)        # 字符转化为16进制整数
            pid = int(self._cfg['can_server']['can_analyze']['product_id'], 16)       # 字符转化为16进制整数

        return vid, pid

    def get_can_module_count(self):
        """
        获取总共监控CAN Module的数量
        :return:
        """
        return len(self._cfg['can_server']['can_module'])

    def get_can_module_info(self, index):
        """
        获取单组CAN Module的CANID信息
        :param index:
        :return:
        """
        can_index = "CAN{}".format(index+1)
        return self._cfg['can_server']['can_module'][can_index]

    def get_can_all_module_info(self):
        """
        获取单组CAN Module的CANID信息
        :param index:
        :return:
        """
        return self._cfg['can_server']['can_module']

    def get_can_tx_id(self, rx_id):
        """
        根据CANFD的RX-ID，绑定的TX-ID
        :param rx_id:
        :return:
        """
        tx_id = 0
        count = self.get_can_module_count()
        for i in range(count):
            info = self.get_can_module_info(i)
            if int(info['rx_id'], base=16) == rx_id:
                tx_id = int(info['tx_id'], base=16)
                break

        return tx_id

    def get_serial_server_info(self):
        device = self._cfg['serial_server']['device']
        bps = int(self._cfg['serial_server']['bps'])

        return device, bps

    def get_serial_server_protocol(self):
        print("serial server protocol = %s" % self._cfg['serial_server']['protocol'])
        return self._cfg['serial_server']['protocol']

    def get_eth_mac(self, eth_name):
        """
        获取已知网卡名的mac地址
        :param eth_name:
        :return:
        """
        return self.__mac_dict[eth_name] if eth_name in self.__mac_dict.keys() else ""

    def get_license_eth(self):
        return self._cfg['license']['eth']

    def get_license_path(self):
        return self._cfg['license']['path']


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    system_config = system_params()

    ip, port = system_config.get_module_server_info()
    print("ip = ", ip)
    print("port = ", port)

    modules = system_config.get_module_monitor_name()
    print("modules = ", modules)

    device, bps = system_config.get_serial_server_info()
    print("device = ", device)
    print("bps = ", bps)

    protocol = system_config.get_serial_server_protocol()
    print("serial server protocol = ", protocol)

    devices_info = system_config.get_devices_info()
    print("devices_info = ", devices_info)

    vendor_id, product_id = system_config.get_can_analyzer_info()
    print("vendor_id = %#x" % vendor_id)
    print("product_id = %#x" % product_id)

    protocol = system_config.get_can_protocol()
    print("can server protocol = %s" % protocol)

    can_tx_id = system_config.get_can_tx_id(0x81)
    print("can_tx_id = %#x" % can_tx_id)

    can_node_info = system_config.get_can_all_module_info()
    print("can_node_info = ", can_node_info)
    can_node_info['CAN1']['index'] = 1
    can_node_info['CAN1']['chanel'] = 1
    can_node_info['CAN1']['uuid'] = "1234"
    print("can_node_info = ", can_node_info)

    license_eth = system_config.get_license_eth()
    print("license_eth = ", license_eth)
    license_path = system_config.get_license_path()
    print("license_path = ", license_path)
    mac = system_config.get_eth_mac(license_eth)
    print("mac = ", mac)
    pass

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
from gaea.config import system_params
from utils.json import json_bottom_dict


class DevicesInfo:
    """
    所有的设备节点信息

    {
        '#1': {
            'TC397': {
                'ip': '127.0.0.1', 'modules_monitor': {
                    'MODULE_CAN': ['EMC_MODULE_CAN0', 'EMC_MODULE_CAN1', 'EMC_MODULE_CAN2', 'EMC_MODULE_CAN3', 'EMC_MODULE_CAN4', 'EMC_MODULE_CAN5', 'EMC_MODULE_CAN6'], 'MODULE_ADC': ['EMC_MODULE_ADC0', 'EMC_MODULE_ADC1', 'EMC_MODULE_ADC2', 'EMC_MODULE_ADC3', 'EMC_MODULE_ADC4', 'EMC_MODULE_ADC5', 'EMC_MODULE_ADC6', 'EMC_MODULE_ADC7'], 'MODULE_SENSOR': ['EMC_MODULE_SENSOR_INA', 'EMC_MODULE_SENSOR_TMP0', 'EMC_MODULE_SENSOR_TMP1', 'EMC_MODULE_SENSOR_TMP2', 'EMC_MODULE_SENSOR_TMP3']
                },
                'uuid': '2001313233223637'
            },
            'H3': {
                'ip': '192.168.1.101', 'modules_monitor': {
                    'MODULE_CAN': ['EMC_MODULE_CAN8', 'EMC_MODULE_CAN9']
                },
                'uuid': '1234567890121111'
            }
        }
    }


    """
    __devices_info = {}
    __devices_name = {}
    __devices_uuid = []

    def __init__(self):
        system_config = system_params()
        if not DevicesInfo.__devices_info:
            DevicesInfo.__devices_info = system_config.get_devices_info()
        # self.__devices_info = system_config.get_devices_info()
        # self.__devices_name = {}
        # self.__devices_uuid = []

    '''
    def get_uuid(self, ip):
        for device_name, device_info in DevicesInfo.__devices_info.items():
            # print(device_name)
            # print(device_info)
            for node_name, node_info in device_info.items():
                # print("node name = ", node_name)
                # print("node info = ", node_info)
                if node_info['ip'] == ip:
                    uuid = node_info.get('uuid', None)
                    return uuid
    '''

    def set_uuid(self, ip, uuid):
        # print("set uuid ++++++++++")
        # print(self.__devices_info)
        # for device_name, device_info in self.__devices_info.items():
        for device_name, device_info in DevicesInfo.__devices_info.items():
            # print(device_name)
            # print(device_info)
            for node_name, node_info in device_info.items():
                # print("node name = ", node_name)
                # print("node info = ", node_info)
                if node_info['ip'] == ip:
                    node_info['uuid'] = uuid
                    DevicesInfo.__devices_uuid.append(node_info['uuid'])
        # print(self.__devices_info)
        # print("DevicesInfo.__devices_info = ", DevicesInfo.__devices_info)
        # print("set uuid ----------")

    def devices_ready(self):
        for device_name, device_info in DevicesInfo.__devices_info.items():
            for node_name, node_info in device_info.items():
                if 'uuid' not in node_info.keys():
                    return False

        return True

    def get_devices_name(self):
        for device_name, device_info in DevicesInfo.__devices_info.items():
            # print(device_name)
            # print(device_info)

            node_list = []
            for node_name, node_info in device_info.items():
                # print(node_name)
                # print(node_info)
                node_list.append(node_name + '-' + node_info['uuid'][-4:])
                # print("node = ", node_list)

            # self.__devices_name[device_name] = node_list
            DevicesInfo.__devices_name[device_name] = node_list

            # devices_info = {'#1': ['TC397-2222', 'H3-3333'], '#2': ['TC397-4444', 'H3-5555'],
            #                '#3': ['TC397-5555', 'H3-6666']}

        # print(self.__devices_name)
        # return self.__devices_name
        return DevicesInfo.__devices_name

    def get_uuid_from_ip(self, ip):
        for device_name, device_info in DevicesInfo.__devices_info.items():
            # print("device_name = ", device_name)
            # print("device_info = ", device_info)
            for node_name, node_info in device_info.items():
                if 'uuid' not in node_info.keys():
                    return None
                if node_info['ip'] == ip:
                    return node_info['uuid']
        pass

    def get_uuid(self):
        uuid = []
        for device_name, device_info in DevicesInfo.__devices_info.items():
            for node_name, node_info in device_info.items():
                # print(node_info)
                if 'uuid' in node_info.keys() :
                    # self.__devices_uuid.append(node_info['uuid'])
                    uuid.append(node_info['uuid'])
        # return self.__devices_uuid
        # print("DevicesInfo.__devices_info = ", DevicesInfo.__devices_info)
        # print("DevicesInfo.__devices_uuid = ", DevicesInfo.__devices_uuid)
        return uuid

    def get_device_info(self):
        return DevicesInfo.__devices_info

    def get_module_monitor_name_from_ip(self, ip):
        """
        获取module server必须的监控模块
        :return:
        """
        modules = []
        dic = {}

        for device_name, device_info in DevicesInfo.__devices_info.items():
            for node_name, node_info in device_info.items():
                if node_info['ip'] == ip:
                    json_module = node_info.get('modules_monitor', None)

                    if json_module is not None:
                        json_bottom_dict(json_module, dic)
                        # print(dic)
                        for k, v in dic.items():
                            modules += v
                            return modules

        return modules

    def get_module_monitor_name_from_uuid(self, uuid):
        """
        获取module server必须的监控模块
        :return:
        """
        modules = []
        dic = {}

        for device_name, device_info in DevicesInfo.__devices_info.items():
            for node_name, node_info in device_info.items():
                if node_info['uuid'] == uuid:
                    json_module = node_info.get('modules_monitor', None)

                    if json_module is not None:
                        json_bottom_dict(json_module, dic)
                        # print(dic)
                        for k, v in dic.items():
                            modules += v
                            return modules

        return modules


# os.chdir("../")
# print(os.getcwd())
# devices_params = DevicesInfo()
# print(os.getcwd())

if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")
    #print(os.getcwd())

    devices_info = DevicesInfo()
    print(devices_info.get_uuid_from_ip("192.168.1.100"))
    devices_info.set_uuid("127.0.0.1", "2001313233223637")
    devices_info.set_uuid("192.168.1.101", "1234567890121111")
    devices_info.set_uuid("192.168.1.102", "1234567890122222")
    devices_info.set_uuid("192.168.1.103", "1234567890123333")
    devices_info.set_uuid("192.168.1.104", "1234567890124444")
    devices_info.set_uuid("192.168.1.105", "1234567890125555")
    print(devices_info.devices_ready())
    print(devices_info.get_uuid_from_ip("192.168.1.100"))
    print("------------------------------------")
    print(devices_info.get_devices_name())
    print(devices_info.get_uuid())
    print("------------------------------------")
    print(devices_info.get_module_monitor_name_from_ip("127.0.0.1"))
    print(devices_info.get_module_monitor_name_from_ip("192.168.1.101"))
    print(devices_info.get_module_monitor_name_from_uuid("2001313233223637"))
    print(devices_info.get_module_monitor_name_from_uuid("1234567890121111"))

    devices_info2 = DevicesInfo()
    print("get_uuid = ", devices_info2.get_uuid())
    print("from ip = ", devices_info2.get_uuid_from_ip("192.168.1.100"))
    print(devices_info2.get_device_info())

    pass

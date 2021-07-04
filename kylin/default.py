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

from utils import const


DEFAULT_SYSTEM_CONFIG = {
    # 当前Module Server的地址和IP
    "module_server": {
        "ip": "127.0.0.1",               # 192.168.1.105
        "port": 9988
    },

    # 当前Module Server必须监控的模块
    "modules_monitor": {
        "MODULE_CAN": [
            "EMC_MODULE_CAN0",
            "EMC_MODULE_CAN1",
            "EMC_MODULE_CAN2",
            "EMC_MODULE_CAN3",
            "EMC_MODULE_CAN4",
            "EMC_MODULE_CAN5",
            "EMC_MODULE_CAN6",
        ],
        "MODULE_ADC": [
            "EMC_MODULE_ADC0",
            "EMC_MODULE_ADC1",
            "EMC_MODULE_ADC2",
            "EMC_MODULE_ADC3",
            "EMC_MODULE_ADC4",
            "EMC_MODULE_ADC5",
            "EMC_MODULE_ADC6",
            "EMC_MODULE_ADC7"
        ],
        "MODULE_SENSOR": [
            "EMC_MODULE_SENSOR_INA",
            "EMC_MODULE_SENSOR_TMP0",
            "EMC_MODULE_SENSOR_TMP1",
            "EMC_MODULE_SENSOR_TMP2",
            "EMC_MODULE_SENSOR_TMP3"
        ]
    },

    # 接入设备的基础信息
    "devices_info": {
        "#1": [{
            "TC397": {
                "ip": "192.168.1.100",

                "modules_monitor": {
                    "MODULE_CAN": [
                        "EMC_MODULE_CAN0",
                        "EMC_MODULE_CAN1",
                        "EMC_MODULE_CAN2",
                        "EMC_MODULE_CAN3",
                        "EMC_MODULE_CAN4",
                        "EMC_MODULE_CAN5",
                        "EMC_MODULE_CAN6"
                    ],
                    "MODULE_ADC": [
                        "EMC_MODULE_ADC0",
                        "EMC_MODULE_ADC1",
                        "EMC_MODULE_ADC2",
                        "EMC_MODULE_ADC3",
                        "EMC_MODULE_ADC4",
                        "EMC_MODULE_ADC5",
                        "EMC_MODULE_ADC6",
                        "EMC_MODULE_ADC7"
                    ],
                    "MODULE_SENSOR": [
                        "EMC_MODULE_SENSOR_INA",
                        "EMC_MODULE_SENSOR_TMP0",
                        "EMC_MODULE_SENSOR_TMP1",
                        "EMC_MODULE_SENSOR_TMP2",
                        "EMC_MODULE_SENSOR_TMP3"
                    ]
                }
            },
            "TDA4": {
                "ip": "192.168.1.101"
            }
        }],
    }
}


if __name__ == '__main__':
    pass

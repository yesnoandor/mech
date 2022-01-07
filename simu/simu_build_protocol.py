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
import datetime
import json
import random
from utils.bytes import *


def build_heart_beat_bin(module_protocol):
    header = module_protocol.build_header(const.HEART_BEAT_UPLOAD, 0)
    heart_beat_bin = module_protocol.build_bin(header, b'')
    # print(heart_beat_bin)
    return heart_beat_bin


def build_system_info_bin(module_protocol, start_time):
    system_info = {"system":
                       {"version":
                            {"sw": "1.0",
                             "hw": "2.0"
                             },
                        "temperature": "56.4",
                        "cpu":
                            {"cpu0": "78",
                             "cpu1": "29",
                             "cpu2": "100",
                             "cpu3": "84",
                             "cpu4": "37",
                             "cpu5": "56",
                             "cpu6": "82",
                             "cpu7": "67",
                             },
                        "memory":
                            {"total": "2048M",
                             "used": "1024M"
                             },
                        "network":
                            {"tx": "86.2",
                             "rx": "0.0"
                             },
                        "uptime": "1:24:56:20"
                        }
                   }
    print(system_info)

    # 模拟 CPU 占用率
    cpu_utilization = []
    for i in range(8):
        # 随机产生8个0-100浮点数，作为CPU占有率
        cpu_utilization.append(random.uniform(0, 100))
    print(cpu_utilization)

    # 模拟 MEMORY 占用率
    memory_utilization = ['64M', '128M', '256M', '512M', '1024M', '1280M', '1408M', '1536M', '2048M']

    # 模拟网速
    network_speed_tx = round(60.0 + random.uniform(0, 20), 2)
    network_speed_rx = round(5.0 + random.uniform(0, 5), 2)

    end_time = datetime.datetime.now()

    # 转化为ms间隔
    interval_ms = ((end_time - start_time).seconds * 1000 + (end_time - start_time).microseconds / 1000)
    ms = interval_ms % 1000
    remain = interval_ms // 1000
    sec = remain % 60
    remain = remain // 60
    min = remain % 60
    hour = remain // 60

    print(start_time)
    print(end_time)
    print("interval = ", interval_ms)
    print("ms = ", ms)
    print("sec = ", sec)
    print("min = ", min)
    print("hour = ", hour)

    # 填充模拟系统信息
    system_info['system']['version'] = {'sw': '2.3', 'hw': '1.0'}
    system_info['system']['temperature'] = int(random.randint(24, 90))
    system_info['system']['cpu'] = {'cpu0': str(cpu_utilization[0]), 'cpu1': str(cpu_utilization[1]),
                                    'cpu2': str(cpu_utilization[2]), 'cpu3': str(cpu_utilization[3]),
                                    'cpu4': str(cpu_utilization[4]), 'cpu5': str(cpu_utilization[5]),
                                    'cpu6': str(cpu_utilization[6]), 'cpu7': str(cpu_utilization[7])}
    system_info['system']['memory'] = {'total': '2048M', 'used': random.choice(memory_utilization)}
    system_info['system']['network']['tx'] = str(network_speed_tx)
    system_info['system']['network']['rx'] = str(network_speed_rx)
    system_info['system']['uptime'] = "%d:%02d:%02d:%03d" % (hour, min, sec, ms)
    jsoninfo = json.dumps(system_info)
    # print(type(jsoninfo))
    # print(jsoninfo)
    body = jsoninfo.encode("utf-8")
    print("---------------------------------")
    print(body)

    header = module_protocol.build_header(const.SYSTEM_INFO_UPLOAD, len(body))
    system_info_bin = module_protocol.build_bin(header, body)
    print_bytes(system_info_bin)

    return system_info_bin


"""
def build_event_info_bin(module_protocol):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    cmd = {
        "event":
            [
                # CAN info
                {"date": now, "mod": "EMC_MODULE_CAN0", "info": "STATUS_OK"},
                {"date": now, "mod": "EMC_MODULE_CAN1", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN2", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN3", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN4", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN5", "warning": "warning"},
                {"date": now, "mod": "EMC_MODULE_CAN6", "error": "error"},
                # ADC info
                {"date": now, "mod": "EMC_MODULE_ADC0", "error": "error"},
                {"date": now, "mod": "EMC_MODULE_ADC1", "warning": "warning"},
                {"date": now, "mod": "EMC_MODULE_ADC2", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC3", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC4", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC5", "warning": "4V"},
                {"date": now, "mod": "EMC_MODULE_ADC6", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC7", "info": "5V"},
                # sensor
                {"date": now, "mod": "EMC_MODULE_SENSOR_INA", "info": "Do H3 Sensor test,temp: 53.437000"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP0", "info": "Do H3 Sensor test,temp: 52.437000"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP1", "error": "error"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP2", "warning": "error"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP3", "info": "OK"},


            ]
        }

    # cmd["event"]["date"] = now
    jsoninfo = json.dumps(cmd)
    body = jsoninfo.encode("utf-8")
    header = module_protocol.build_header(const.MODULE_EVENT_UPLOAD, len(body))     # 构建msg
    event_info_bin = module_protocol.build_bin(header, body)

    return event_info_bin
"""


def build_event_info_bin(module_protocol):
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    cmd = {
        "event":
            [
                # CAN info
                {"date": now, "mod": "EMC_MODULE_CAN0", "info": "STATUS_OK"},
                {"date": now, "mod": "EMC_MODULE_CAN1", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN2", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN3", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN4", "info": "OK"},
                {"date": now, "mod": "EMC_MODULE_CAN5", "warning": "warning"},
                {"date": now, "mod": "EMC_MODULE_CAN6", "error": "error"},
                # ADC info
                {"date": now, "mod": "EMC_MODULE_ADC0", "error": "error"},
                {"date": now, "mod": "EMC_MODULE_ADC1", "warning": "warning"},
                {"date": now, "mod": "EMC_MODULE_ADC2", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC3", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC4", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC5", "warning": "4V"},
                {"date": now, "mod": "EMC_MODULE_ADC6", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC7", "info": "5V"},
                # sensor
                {"date": now, "mod": "EMC_MODULE_SENSOR_INA", "info": "Do H3 Sensor test,temp: 53.437000"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP0", "info": "Do H3 Sensor test,temp: 52.437000"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP1", "error": "error"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP2", "warning": "error"},
                {"date": now, "mod": "EMC_MODULE_SENSOR_TMP3", "info": "OK"},
            ]
    }

    '''
    cmd = {
        "event":
            [
                # ADC info
                {"date": now, "mod": "EMC_MODULE_ADC2", "info": "5V"},
                {"date": now, "mod": "EMC_MODULE_ADC3", "info": "5V"}
            ]
    }
    '''

    # cmd["event"]["date"] = now
    jsoninfo = json.dumps(cmd)
    body = jsoninfo.encode("utf-8")
    header = module_protocol.build_header(const.MODULE_EVENT_UPLOAD, len(body))
    event_info_bin = module_protocol.build_bin(header, body)

    return event_info_bin


if __name__ == '__main__':
    pass

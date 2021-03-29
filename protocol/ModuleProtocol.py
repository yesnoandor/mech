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


import wx
import json
import struct
import datetime
import binascii
# import logging
from utils import const
from utils.bytes import *
from utils.crc import *
from utils.logger import SingleLogger
from hw.devices import DevicesInfo
from random import choice
from random import random
from pubsub import pub
from db.file import db_file


const.MAGIC_NUMBER = 0x7e
const.ESCAPE_NUMBER = 0x7d
const.ESCAPE_ESCAPE_NUMBER = 0x01
const.ESCAPE_MAGIC_NUMBER = 0x02

const.GWM_VENDOR_ID = 0x20
const.L2_DEVICE_ID = 0x01
const.L3_DEVICE_ID = 0x02
const.L4_DEVICE_ID = 0x03

const.HEART_BEAT_UPLOAD = 0x0001
const.MODULE_EVENT_UPLOAD = 0x0002
const.SYSTEM_INFO_UPLOAD = 0x0100

const.RTC_SYNC = 0x8004
const.SETTING_DOWNLOAD = 0x8005


class ModuleProtocol:
    """
    Module Server 的协议解析
    """
    def __init__(self, ip='127.0.0.1', serial_id=bytearray([0, 0, 0, 0, 0, 0])):
        """
        构造方法, 初始化变量
        :param ip: 默认的客户端IP
        """
        #
        self.__ip = ip
        self.__uuid = ""

        # 初始化日志类
        self.__logger = SingleLogger()

        # 初始化设备日志
        self.__device_logger = None
        # self.__device_logger = LogFile("12345678")

        # 初始化需要发布的消息
        self.__pub_module_info_msg_name = "module_info_event"       # module信息传输触发事件
        self.__pub_system_info_msg_name = "system_info_event"       # system信息传输触发事件
        self.__pub_device_ready_msg_name = "device_node_ready"      # 设备准备好触发事件

        # print("pub module info : ", self.__pub_module_info_msg_name)
        # print("pub system info : ", self.__pub_system_info_msg_name)
        # print("pub device ready : ", self.__pub_device_ready_msg_name)

        self.__system_info = {"version": {},
                              "temperature": {},
                              "memory": {},
                              "cpu": {},
                              "storage": {},
                              "socket": {},
                              'uuid': {},
                              'uptime': {}
                              }

        self.vendor_id = const.GWM_VENDOR_ID            # 默认厂商号
        self.product_id = const.L2_DEVICE_ID
        self.serial_id = serial_id
        self._serial_number = 0                         # 发送序列号，依次递增
        pass

    @staticmethod
    def escape(data):
        """
        转义处理
        :param data: 原始的bytearray
        :return:
        """
        escape_bin = bytearray()
        # print(type(data))
        for byte in data:  # 将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列
            if byte == 0x7d:
                escape_bin.append(0x7d)
                escape_bin.append(0x01)
                pass
            elif byte == 0x7e:
                escape_bin.append(0x7d)
                escape_bin.append(0x02)
                pass
            else:
                escape_bin.append(byte)
                pass

        return escape_bin

    @staticmethod
    def unescape(data):
        """
        反转义处理
        :param data:
        :return:
        """
        unescape_bin = bytearray()

        flag = False
        for byte in data:
            if flag:
                if byte == 0x01:
                    unescape_bin.append(0x7d)
                else:
                    unescape_bin.append(0x7e)
                flag = False

            elif byte == 0x7d:
                flag = True
            else:
                unescape_bin.append(byte)

        return unescape_bin

    @staticmethod
    def build_inquiry_body():
        """
        构建查询指令
        :return:
        """
        cmd = {"system": ["version", "temperature", "cpu", "memory"]}
        # print(cmd)
        jsoninfo = json.dumps(cmd)
        # print(type(jsoninfo))
        # print(jsoninfo)
        body = jsoninfo.encode("utf-8")
        # print(type(body))
        # print_hex(body)
        return body

    @staticmethod
    def build_rtc_sync_body():
        """
        构建时钟同步消息体
        :return:
        """
        now = datetime.datetime.now()
        cmd = {
            'Setting': {"MOD_RTC":
                            {"year": now.year,
                             "month": now.month,
                             "day": now.day,
                             "hour": now.hour,
                             "min": now.minute,
                             "sec": now.second
                             }
                        }
        }
        jsoninfo = json.dumps(cmd)
        # print(type(jsoninfo))
        # print(jsoninfo)
        body = jsoninfo.encode("utf-8")
        # print(type(body))
        # print_bytes(body)
        return body

    @staticmethod
    def build_adc_setting_body():
        now = datetime.datetime.now()
        cmd = {
            "Setting":
                {"MOD_RTC":
                    {
                        "year": now.year,
                        "month": now.month,
                        "day": now.day,
                        "hour": now.hour,
                        "min": now.hour,
                        "sec": now.second
                    }
                }
        }
        jsoninfo = json.dumps(cmd)
        # print(type(jsoninfo))
        # print(jsoninfo)
        body = jsoninfo.encode("utf-8")
        # print(type(body))
        # print_hex(body)
        return body

    @staticmethod
    def build_emc_control_body(start):
        cmd = {
            "Setting":
                {"MOD_EMC":
                    start
                }
        }
        jsoninfo = json.dumps(cmd)          # 将python数据结构转换为json格式字符
        # print(type(jsoninfo))
        # print(jsoninfo)
        body = jsoninfo.encode("utf-8")
        # print(type(body))
        # print_hex(body)
        return body

    def build_header(self, msg_id, msg_len, vendor_id=const.GWM_VENDOR_ID, product_id=const.L2_DEVICE_ID, serial_id=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00]):
        """
        构建header的bin数据
        :param msg_id:
        :param msg_len:
        :param vendor_id:
        :param product_id:
        :param serial_id:
        :return:
        """
        header = struct.pack('<HHBBBBBBBBI', msg_id, msg_len, self.vendor_id, self.product_id, self.serial_id[0], self.serial_id[1],
                             self.serial_id[2], self.serial_id[3], self.serial_id[4], self.serial_id[5], self._serial_number)
        # print_bytes(header)

        self._serial_number += 1
        return header

    @staticmethod
    def build_crc(data):
        """
        计算crc的值
        :param data: 需要计算crc的bytearray
        :return: byte类型的crc输出
        """
        # print_bytes(data)
        check = crc16(data)
        crc = struct.pack('<H', check)
        # print_bytes(crc)
        return crc

    def build_inquiry_bin(self):
        """
        构建查询命令的bin格式
        :return:
        """
        body = self.build_inquiry_body()
        header = self.build_header(0x8100, len(body), serial_id=self.serial_id)
        inquiry_bin = self.build_bin(header + body)
        return inquiry_bin

    def build_rtc_sync(self):
        """
        构建时钟同步消息的bin格式
        :return:
        """
        # print("build_rtc_sync++++++++")
        body = self.build_rtc_sync_body()
        # print("body = ", body)
        # header = self.build_header(0x8104, len(body), serial_id=self.serial_id)
        header = self.build_header(const.RTC_SYNC, len(body), serial_id=self.serial_id)
        # print("header = ", header)
        rtc_sync_bin = self.build_bin(header, body)
        # print("rtc_sync_bin = ", rtc_sync_bin)
        # print("build_rtc_sync----------")
        return rtc_sync_bin

    def build_emc_control(self, cmd):
        """
        构建emc启动停止命令的bin格式
        :param cmd: 'start' or 'stop'
        :return:
        """
        body = self.build_emc_control_body(cmd)
        # print("body = ", body)
        # header = self.build_header(0x8104, len(body), serial_id=self.serial_id)
        header = self.build_header(const.SETTING_DOWNLOAD, len(body), serial_id=self.serial_id)
        # print("header = ", header)
        emc_control_bin = self.build_bin(header, body)
        # print("emc_control_bin = ", emc_control_bin)
        return emc_control_bin

    def build_bin(self, header, body):
        # print("build_bin++++++++++")

        crc = self.build_crc(header + body)
        data = header + body + crc
        data = self.escape(data)
        magic_number = const.MAGIC_NUMBER.to_bytes(length=1, byteorder='big', signed=False)
        data = magic_number + data + magic_number
        # print("data = ", data)

        # print_bytes(header)
        # print_bytes(body)
        # print_bytes(crc)
        # print_bytes(data)

        # print("build_bin----------")
        return data

    @staticmethod
    def parse_header(header):
        """
        解析头数据
        :param header:
        :return:
        """
        tmp = header[:2]
        msg_id = int.from_bytes(tmp, byteorder='little', signed=False)

        tmp = header[2:4]
        msg_len = int.from_bytes(tmp, byteorder='little', signed=False)

        vendor_id = header[4]
        product_id = header[5]
        serial_id = header[6:12]

        tmp = header[13:]
        serial_number = int.from_bytes(tmp, byteorder='little', signed=False)

        return msg_id, msg_len, vendor_id, product_id, serial_id, serial_number

    @staticmethod
    def parse_body(body):
        # print(body)
        pass

    def parse_uuid(self):
        """
        返回当前设备的uuid
        :return:
        """
        return self.__uuid

    def parse_body_heart_beat(self):
        # print("parse_body_heart_beat::++++++++++++++++++++")

        devices_info = DevicesInfo()
        if self.__uuid is "":
            self.__uuid = '%02X' % self.vendor_id
            self.__uuid += '%02X' % self.product_id
            self.__uuid += bytesToHexString(self.serial_id)
            # print("uuid = ", self.__uuid)

            devices_info.set_uuid(self.__ip, self.__uuid)
            # print(devices_info.devices_ready())

            if self.__device_logger is None:
                log_dir = "log/" + self.__uuid
                # print("log dir = ", log_dir)
                self.__device_logger = db_file(log_dir)

            if devices_info.devices_ready():
                # print(" send msg device_node_ready!!!")
                wx.CallAfter(pub.sendMessage, self.__pub_device_ready_msg_name)

        wx.CallAfter(pub.sendMessage, 'heart_beat_event', mode=True)
        # print("parse_body_heart_beat::--------------------")

    def parse_body_event(self, body):
        """

        :param body:
        :return:
        """
        # print("parse_body_event::++++++++++++++++++++")
        # print(body)
        # print_bytes(body)

        # body_json = json.dumps(body.decode("utf-8"))
        # print(type(body_json))
        # print(body_json)
        # body_dic = json.loads(body_json)
        body_dic = json.loads(body.decode("utf-8"))

        # print(type(body_dic))
        # print(body_dic["event"])
        if isinstance(body_dic["event"], dict):
            # self.__logger.info("get a module event")
            if self.__device_logger is not None:
                # print(body_dic["event"])
                self.__device_logger.save(body_dic["event"])

            for k, v in body_dic["event"].items():
                # print(k)
                # print(v)
                if k == "mod":
                    name = v
                if k in ["warning", "error", "info"]:
                    status = k
                    log = v
                if k == "date":
                    timestamp = v

            # print("name = ", name)
            # print("log = ", log)
            # print("status = ", status)
            # print("timestamp = ", timestamp)

            self.__logger.debug("name = %s" % name)
            self.__logger.debug("log = %s" % log)
            self.__logger.debug("status = %s" % status)
            self.__logger.debug("timestamp = %s" % timestamp)

            wx.CallAfter(pub.sendMessage, self.__pub_module_info_msg_name, uuid=self.__uuid, name=name, log=log, status=status, time=timestamp)

        elif isinstance(body_dic["event"], list):
            # self.__logger.info("get a module event list")
            names = []
            states = []
            logs = []
            for event in body_dic["event"]:
                # print(body_dic["event"])
                # print("event = ", event)
                if self.__device_logger is not None:
                    self.__device_logger.save(event)

                # print(event["mod"])
                for k, v in event.items():
                    # print("k =", k)
                    # print("v =", v)
                    if k == "mod":
                        names.append(v)
                    if k in ["warning", "error", "info"]:
                        states.append(k)
                        logs.append(v)
                    if k == "date":
                        timestamp = v

            # print("names = ", names)
            # print("logs = ", logs)
            # print("states = ", states)

            for i in range(len(names)):
                name = names[i]
                log = logs[i]
                state = states[i]

                # print("type name =", type(name))
                # print("name = ", name)
                # print("log = ", log)
                # print("state = ", state)

                # self.__logger.info("name = {}".format(name))
                # self.__logger.info("log = {}".format(log))
                # self.__logger.info("state = {}".format(state))

                wx.CallAfter(pub.sendMessage, self.__pub_module_info_msg_name, uuid=self.__uuid, name=name, log=log, status=state, time=timestamp)
        else:
            print("error event!!!")

        # print("parse_body_event::--------------------")

    def parse_body_system_info(self, body):
        body_dic = json.loads(body.decode("utf-8"))
        system_info = body_dic['system']
        system_info['uuid'] = ""
        for char in bytesTobcd(self.vendor_id.to_bytes(1, byteorder='little', signed=False) + self.product_id.to_bytes(1, byteorder='little', signed=False) + self.serial_id):
            system_info['uuid'] += char
        system_info['ip'] = self.__ip

        self.__system_info.update(system_info)
        # print("system info = ", self.__system_info)

        wx.CallAfter(pub.sendMessage, self.__pub_system_info_msg_name, info=self.__system_info)

        devices_info = DevicesInfo()
        if devices_info.get_uuid_from_ip(self.__ip) is None:
            devices_info.set_uuid(self.__ip, system_info['uuid'])

    def parse_body_rtc_sync(self, body):
        print("body = ", body)

    @staticmethod
    def parse_crc(crc_bin):
        """
        将两字节的byte类型数据转化为int类型的crc
        :param crc_bin: byte类型的crc
        :return: int类型的crc
        """
        crc = int.from_bytes(crc_bin, byteorder='little', signed=False)
        return crc

    def parse_uuid(self, data):
        """
        根据消息，解析出uuid
        :param data:
        :return:
        """
        data = self.unescape(data[1:-1])
        header_bin = data[:16]
        msg_id, msg_len, vendor_id, product_id, serial_id, serial_number = self.parse_header(header_bin)
        uuid = '%02X' % vendor_id
        uuid += '%02X' % product_id
        uuid += bytesToHexString(serial_id)
        return uuid

    def parse_data(self, data):
        """
        解析一帧完整bin数据
        :param data:
        :return:
        """
        # self.__logger.info("parse_data++++++++++")
        # print(data)
        # print_hex(data)
        data = self.unescape(data[1:-1])
        # print(data)
        # print_hex(data)

        header_bin = data[:16]
        # print_hex(header_bin)
        msg_id, msg_len, vendor_id, product_id, serial_id, serial_number = self.parse_header(header_bin)
        # print("msg_id = ", msg_id)
        # print("msg_len = ", msg_len)
        # print("vendor_id = ", hex(vendor_id))
        # print("product_id = ", hex(product_id))
        self.serial_id = serial_id

        if msg_len:
            body_bin = data[16:(16 + msg_len)]
            self.parse_body(body_bin)

        begin = 16 + msg_len
        # print("begin = ", begin)
        # print_hex(data)
        # print(len(data))
        crc_bin = data[begin:]
        # print_hex(crc_bin)
        crc = self.parse_crc(crc_bin)

        #
        # print_hex(data[:-2])
        check = crc16(data[:-2])

        if check != crc:
            # print("body = ", body_bin)
            # print_hex(data)
            # print_hex(crc_bin)
            # print("check = 0x%x" % check)
            # print("crc = 0x%x" % crc)
            # print("crc error")
            return None
        else:           # crc 校验正常
            # print("crc ok")

            #    uuid = bytesToHexString(self.serial_id)
            #    log_dir = 'log/' + uuid
            #    print("log dir = ", log_dir)
            #    # self.__device_logger = db_file(log_dir)

            #    device_config.new_device(uuid=uuid, ip=self.ip)

            if msg_id == const.HEART_BEAT_UPLOAD:
                # self.__logger.info("this is a head beat package")
                self.parse_body_heart_beat()
                return const.HEART_BEAT_UPLOAD
            elif msg_id == const.MODULE_EVENT_UPLOAD:
                # self.__logger.info("this is a module event package")
                self.parse_body_event(data[16:-2])
                return const.MODULE_EVENT_UPLOAD
            elif msg_id == const.SYSTEM_INFO_UPLOAD:
                # self.__logger.info("this is a system info package")
                self.parse_body_system_info(data[16:-2])
                return const.SYSTEM_INFO_UPLOAD
            elif msg_id == const.RTC_SYNC:
                self.parse_body_rtc_sync(data[16:-2])
                return const.RTC_SYNC
            else:
                self.__logger.error("invalid package")
                self.__logger.error("msg_id = {}".format(msg_id))
                return None

            """
            if self.__device_logger is None:
                log_dir = bytesToHexString(self.serial_id)
                log_dir = 'log/' + log_dir
                print("log dir = ", log_dir)
                self.__device_logger = LogFile(log_dir)
            """

            """
            random_module = ['EMC_MODULE_ADC0', 'EMC_MODULE_ADC1', 'EMC_MODULE_ADC2',
                             'EMC_MODULE_ADC3', 'EMC_MODULE_ADC4', 'EMC_MODULE_ADC5',
                             'EMC_MODULE_ADC6', 'EMC_MODULE_ADC7']
            random_state = ['info', 'warning', 'error']
            name = choice(random_module)
            log = str(random())
            state = choice(random_state)
            wx.CallAfter(pub.sendMessage, 'recv_module_event', name=name, log=log, status=state)
            """

        # self.__logger.info("parse_data----------")
        pass


if __name__ == '__main__':
    """
    heart_beat = "7e 01 00 00 00 20 01 00 00 00 00 00 00 00 00 00 00 c7 74 7e"
    heart_beat_bin = hexStringTobytes(heart_beat)
    print(heart_beat_bin)
    print_hex(heart_beat_bin)
    protocol = MechProtocol()
    protocol.parse_data(heart_beat_bin)
    """

    event = "7e 02 00 45 00 20 01 00 00 00 00 00 00 02 00 00 00 7b 22 65 76 65 6e 74" \
            "22 3a 7b 22 64 61 74 65 22 3a 22 32 30 31 39 30 32 31 36 30 39 32 38 31" \
            "35 22 2c 22 6d 6f 64 22 3a 22 43 43 43 22 2c 22 77 61 72 6e 69 6e 67 22 " \
            "3a 22 49 4d 55 5f 45 52 52 4f 52 22 7d 01 7d 01 34 24 7e "
    event_bin = hexStringTobytes(event)
    print(event_bin)
    print_bytes(event_bin)
    protocol = ModuleProtocol("127.0.0.1")

    protocol.parse_data(event_bin)

    """
    cmd = {"system": ["version", "temperature", "cpu", "memory"]}
    print(type(cmd))
    print(cmd)
    jsoninfo = json.dumps(cmd)
    print(type(jsoninfo))
    print(jsoninfo)
    print(jsoninfo.encode("utf-8"))
    """
    """
    print("==============================")
    protocol = MechProtocol()
    bin = protocol.build_inquiry_bin()
    print(bin)
    print_hex(bin)
    bbb = protocol.escape(bin)
    print(bbb)
    print_hex(bbb)
    aaa = protocol.unescape(bbb)
    print(aaa)
    print_hex(aaa)
    pass
    """


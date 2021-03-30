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
import wx
import time
import usb
import logging
import threading
# from utils.logger import Logger
from ctypes import CDLL, sizeof
from utils.logger import SingleLogger
from hw.ZLG_Struct import *
from copy import deepcopy
from pyudev.wx import MonitorObserver, EVT_DEVICE_EVENT
from pyudev import Context, Monitor


class CanAnalyze:
    """
    CAN分析仪基类
    """
    def __init__(self, vendor_id, product_id):
        # 初始化日志类
        self.__logger = SingleLogger()

        # CAN分析仪参数
        self.__vendor_id = vendor_id
        self.__product_id = product_id
        self._canfd_devices = []                    # CAN 分析仪列表
        self._device_number = self.scan_devices(vendor_id, product_id)      # CAN分析仪的个数
        pass

    def scan_devices(self, vendor_id, product_id):
        """
        扫描并获取所有指定USB id的CAN分析仪设备
        :param vendor_id:
        :param product_id:
        :return: 设备类的列表
        """
        devices = usb.core.find(find_all=True)
        if devices is None:
            raise ValueError('CAN Device not found')

        for device in devices:
            if (device.idVendor == vendor_id) & (device.idProduct == product_id):
                self._canfd_devices.append(device)

        return len(self._canfd_devices)

    def get_device_number(self):
        return self._device_number


class CanAnalyze_ZLG(CanAnalyze):
    """
    周立功CAN分析仪类
    """
    def __init__(self, vendor_id, product_id):
        # 初始化日志类
        self.__logger = SingleLogger()

        super().__init__(vendor_id, product_id)

        self._canfd_so = "hw/libusbcanfd.so"        # CANFD动态库名称
        self._canfd = CDLL(self._canfd_so)          # 获取CANFD的句柄
        self._device_type = 33                      # 设备类型 （USBCANFD-200U）
        self._can_err_msg = ZCAN_ERR_MSG()          #
        self._can_stat = ZCAN_STAT()

        # CAN分析仪的初始化参数配置
        can_clk = 60000000
        can_mod = 0

        aset = ASET(
            tseg1=6,
            tseg2=1,
            sjw=1,
            smp=0,
            brp=5
        )
        dset = DSET(
            tseg1=6,
            tseg2=1,
            sjw=1,
            smp=0,
            brp=2,
        )

        self._init_info = ZCAN_INIT(
            clk=can_clk,
            mode=can_mod,
            aset=aset,
            dset=dset
        )

        #
        # self.device_number = self.scan_devices(vendor_id, product_id)
        # print("device number2 = ", len(self._canfd_devices))

        # 获取CAN分析仪的设备信息,保存到私有变量self._canfd_devices_info中
        # self._canfd_devices_info = dict()
        self._canfd_devices_info = self.GetDevicesInfo()
        # print("canfd devices info = {}".format(self._canfd_devices_info))
        # self._logger.info("canfd devices info = {}".format(self._canfd_devices_info))
        # self.Close(0)

        #for sn, can_info in self._canfd_devices_info.items():
        #    print("%s : %d " % (sn, can_info['index']))

    def GetDevicesInfo(self):
        """
        获取CAN分析仪的设备信息
        :return:
        """
        canfd_devices_info = dict()

        for num in range(0, self.get_device_number()):
            try:
                # print("num = ", num)
                self._OpenDevice(num)

                info = self._ReadDeviceInfo(num)

                #self._CloseDevice(num)
                #self._OpenDevice(num)


                """
                print(type(info))
                print("board_info = ", info)
                print("hardware version = 0x%x " % info.hmv)
                print("firmware version = 0x%x" % info.fwv)
                print("driver version = 0x%x" % info.drv)
                print("api version = 0x%x" % info.api)
                print("irq = ", info.irq)
                print("channels = ", info.chn)
                print(type(info.sn))
                print("sn = ", info.sn)
                print(type(info.id))
                print("id = ", info.id)
                print(info.sn[0])
                """

                """
                sn = str()
                for ch in info.sn:
                    sn += chr(ch)
                """
                sn = "".join(list(map(str, info.sn)))       # 将字节型的SN转化为字符串
                # print("sn = ", sn)
                # self._logger.info("sn = {}".format(sn))

                canfd_devices_info[sn] = {
                    "index": num,
                    "hmv": hex(info.hmv),   # 转化为16进制字符串 --> 0x100 --> v1.00 --> hardware version
                    "fwv": hex(info.fwv),   # 转化为16进制字符串 --> 0x107 --> v1.07 --> firmware version
                    "drv": hex(info.drv),   # 转化为16进制字符串 --> 0x100 --> v1.00 --> driver version
                    "api": hex(info.api),   # 转化为16进制字符串 --> 0x100 --> v1.00 --> API version
                    "irq": hex(info.irq),
                    "chn": hex(info.chn),   # 转化为16进制字符串 --> 0x2 --> 2 channels
                    "channel": {}
                }

                # for inc in range(int(canfd_devices_info[sn]["chn"], 16)):
                #    canfd_devices_info[sn]["channel"][inc] = dict(init=False, receive=False)
            except Exception as e:
                print(e)
            #self._CloseDevice(0)

        # print(canfd_devices_info)
        # print(type(canfd_devices_info[sn]['hmv']))
        # print(canfd_devices_info[sn]['hmv'])

        return canfd_devices_info


    def ResetCAN(self):
        """
        复位当前所有CAN分析仪的所有通道
        :return:
        """
        for sn, device in self._canfd_devices_info.items():
            for chn in device["channel"]:
                self._ResetCAN(device["device_index"], chn)

    def GetSN(self):
        """
        获取当前驱动监控到的所有设备SN号
        :return:
        """
        return list(self._canfd_devices_info.keys())

    def GetDevInfoFromSN(self, sn):
        """
        根据设备SN号，得到设备索引号
        :param sn:
        :return:
        """
        if sn in self._canfd_devices_info.keys():
            return self._canfd_devices_info[sn]
        else:
            raise ValueError("No device has SN: {}".format(sn))

    def GetDevIDFromSN(self, sn):
        dev_info = self.GetDevInfoFromSN(sn)

        return dev_info["index"]

    def GetChannelFromSN(self, sn):
        dev_info = self.GetDevInfoFromSN(sn)
        # print(dev_info['channel'])
        return [0, 1]

    def GetInitInfo(self):
        """
        返回初始化配置参数
        :return:
        """
        return self._init_info

    def StartAll(self):
        """
        启动所有的CAN分析仪设备的所有通道
        :return:
        """
        for sn, dev_info in self._canfd_devices_info.items():
            index = dev_info["index"]
            for channel in dev_info['channel'].items():
                self.Start(index, channel[0])

    def Start(self, index, chn):
        # print("Start...")
        # print("index = ", index)
        # print("chn = ", chn)
        init_info = self.GetInitInfo()

        self._InitCAN(index, chn, init_info)
        self._SetReference(index, chn, 0x18, c_int(1))      # 设置CANFD的波特率为
        self._StartCAN(index, chn)
        self._ClearBuffer(index, chn)
        # print("Start.....")
        # self._ClearBuffer(card_index, chn)
        # self._canfd_devices_info[sn]["channel"][chn]['init'] = True

    def Close(self, index):
        #self._ResetCAN(index, 0)
        #self._ResetCAN(index, 1)
        self._CloseDevice(index)

    def Send(self, index, channel, can_id, mode, data):
        """
        发送某个CAN分析仪某个通道的数据
        :param index:   设备索引号
        :param channel: 通道索引号
        :param can_id:
        :param mode:    CANFD or CAN2.0 模式
        :param date:    二进制数据 （bytearray）
        :return:
        """

        msg_inf = ZCAN_MSG_INF(
            fmt=1,
            brs=1,
            txm=0,
            sdf=0,
            sef=0
        )

        # print("index = ", index)
        # print("channel = ", channel)
        # print("can_id = ", hex(can_id))
        # print("mode = ", mode)
        # print("data = ", data)

        if mode == "CANFD":
            msg_hdr = ZCAN_MSG_HDR(inf=msg_inf, len=64, chn=channel, id=can_id)

            msg = CANFDMSG(
                hdr=msg_hdr,
                dat=(U8 * 64)()
            )

            # print(type(data))

            num = 0
            for item in data:               # item 为int类型
                msg.dat[num] = item
                # print(type(msg.dat[num]))
                # print(type(item))
                # print("item = ",  item)
                num += 1

        else:
            msg_hdr = ZCAN_MSG_HDR(inf=msg_inf, len=8, chn=channel, id=can_id)

            msg = CAN20MSG(
                hdr=msg_hdr,
                dat=(U8 * 8)(0x40, 0x3F, 0x3E, 0x3D, 0x3C, 0x3B, 0x3A, 0x39)
            )

        count = 1
        frame_number = self._canfd.VCI_TransmitFD(self._device_type, index, channel, byref(msg), count)
        # print("frame_number = ", frame_number)
        return frame_number
        # self._TransmitFD(self, index, channel, msg)

    def Receive(self, index, channel, mode, timeout=2000):
        """
        接收某个CAN分析仪某个通道的数据
        :param index:
        :param channel:
        :param mode:
        :param timeout:
        :return: 二进制数据 （bytearray）
        """
        if mode == "CANFD":
            received_msg = (CANFDMSG * 1)()
        else:
            received_msg = (CAN20MSG * 1)()

        num = self._canfd.VCI_ReceiveFD(self._device_type, index, channel, received_msg, 1, timeout)
        # print("frame_number = ", num)
        # self.__logger.info("frame_number = {}".format(num))
        if num == 0:
            return 0, b''

        for msg in received_msg:
            data = b''
            inc = 0
            # print("msg data = ", msg.dat)
            # print("msg len = ", len(msg.dat))
            for ch in msg.dat:
                # print(type(ch))
                # print("ch = ", ch)
                data += ch.to_bytes(length=1, byteorder='big', signed=False)    # 将int转化为bytes
                if inc >= msg.hdr.len:
                    break
                else:
                    inc += 1
            """
            print("localts: {} [.{}] id: {} ts: {} len: {} data: {}".format(
                str(time.time()),
                channel,
                hex(msg.hdr.id),
                str(msg.hdr.ts),
                str(msg.hdr.len),
                data))
            """
        #num = self._ReceiveFD(self, index, channel, received_msg)
        #if num > 0:
        #    for msg in received_msg:
        #        print(msg)
        #        date.append(msg.dat)
        # print(type(msg.hdr.id))
        # print("id = ", hex(int(msg.hdr.id)))
        # print("len = ", msg.hdr.len)
        # print(type(data))
        # print(data)
        id = int(msg.hdr.id)
        # print("id = ", hex(id))
        # print(msg.hdr.len)
        # print(data)
        # print_hex(data)

        #self.__logger.info("id = {}".format(id))
        #self.__logger.info("len =  {}".format(msg.hdr.len))
        #self.__logger.info("data =  {}".format(data))

        # res = crc8(data)
        # print("res = ", res)
        return msg.hdr.id, data

    def _OpenDevice(self, card_index):
        """
        打开CAN分析仪
        :param card_index:
        :return:
        """
        ret = self._canfd.VCI_OpenDevice(self._device_type, card_index, 0)
        # print("ret = ", ret)
        if ret != 1:
            raise Exception("Open device id {} failed!".format(str(card_index)))

    def _CloseDevice(self, card_index):
        """
        关闭CAN分析仪
        :param card_index:  设备索引号
        :return:
        """
        if self._canfd.VCI_CloseDevice(self._device_type, card_index) != 1:
            raise Exception("Cloase device id {} failed!".format(str(card_index)))

    def _InitCAN(self, card_index, channel, init_info):
        """
        初始化CAN分析仪的某一路
        :param card_index: 设备索引号
        :param channel: 设备通道号
        :param init_info: 初始化配置参数
        :return:
        """
        if self._canfd.VCI_InitCAN(self._device_type, card_index, channel, byref(init_info)) != 1:
            raise Exception("Init device id {} channel {} failed!".format(str(card_index),
                                                                          str(channel)))

    def _ReadDeviceInfo(self, card_index):
        """
        获取CAN分析仪的设备信息
        :param card_index: 设备索引号
        :return:
        """
        device_info = ZCAN_DEV_INF()
        if self._canfd.VCI_ReadBoardInfo(self._device_type, card_index, byref(device_info)) != 1:
            raise Exception("Can't get device info from {}".format(str(card_index)))

        return device_info

    def _ReadDeviceErrInfo(self, card_index, channel):
        """
        获取CAN分析仪某一路的最近一次错误信息
        :param card_index: 设备索引号
        :param channel: 设备通道号
        :return:
        """
        error_info = ZCAN_ERR_MSG()

        if self._canfd.VCI_ReadErrInfo(self._device_type, card_index, channel, byref(error_info)) != 1:
            raise Exception("Can't get channel error info from device id {} channel {}".format(str(card_index),
                                                                                               str(channel)))
        else:
            return error_info

    def _ReadCANStatus(self, card_index, channel):
        """
        获取CAN分析仪某一路的状态
        :param card_index: 设备索引号
        :param channel: 设备通道号
        :return:
        """
        can_status = ZCAN_STAT()
        if self._canfd.VCI_ReadCANStatus(self._device_type, card_index, channel, byref(can_status)) != 1:
            raise Exception("Cant't get CAN status from  device id {} channel {} ".format(str(card_index),
                                                                                          str(channel)))
        else:
            return can_status

    def _SetReference(self, card_index, channel, ref, data):
        """
        设置设备的相应参数
        :param card_index: 设备索引号
        :param channel: 设备通道号
        :param ref: 参数类型, =18, 设置波特率
        :param data:
        :return:
        """
        if self._canfd.VCI_SetReference(self._device_type, card_index, channel, ref, byref(data)) != 1:
            raise Exception("Can't Set Reference {} to device id {} channel {}!".format(str(ref),
                                                                                        str(card_index),
                                                                                        str(channel)))

    def _StartCAN(self, card_index, channel):
        """
        启动CAN分析仪的某一路通道
        :param card_index: 设备索引号
        :param channel: 设备通道号
        :return:
        """
        if self._canfd.VCI_StartCAN(self._device_type, card_index, channel) != 1:
            raise Exception("Start CAN device id {} channel {} failed!".format(str(card_index),
                                                                               str(channel)))

    def _ResetCAN(self, card_index, channel):
        """
        复位CAN分析仪的某一路通道
        :param card_index: 设备索引号
        :param channel: 设备通道号
        :return:
        """
        if self._canfd.VCI_ResetCAN(self._device_type, card_index, channel) != 1:
            raise Exception("Reset CAN device id {} channel {} failed!".format(str(card_index),
                                                                               str(channel)))

    def _GetReceiveNum(self, card_index, channel):
        """
        CAN分析仪某一通道数据缓冲区中接收到但尚未被读取的帧数量
        :param card_index:
        :param channel:
        :return: 帧数量
        """
        return self._canfd.VCI_GetReceiveNum(self._device_type, card_index, channel)

    def _ClearBuffer(self, card_index, channel):
        """
        清空指定CAN分析仪某一通道的缓冲区
        :param card_index:
        :param channel:
        :return:
        """
        if self._canfd.VCI_ClearBuffer(self._device_type, card_index, channel) != 1:
            raise Exception("Cant' clear buffer for device id {} channel {}!".format(str(card_index),
                                                                                     str(channel)))

    def _TransmitFD(self, card_index, channel, msg, count=1):
        """
        发送函数CAN-FD数据
        :param card_index:
        :param channel:
        :param msg:
        :param count: 要发送的帧数
        :return: 实际发送成功的帧数
        """
        frame_number = self._canfd.VCI_TransmitFD(self._device_type, card_index, channel, byref(msg), count)
        return frame_number

    def _Receive(self, card_index, channel, msg, timeout=2):
        """
        从指定的设备CAN分析仪某个通道的接收缓冲区中读取数据
        :param card_index:
        :param channel:
        :param msg:
        :param timeout:
        :return: 实际读取到的帧数
        """
        frame_number = self._canfd.VCI_Receive(self._device_type, card_index, channel, msg, 100, timeout)
        return frame_number

    def _ReceiveFD(self, card_index, channel, msg, timeout=1000):
        """
        从指定的设备CAN分析仪某个通道的接收缓冲区中读取CAN-FD数据
        :param card_index:
        :param channel:
        :param msg:
        :param timeout:
        :return:
        """
        frame_number = self._canfd.VCI_ReceiveFD(self._device_type, card_index, channel, msg, 1000, timeout)
        return frame_number


if __name__ == "__main__":
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    fd = CanAnalyze_ZLG(0x04cc, 0x1240)
    #fd = CanAnalyze_ZLG(0x3068, 0x0009)

    fd.Start(index=0, chn=0)
    #fd.Start(index=0, chn=1)
    # fd.Close(0)
    # fd.Close(1)

    #print("Start-ii")
    #fd = CanAnalyze_ZLG(0x04cc, 0x1240)

    #fd.Start(index=0, chn=0)
    #fd.Start(index=0, chn=1)
    #print("Start-iii")

    # heart_beat = "7e 01 00 00 00 20 01 00 00 00 00 00 00 00 00 00 00 c7 74 7e"
    # heart_beat_bin = hexStringTobytes(heart_beat)
    # print(heart_beat_bin)
    # print_hex(heart_beat_bin)

    # fd.Send(index=0, channel=0, can_id=0x160, mode='CANFD', data=heart_beat_bin)
    # id, respond_bin = fd.Receive(index=0, channel=0, mode='CANFD')
    # print("id = ", hex(id))
    # print(respond_bin)
    # print_hex(respond_bin)

    #fd.Send(index=0, channel=1, can_id=0x202, mode='CANFD')
    #fd.Receive(index=0, channel=1)
    #fd.Send(index=0, channel=1, can_id=0x203, mode='CANFD')
    #fd.Send(index=0, channel=1, can_id=0x204, mode='CANFD')
    #fd.Send(index=0, channel=1, can_id=0x205, mode='CANFD')
    #fd.Send(index=0, channel=1, can_id=0x206, mode='CANFD')
    #fd.Send(index=0, channel=0, can_id=0x207, mode='CANFD')
    #fd = CanFD()

    """
    sleep_cmd = "01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10" \
                "11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F 20" \
                "21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F 30" \
                "31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F 40"

    sleep_cmd_bin = hexStringTobytes(sleep_cmd)
    print(sleep_cmd_bin)
    print_hex(sleep_cmd_bin)

    fd.Send(index=0, channel=0, can_id=0x160, mode='CANFD', data=sleep_cmd_bin)
    """

    """
    {'C8AA17E19B58011900F5': {'device_index': 0, 'hmv': '0x100', 'fwv': '0x107', 'drv': '0x100', 'api': '0x100', 'irq': '0x0', 'chn': '0x2', 'channel': {0: {'init': False, 'receive': False}, 1: {'init': False, 'receive': False}}}}
    """
    pass
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

from wx.lib import newevent

ModuleEvent, EVT_MODULE = newevent.NewEvent()
ChartEvent, EVT_CHART = newevent.NewEvent()
NodeEvent, EVT_NODE = newevent.NewEvent()
NodeTabEvent, EVT_TAB_NODE = newevent.NewEvent()
DeviceEvent, EVT_DEVICE = newevent.NewEvent()
CpuInfoEvent, EVT_CPU_INFO = newevent.NewEvent()
MemoryInfoEvent, EVT_MEMORY_INFO = newevent.NewEvent()
NetworkInfoEvent, EVT_NETWORK_INFO = newevent.NewEvent()
NodeInfoEvent, EVT_NODE_INFO = newevent.NewEvent()
PerformanceInfoEvent, EVT_PERFORMANCE_INFO = newevent.NewEvent()


if __name__ == '__main__':
    pass

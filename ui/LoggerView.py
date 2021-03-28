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
import os
import json


class LoggerFrame(wx.Frame):
    """
    显示日志信息的窗体
    """
    def __init__(self, module, path, mode='all', *args, **kw):
        super(LoggerFrame, self).__init__(*args, **kw)

        # self._makeMenuBar()
        # self.CreateStatusBar()
        # self.SetStatusText("This is an example program...")

        self._module_name = module
        self._log_file = path + os.sep + module + '.log'
        print("log file = ", self._log_file)

        # mode = 'error'
        content = ''
        try:
            with open(self._log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if mode == 'all':
                        content += line
                    else:
                        print(type(line))
                        event = json.loads(line.strip())
                        print(type(event))
                        print("event = ", event)
                        for k, v in event.items():
                            print("k = ", k)
                            if k == mode:
                                content += line

                print("content = ", content)

                self.textCtrl = wx.TextCtrl(self, wx.ID_ANY, value=content,
                                            style=wx.TE_MULTILINE | wx.VSCROLL | wx.TE_READONLY)
                # self.textCtrl.Disable()

        except Exception as e:
            print(e)

    def _makeMenuBar(self):
        fileMenu = wx.Menu()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.onExit, exitItem)
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)

    def onExit(self, event):
        self.Close(True)

    def onAbout(self, event):
        about = wx.adv.AboutDialogInfo()
        about.Name = "Change wxTextCtrl colors example"
        about.Version = "0.1"
        about.Copyright = "(C) Emiliano Mesquita Drago"
        about.Description = "An example for changing wxTextCtrl colors"
        about.SetWebSite("https://github.com/mezka/wx-textctrlcolor-example.git")
        wx.adv.AboutBox(about)


if __name__ == '__main__':
    # 改变当前工作目录到上一级目录
    os.chdir("../")

    app = wx.App()
    frm = LoggerFrame(module="EMC_MODULE_ADC0",
                      path="log/2001313233223637",
                      mode='all',
                      parent=None,
                      style=wx.DEFAULT_FRAME_STYLE | wx.MAXIMIZE,
                      title='Change wxTextCtrl colors example')
    frm.Show()
    app.MainLoop()


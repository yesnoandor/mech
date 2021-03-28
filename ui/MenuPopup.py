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


class MenuControlPopup(wx.Menu):
    def __init__(self, parent):
        super(MenuControlPopup, self).__init__()
        self.parent = parent

        # 生成一个菜单项
        self.time_sync = wx.MenuItem(self, wx.ID_ANY, 'Time Sync')
        self.time_sync.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        # 将菜单项加入到当前菜单中
        self.time_sync_item = self.Append(self.time_sync)

        self.params_setting = wx.MenuItem(self, wx.ID_ANY, 'Params Setting')
        self.params_setting.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.params_setting_item = self.Append(self.params_setting)

        self.shut_down = wx.MenuItem(self, wx.ID_ANY, 'Shut Down')
        self.shut_down.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.shut_down_item = self.Append(self.shut_down)

        self.reboot = wx.MenuItem(self, wx.ID_ANY, 'Reboot')
        self.reboot.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.reboot_item = self.Append(self.reboot)

        self.sleep = wx.MenuItem(self, wx.ID_ANY, 'Sleep')
        self.sleep.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.sleep_item = self.Append(self.sleep)

        self.Bind(wx.EVT_MENU, self.OnTimeSync, self.time_sync_item)
        self.Bind(wx.EVT_MENU, self.OnParamsSetting, self.params_setting_item)
        self.Bind(wx.EVT_MENU, self.OnShutDown, self.shut_down_item)
        self.Bind(wx.EVT_MENU, self.OnReboot, self.reboot_item)
        self.Bind(wx.EVT_MENU, self.OnSleep, self.reboot_item)

    def OnTimeSync(self, event):
        print("Time Sync!")

    def OnParamsSetting(self, event):
        print("Params Setting!")

    def OnShutDown(self, event):
        print("Shut Down!")

    def OnReboot(self, event):
        print("Reboot!")

    def OnSleep(self, event):
        print("Sleep!")


class MenuPopup(wx.Menu):
    def __init__(self, parent):
        super(MenuPopup, self).__init__()
        self.parent = parent

        # 生成一个菜单项
        #self.system_control = wx.MenuItem(self, wx.ID_ANY, 'System Control')
        #self.system_control.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.bmp'))
        # 将菜单项加入到当前菜单中
        #self.system_control_item = self.Append(self.system_control)

        '''
        self.action_menu = wx.Menu()
        self.time_sync = wx.MenuItem(self, wx.ID_ANY, 'Time Sync')
        self.time_sync.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.action_menu.Append(self.time_sync)
        # 将菜单项加入到当前菜单中
        self.AppendMenu(self.system_control_item, self.action_menu)
        '''

        # make a submenu
        self.sm = wx.Menu()
        self.time_sync = wx.MenuItem(self, wx.ID_ANY, 'Time Sync')

        self.time_sync_item = self.sm.Append(self.time_sync)
        self.params_setting = wx.MenuItem(self, wx.ID_ANY, 'Params Setting')
        self.params_setting_item = self.sm.Append(self.params_setting)
        self.shut_down = wx.MenuItem(self, wx.ID_ANY, 'Shut Down')
        self.shut_down_item = self.sm.Append(self.shut_down)
        self.reboot = wx.MenuItem(self, wx.ID_ANY, 'Reboot')
        self.reboot_item = self.sm.Append(self.reboot)
        self.sleep = wx.MenuItem(self, wx.ID_ANY, 'Sleep')
        self.sleep_item = self.sm.Append(self.sleep)

        self.Append(wx.ID_ANY, "System Control", self.sm)

        self.data_Statistics = wx.MenuItem(self, wx.ID_ANY, 'Data Statistics')
        self.data_Statistics.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.data_Statistics_item = self.Append(self.data_Statistics)

        self.update = wx.MenuItem(self, wx.ID_ANY, 'Check for Updates')
        self.update.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.update_item = self.Append(self.update)

        self.help = wx.MenuItem(self, wx.ID_ANY, 'Help')
        self.help.SetBitmap(bmp=wx.Bitmap('res//Time-Sync-icon-gray.png'))
        self.help_item = self.Append(self.help)

        self.Bind(wx.EVT_MENU, self.OnTimeSync, self.time_sync_item)
        self.Bind(wx.EVT_MENU, self.OnParamsSetting, self.params_setting_item)
        self.Bind(wx.EVT_MENU, self.OnShutDown, self.shut_down_item)
        self.Bind(wx.EVT_MENU, self.OnReboot, self.reboot_item)
        self.Bind(wx.EVT_MENU, self.OnSleep, self.sleep_item)
        self.Bind(wx.EVT_MENU, self.OnDataStatistics, self.data_Statistics_item)
        self.Bind(wx.EVT_MENU, self.OnUpdate, self.update_item)
        self.Bind(wx.EVT_MENU, self.OnHelp, self.help_item)

        self.time_sync.SetBackgroundColour((0, 0, 200))
        self.help.SetTextColour((0, 0, 200))

    def OnDataStatistics(self, event):
        print("Data Statistics")

    def OnUpdate(self, event):
        print("Update")

    def OnHelp(self, event):
        print("Help")

    def OnTimeSync(self, event):
        print("Time Sync!")

    def OnParamsSetting(self, event):
        print("Params Setting!")

    def OnShutDown(self, event):
        print("Shut Down!")

    def OnReboot(self, event):
        print("Reboot!")

    def OnSleep(self, event):
        print("Sleep!")


if __name__ == '__main__':
    pass

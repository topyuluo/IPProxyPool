#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : YuLuo

import sys
sys.path.append("..")
from WebService.Api import run as WebRun
from Schedule.ProxyRefreshSchedule import run as RefreshRun
from Schedule.ProxyValidate import run as ValidateRun
from multiprocessing import Process

"""
    统一启动方法入口
"""
def run():

        list = []

        webProcess = Process(target= WebRun ,name='webapi')   #web启动入口
        list.append(webProcess)
        refreshProcess = Process(target=RefreshRun , name='proxy') #下载proxy入口
        list.append(refreshProcess)
        validate = Process(target=ValidateRun , name='validateproxy')  #验证proxy入口
        list.append(validate)

        for process in list:
            process.start()

        for process in list:
            process.join()

if __name__ == '__main__':
    run()


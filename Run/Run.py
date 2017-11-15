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
class Run(object):

    def __init__(self):
        pass

    def run(self):

        list = []

        webProcess = Process(target= WebRun )   #web启动入口
        list.append(webProcess)
        refreshProcess = Process(target=RefreshRun) #下载proxy入口
        list.append(refreshProcess)
        validate = Process(target=ValidateRun)  #验证proxy入口
        list.append(validate)

        for process in list:
            process.start()

        for process in list:
            process.join()

if __name__ == '__main__':
    Run().run()


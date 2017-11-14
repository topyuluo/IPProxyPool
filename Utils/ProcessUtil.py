#!/usr/bin/env python
# -*- coding: utf-8 -*-


# @Author  : YuLuo
from Utils.Constants import processNum
from multiprocessing import  Process
from Utils.ReadConfigUtil import ReadConfigUtil
from Utils.Constants import processNum

"""
    进程类封装
"""
class ProcessUtil(object):

    def __init__(self ,num=None):
        if processNum is None:
            self.num = processNum
        else:
            self.num = num
        self.process_list = []


    def putProcessPool(self , target):
        '''
        add task
        :param target:
        :return:
        '''
        for i in range(processNum):
            process = Process(target=target, args=())
            self.process_list.append(process)

    def start(self):
        '''
        start task
        :return:
        '''
        for i in range(processNum):
            self.process_list[i].start()

    def join(self):
        '''
        wait sub process end
        :return:
        '''
        for i in range(processNum):
            self.process_list[i].join()


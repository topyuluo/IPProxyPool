#!/usr/bin/env python
# -*- coding: utf-8 -*-


# @Author  : YuLuo
import  logging
import os
from logging.handlers import TimedRotatingFileHandler
from Utils.Constants import logLevel

class Logger():
    def __init__(self, name ,loglevel=logLevel):
        """
        package logger class
        :param name: log name
        :param fileName: log file name
        :param level:  log level
        """
        level = logging.INFO if loglevel == 1 else logging.DEBUG
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.handler(name ,level)

    def handler(self , name ,level):
        if not self.logger.handlers:
            file_name = '/%s.log' % name
            path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
            realPath = os.path.join(path , 'log')
            if not os.path.exists(realPath):
                os.makedirs(realPath)
            # 创建一个handler，用于写入日志文件
            path_file_name = realPath+file_name
            fh = TimedRotatingFileHandler(filename=path_file_name, when="D", interval=1, backupCount=2)
            # fh = logging.FileHandler(path_file_name)
            fh.setLevel(level)

            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(level)

            # 定义handler的输出格式
            formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler

            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

    def getLog(self):
        return  self.logger
if __name__ == '__main__':
    print (os.path.exists(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0],'log')))
    os.makedirs(os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0],'log'))

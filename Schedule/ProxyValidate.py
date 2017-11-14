#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : YuLuo
from Utils.Util import validUserProxy
from Utils.ProcessUtil import ProcessUtil
import time
from DB.DBClientFactory import DBClientFactory
from Utils.Constants import sleepTime ,dbName ,commonPool ,validatePool
"""
    验证代理类
"""
from Utils.Logger import Logger
logger = Logger('validate').getLog()

class ProxyValidate(object):
    def __init__(self):
        self.__dbClient = DBClientFactory(dbName , commonPool ).createDB()
        pass

    def validate_proxy(self):
        """
        validate proxy
        :return:
        """
        proxy = None
        flag = True
        while flag:
            proxy = self.__dbClient.get()
            if proxy is None:
                logger.warn('当前仓库无ip, 进程休眠 ,休眠时间：%s 秒' % sleepTime)
                time.sleep(sleepTime)
            else:
                flag = False
        while proxy:
            if validUserProxy(proxy):
                logger.info('success : %s' % proxy)
                self.__dbClient.changeTable(validatePool)
                self.__dbClient.put(proxy)
            self.__dbClient.changeTable(commonPool)
            proxy = self.__dbClient.get()

def validate_proxy_pool():
    schedule = ProxyValidate()
    schedule.validate_proxy()

def run():
    logger.info("[ProxyValidate.py] Run Success !")
    process = ProcessUtil()
    process.putProcessPool(validate_proxy_pool)
    process.start()
    process.join()

if __name__ == '__main__':
    run()
# -*- coding: utf-8 -*-
#! /usr/bin/env python

from apscheduler.schedulers.blocking import BlockingScheduler
from Collectproxy.CollectFreeProxy import CollectFreeProxy
from Utils.ReadConfigUtil import ReadConfigUtil
from Utils.Logger import Logger
from DB.DBClientFactory import DBClientFactory
from datetime import  datetime
from Utils.Constants import schedulerMinutes , dbName , commonPool ,freeProxy as proxySections

import logging
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


__author__ = 'YuLuo'

"""
    定时刷新代理
"""
logger = Logger("scheduler").getLog()
class ProxyRefreshSchedule(object):

    def __init__(self):
        self.__dbClient = DBClientFactory(dbName, commonPool).createDB()
        self.config = ReadConfigUtil()
        pass

    def init_refresh_proxy(self):
        """
        init and refresh proxy
        :return:
        """
        start_time = datetime.now()
        proxy_set = set()
        for freeProxy in self.config.getSections(proxySections):
            for proxy in getattr(CollectFreeProxy ,freeProxy.strip())():
                proxy_set.add(proxy.strip())
        logger.info('begin insert data !')
        i = 0
        for proxy in proxy_set:
            result = self.saveData(proxy)
            if result is not None:
                i = i + 1
        logger.info('end insert data ! - success ')
        end_time = datetime.now()
        use_time = (end_time -start_time).total_seconds()
        logger.info("完成一次周期刷新，耗时：%s 秒" % use_time)
        logger.info("本次刷新新增ip: %s 个 ，其中有效ip : %s 个" %(len(proxy_set) , i))

    def saveData(self ,proxy):
        return self.__dbClient.put(proxy)

def main():
    proxySchedule = ProxyRefreshSchedule()
    proxySchedule.init_refresh_proxy()

def run():
    logger.info("[ProxyRefreshScheduler.py] Run Success !")
    scheduler = BlockingScheduler()
    scheduler.add_job(main , "interval" ,minutes = schedulerMinutes)
    logger.info("定时任务创建成功，%s 分钟后将运行！" % schedulerMinutes)
    scheduler.start()

if __name__ == '__main__':
    main()








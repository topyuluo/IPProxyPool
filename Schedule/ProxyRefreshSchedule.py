# -*- coding: utf-8 -*-
#! /usr/bin/env python

from apscheduler.schedulers.blocking import BlockingScheduler
from Collectproxy.CollectFreeProxy import CollectFreeProxy
from Utils.ReadConfigUtil import ReadConfigUtil
from Utils.Logger import Logger
from DB.DBClientFactory import DBClientFactory
from datetime import  datetime
import time

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
            try:
                for proxy in getattr(CollectFreeProxy ,freeProxy.strip())():
                    proxy_set.add(proxy.strip())
            except Exception as e :
                logger.error('error')
        logger.info('begin insert data !')
        i = 0
        new_set = list()

        old_proxy_list = self.__dbClient.getAllProxy()

        for proxy in proxy_set:
            if len(proxy) > 6:
                if proxy not in old_proxy_list:
                    downtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    data = {'proxy': proxy, 'downtime': downtime, 'score': 10}
                    i = i + 1
                    new_set.append(data)

                # datetime1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # data = {'proxy': proxy, 'downtime': datetime1, 'score': 10}
                # result = self.saveData(data)
                # if not result:

        self.__dbClient.insert_many(new_set)
        logger.info('end insert data ! - success ')
        end_time = datetime.now()
        use_time = (end_time -start_time).total_seconds()
        logger.info("完成一次周期刷新，耗时：%s 秒" % use_time)
        logger.info("本次刷新共下载代理: %s 个 ，其中有效代理 : %s 个" %(len(proxy_set) , i))

    # def saveData(self ,data):
    #     return self.__dbClient.find(data)

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








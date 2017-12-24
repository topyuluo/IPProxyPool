#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Author  : YuLuo
from Utils.Util import validUserProxy
from Utils.ProcessUtil import ProcessUtil
import time
from DB.DBClientFactory import DBClientFactory
from Utils.Constants import sleepTime ,dbName ,commonPool ,validatePool
import threading
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
        data = None
        flag = True
        while flag:
            data = self.__dbClient.get_one()
            if data is None:
                logger.warn('当前仓库无ip, 进程休眠 ,休眠时间：%s 秒' % sleepTime)
                time.sleep(sleepTime)
            else:
                flag = False
        while data:
            validatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if validUserProxy(data):
                logger.info('success : %s' % data)
                self.__dbClient.remove(data['_id'])
                self.__dbClient.changeTable(validatePool)
                data['validatetime'] = validatetime
                self.__dbClient.put(data)
            else:
                change = {}
                score = data['score'] -2
                if score < 0 :
                    self.__dbClient.remove(data['_id'])
                else:
                    change['score'] = score
                    change['validatetime'] = validatetime
                    self.__dbClient.update({'proxy':data['proxy']} , {'$set':change})
            self.__dbClient.changeTable(commonPool)
            data = self.__dbClient.get_one()

def validate_proxy_pool():
    # if mutex.acquire(1):
    print("12323")
    schedule = ProxyValidate()
    schedule.validate_proxy()
    mutex.release()


num = 0
mutex = threading.Lock()

def run():
    logger.info("[ProxyValidate.py] Run Success !")
    process = ProcessUtil()
    process.putProcessPool(validate_proxy_pool)
    process.start()
    process.join()

    
    # threads = []
    # t= threading.Thread(target=validate_proxy_pool ,args=())
    # t1 = threading.Thread(target=validate_proxy_pool ,args=())
    # t2 = threading.Thread(target=validate_proxy_pool ,args=())
    # t = validate_proxy_pool()
    # t1 = validate_proxy_pool()
    # t2 = validate_proxy_pool()
    #
    # threads.append(t)
    # threads.append(t1)
    # threads.append(t2)
    #
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # for t in threads:
    #     t.join()


if __name__ == '__main__':
    run()
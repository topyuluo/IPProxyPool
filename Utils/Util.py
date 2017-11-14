#-*- coding:utf-8 -*-
"""
工具函数
"""
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import functools
from Utils.Logger import  Logger
from Utils.ReadConfigUtil import ReadConfigUtil

logger = Logger("validate").getLog()
url = ReadConfigUtil().get('WebUrl' ,'verifyUrl')

'''装饰器'''
def time(web):
    def deco(func):
        @functools.wraps(func)
        def __deco(*args , **kw):
            logger.info('当前下载: %s' % web)
            return func(*args , **kw)
        return __deco
    return deco

def validUserProxy(proxy):
    """
    validate available proxy
    :param proxy:
    :return:
    """
    proxy = {
        'http':proxy ,
        'https':proxy}
    try:
        response = requests.get(url ,proxies=proxy , timeout = 10 , verify = False )
        if response.status_code == requests.codes.ok:
            return True
        else:
            return False
    except Exception:
        logger.debug("代理验证异常")


def request():
    import json
    response = requests.get('http://192.168.1.12:5001/get/')
    jsonStr = json.loads(response.text)
    proxy = jsonStr['proxy']
    proxy = {
        'http': proxy,
        'https': proxy}
    return proxy
# print request()






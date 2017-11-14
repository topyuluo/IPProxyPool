# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

import os
try:
    import ConfigParser
except:
    import configparser as ConfigParser
version = False
import sys
if sys.version_info[0] == 3 :
    version = True
'''
    读取配置文件工具类
        - 采用单例模式
        - 线程非安全

            如果想要保证线程安全
                - 可以采用双重检验锁的方式来处理。
'''
class ReadConfigUtil(object):
    __instance = None

    def __init__(self):
        self.path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
        self.realPath = os.path.join(self.path , "conf.ini")
        self.configParse = NewConfigerParser()
        if version:
            self.configParse.read(self.realPath ,encoding='utf-8')
        else:
            self.configParse.read(self.realPath)

    '''
        单例模式
            - 线程非安全
    '''
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(ReadConfigUtil ,cls).__new__(cls , *args , **kwargs)
        return cls.__instance

    def get(self, field , key ):
        try:
            result = self.configParse.get(field , key)
        except:
            result = None
        return result

    def getSections(self , sections):
        return self.configParse.options(sections)

    def getInt(self ,field , key):
        try:
            result = self.configParse.getint(field , key)
        except:
            print ("方法getInt() 抛出异常")
            result = 0
        return result


class NewConfigerParser(ConfigParser.ConfigParser):
    """
    option 大小写不敏感问题
    """
    def optionxform(self ,optionstr):
        return optionstr

if __name__ == '__main__':
    print (ReadConfigUtil().get("freeProxy"))
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())
    # print id(ReadConfigUtil())

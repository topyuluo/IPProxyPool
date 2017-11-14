# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

'''
    数据库工厂类
        -返回具体数据库操作类
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from Utils.ReadConfigUtil import ReadConfigUtil
from Utils.Constants import mongodb ,redisdb ,mysqldb ,db , db_type ,db_host ,db_port
class DBClientFactory(object):

    def __init__(self ,dbName , dbTable):
        self.config = ReadConfigUtil()
        self.dbName = dbName
        self.dbTable = dbTable
        self.host = self.config.get(db , db_host)
        self.port = self.config.get(db ,db_port)

    def createDB(self):
        """
        常见数据库客户端
        :return:
        """
        return self.getClient()

    def getClient(self):
        __Client = None

        if mongodb == self.readConfig():
            __Client = 'MongoDBClient'

        if redisdb == self.readConfig():
            __Client = 'RedisDBClient'

        if mysqldb == self.readConfig():
            __Client = 'MysqlDBClient'

        if __Client is None :
            print("配置文件错误,初始化数据库失败")
            return None
        return self.getInstance(__Client ,__Client ,self.dbName , self.dbTable ,host = self.host ,port = self.port)

    def getInstance(self ,module_name , class_name , *args , **kw):
        """
        动态生成实例
        :param module_name:
        :param class_name:
        :param args:
        :param kw:
        :return:
        """
        module_meta = __import__(module_name ,globals() ,locals() ,[class_name])
        class_meta = getattr(module_meta , class_name)
        obj = class_meta(*args , **kw)
        return obj

    def readConfig(self):
        """
        抽离读取文件的方法
        :return:
        """
        return  self.config.get(db , db_type)


if __name__ == '__main__':
    mong = DBClientFactory('12' ,'1' ,'1' ,12).createDB()
    mong.put('12312123')
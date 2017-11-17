# -*- coding:utf-8 -*-

'''
    常量定义文件
'''

'''配置文件键值对'''
db = 'db'
db_type = 'db_type'
db_host = 'db_host'
db_port = 'db_port'
db_name = 'db_name'
freeProxy = "freeProxy"

'''定义数据库类型'''
mongodb = 'mongodb'
redisdb = 'redis'
mysqldb = 'mysql'

'''定义参数常量'''
type = 'type'
name = 'name'
host = 'host'
port = 'port'
clazz = 'getfreeproxy'
defaultHost = '127.0.0.1'
defaultPort = '27017'

'''配置数据库相关信息'''
mongoClient = 'MongoDBClient'
dbName = "IpProxyPool" #数据库名字
commonPool = 'Common_IP'  #ip池总表
validatePool = 'verify_ip' #验证ip表

'''Http请求配置'''
retryTime = 5
timeout = 30

'''进程配置'''
processNum = 3
sleepTime = 60*31

'''任务下载周期'''
schedulerMinutes = 15 #单位为分钟

'''邮件配置'''
smtp_server = 'smtp.xxx.com'
from_email = 'xxx' #发件人邮件地址
email_password = 'xxx'
to_email = 'xxx' #接收人邮件地址


'''打印日志输出等级配置'''
logLevel = 1  #0代表debug级别(默认) 1 为info 级别





# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

import sys
from pymongo import MongoClient
import random
from DB.DBClient import DBClient
from Utils.Constants import defaultHost , defaultPort
"""
    MongoDB数据库操作类
"""

class MongoDBClient(DBClient):

   def __init__(self , dbName, collectionName, host= defaultHost ,port = defaultPort ):
      self.__client = MongoClient(host, int(port))
      self.__dbName = self.__client[dbName]
      self.name = collectionName

      # self.__collectionName = self.__dbName[collectionName]


   def put(self , value):
      """
      put data in mongodb
      :param value:
      :return:
      """

      if self.__dbName[self.name].find_one({'proxy':value}):
         return None
      else:
         self.__dbName[self.name].insert({'proxy':value})
         return "OK"

   def remove(self , value):
      """
      remove data from mongodb
      :param value:
      :return:
      """
      self.__dbName[self.name].remove({'proxy':value})



   def getAll(self):
      """
      get all data
      :return:
      """
      return [p['proxy'] for p in self.__dbName[self.name].find()]

   def get(self):
      """
      get a random proxy
      :return:
      """
      get_all = self.getAll()
      return random.choice(get_all) if get_all else  None


   def removeAll(self):
      """
      clean proxy table
      :return:
      """
      self.__dbName[self.name].remove()


   def getcount(self):
      """
      get all count in db
      :return:
      """
      return self.__dbName[self.name].count()

   def changeTable(self ,tableName):
      """
      change table
      :return:
      """
      self.name = tableName

if __name__ == '__main__':
   client = MongoDBClient('IpProxyPool', 'verify_ip')
   print (client.getcount())


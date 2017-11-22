# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

import time
from pymongo import MongoClient
import random
from DB.DBClient import DBClient
from Utils.Constants import defaultHost , defaultPort
import pymongo
"""
    MongoDB数据库操作类
"""

class MongoDBClient(DBClient):

   def __init__(self , dbName, collectionName, host= defaultHost ,port = defaultPort ):
      self.__client = MongoClient(host, int(port))
      self.__dbName = self.__client[dbName]
      self.name = collectionName

      # self.__collectionName = self.__dbName[collectionName]


   def put(self , data):
      """
      put data in mongodb
      :param value:
      :return:
      """
      if self.__dbName[self.name].find_one({'proxy':data['proxy']}):
         return None
      else:
         self.__dbName[self.name].insert(data)
         return "OK"

   def remove(self , value):
      """
      remove data from mongodb
      :param value:
      :return:
      """
      self.__dbName[self.name].remove({'_id':value})

   def insert_many(self , list):
      """
      insert data many data
      :param list:
      :return:
      """
      self.__dbName[self.name].insert_many(list)

   def update(self , old , change):
      self.__dbName[self.name].update(old , change)

   def find(self , data):
      data = self.__dbName[self.name].find_one({'proxy':data['proxy']})
      if data:
         return True
      else:
         return None



   def getAll(self):
      """
      get all data
      :return:
      """
      return [p for p in self.__dbName[self.name].find()]


   def getAllProxy(self):

      return [p['proxy'] for p in self.__dbName[self.name].find()]

   def get(self):
      """
      get a random proxy
      :return:
      """
      get_all = self.getAll()
      return random.choice(get_all) if get_all else  None

   def get_one(self):
      data = self.__dbName[self.name].find().sort('score', pymongo.DESCENDING)[0]
      print(data)
      self.remove(data['_id'])
      return data


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
   client = MongoDBClient('IpProxyPool', 'Common_IP')
   print (client.get()['proxy'])


# -*- coding:utf-8 -*-
__author__ = 'Yuluo'

"""
    DB操作类
      - 定义相关方法，方法无实现
      - 方法的实现交给子类
"""

class DBClient(object):


   def put(self , value):
      '''
      insert data
      :param value:
      :return:
      '''
      pass

   def put(self , key , vlaue):

      pass

   def remove(self , value):
      """
      remove data
      :param value:
      :return:
      """
      pass

   def remove(self , key ,value):
      pass

   def getAll(self):
      """
      get all data
      :return:
      """
      pass

   def get(self):
      """
      get a random data
      :return:
      """
      pass

   def get(self , value):
      """
      get a assign data
      :param value:
      :return:
      """
      pass

   def removeAll(self):
      """
      clean database
      :return:
      """
      pass

   def getcount(self):
      """
      get data count
      :return:
      """
      pass

   def changeTable(self ,tableName):
      """
      change table
      :return:
      """
      pass


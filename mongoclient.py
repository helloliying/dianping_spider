#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
import pymongo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MongoClient:

	def __init__(self):
		host = pyspider.config.mongo_config.host
		port = pyspider.config.mongo_config.port
		db = pyspider.config.mongo_config.db
		self.mongoConn = pymongo.MongoClient(host,port)
		self.db = self.mongoConn.huicong

	def collectData(self,data,set_name):
		if data:
			self.db.huicong_html.insert({data})  #悲剧写死了。。。

	def countData(self):
		return self.db.find.count()

	def outputData(self):	
		pass
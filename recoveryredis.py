#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from redisclient import RedisConnect
import re
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

redisConn = RedisConnect()
#while redisConn.scard("failed::store::user::bak")>0:
#	url = redisConn.pop("failed::store::user::bak")
#	print (url)
#	if re.search("pageno=1",url)!= None:
#		link = re.findall("http://www.dianping.com(.*)/review_more",url)[0]
#		print (link)
#		redisConn.sadd("dianping::store",link)
#	else:
#		print ("relive url")
#		print (url)
#		redisConn.sadd("failed::store::user::clean",url)

while redisConn.scard("success::store::user::bak")>0:
	url = redisConn.pop("success::store::user::bak")
	print (url)
	link = re.findall("http://www.dianping.com(.*)/review_more",url)[0]
	print (link)
	redisConn.sadd("success::store",link)

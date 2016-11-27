#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from http import  HttpRequest
from log import Logger
import time
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import requests
import urllib2
import cookielib


HTTP_HEADERS = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Host':'www.dianping.com',
#	'Referer':'http://www.dianping.com/member/32513405',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

class RequestCookie(object):
	
	def __init__(self):
		pass

	def requestCookie(self,url):
		s = requests.Session()
	#	HTTP_HEADERS["Referer"] = url
	#	print (HTTP_HEADERS)
		resp = s.get(url,headers = HTTP_HEADERS)
		cookies = resp.cookies
		cookie = '; '.join(['='.join(item) for item in cookies.items()])
		return (cookie)

x = RequestCookie()
cookie = x.requestCookie("http://www.dianping.com/search/category/2/10/g110")
print (cookie)

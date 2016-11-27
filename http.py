#-*-coding':'utf8-*-
#! /usr/bin/python
#encoding=utf-8
import urllib
import requests
import urllib2
import cookielib
from lxml import etree
#from config import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


HTTP_HEADERS = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
#	'Cookie':'_hc.v=433ac401-2e99-61dc-513e-d94ae4f02385.1479721275; __utma=1.1976915789.1479721275.1479721275.1479721275.1; __utmc=1; __utmz=1.1479721275.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; s_ViewType=10; PHOENIX_ID=0a01070e-1588648a1aa-b93338; JSESSIONID=C600AF39DDA087D454B1C24FE50939B2; aburl=1; cy=2; cye=beijing',
	'Cookie':'_hc.v="\"eea4ca0c-db9a-4f8d-9aee-94789e096462.1479794513\""; PHOENIX_ID=0a01677b-1589003038d-14482ed; s_ViewType=10; JSESSIONID=9F96B4203CF5F5E561A8824AF91D5580; aburl=1; cy=2; cye=beijing',
	'Host':'www.dianping.com',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

class HttpRequest:

	def __init__(self,timeout=None):
		self.encoding = "utf-8"
        #if timeout == None':'
		timeout = 30
		urllib2.socket.setdefaulttimeout(float(timeout))
		cookie = cookielib.CookieJar()
		handler = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)

	def get(self,url,params = None,header = None):
		request_url = url
		data = None
		if params !=None:
			param = urllib.urlencode(params)
			request_url = url + "?" + param 	
		response = requests.get(request_url,headers = HTTP_HEADERS)
		return  (response.text,response.status_code)

	def post(self,url,params = None,header = None):
		if params != None:
			result = requests.post(url,data = params ,headers = HTTP_HEADERS).text
		return result	

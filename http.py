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
	'Cookie':'showNav=#nav-tab|0|1; navCtgScroll=243; _hc.v="\"eea4ca0c-db9a-4f8d-9aee-94789e096462.1479794513\""; dper=56a37ab9b02a650a7c9fef87dee6d27fbf2d9e1ab218272202ea7ac978ca10ee; ua=%E6%9D%8E%E5%A4%9A%E5%A4%9A%E7%9A%84%E5%A4%8F%E5%A4%A9; __utma=205923334.406525566.1480045399.1480045399.1480045399.1; __utmc=205923334; __utmz=205923334.1480045399.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a0102fe-158a8ae8a9a-29df578; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; JSESSIONID=90A3611AF42719064478A354A6DB7FFE; aburl=1; cy=2; cye=beijing',
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

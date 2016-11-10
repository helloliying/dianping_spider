#-*-coding':'utf8-*-
#! /usr/bin/python
#encoding=utf-8
import urllib
import requests
import urllib2
import cookielib
from lxml import etree
from config import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# HTTP_HEADERS = {
#     'Accept'':''application/json, text/javascript',
# 	'Accept-Encoding'':''gzip, deflate',
# 	'Accept-Language'':''zh-CN,zh;q=0.8',
# 	'Content-Length'':''21',
# 	'Content-Type'':''application/x-www-form-urlencoded;charset=UTF-8;',
# 	'Cookie'':''_hc.v=a2191b18-0b92-c093-4de3-e74d5fba8273.1473007045; __utma=205923334.618598470.1477727672.1477727672.1478019961.2; __utmz=205923334.1477727672.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a018333-1582e6765c3-5322b4; s_ViewType=10; JSESSIONID=180BA04564BB5583B9A3C217C19D98FF; aburl=1; cy=2; cye=beijing',
# 	'Host'':''www.dianping.com',
# 	'Origin'':''http':'//www.dianping.com',
# 	'Proxy-Connection'':''keep-alive',
# 	# 'Referer'':''http':'//www.dianping.com/member/97899/checkin',
# 	'User-Agent'':''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
# 	'X-Request'':''JSON',
# 	'X-Requested-With'':''XMLHttpRequest'	
# }

HTTP_HEADERS = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Cookie':'_hc.v=a2191b18-0b92-c093-4de3-e74d5fba8273.1473007045; __utma=205923334.618598470.1477727672.1477727672.1478019961.2; __utmz=205923334.1477727672.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a65026a-1583c6df3e8-bdfe90; s_ViewType=10; JSESSIONID=F770931C9A6A65A91A19BE5F3144942A; aburl=1; cy=2; cye=beijing',
	'Host':'www.dianping.com',
	'Referer':'http://www.dianping.com/member/32513405',
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
		return  (response.text)

	def post(self,url,params = None,header = None):
		if params != None:
			result = requests.post(url,data = params ,headers = HTTP_HEADERS).text
		return result	

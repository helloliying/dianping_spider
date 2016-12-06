#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
import urllib
import requests
import urllib2
import cookielib
from lxml import etree
from cookie import RequestCookie
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


HTTP_HEADERS = {
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
#	'Cookie':'_hc.v="\"eea4ca0c-db9a-4f8d-9aee-94789e096462.1479794513\""; PHOENIX_ID=0a650c81-1588abd4ab7-f89cab; s_ViewType=10; JSESSIONID=DF48757BB424EF1C49BFF24EA668C98C; aburl=1; cy=2; cye=beijing',
	'Cookie':'aburl=1; cy=2; cye=beijing; JSESSIONID=1F7281EE2EDD5B6D033DBEEE0E476B28',
	'Host':'www.dianping.com',
	'Referer':'http://www.dianping.com/member/32513405',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

class HttpRequest:

	def __init__(self,timeout=None):
		self.encoding = "utf-8"
		self.cookie = RequestCookie()
		self.headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
#       'Cookie':'_hc.v="\"eea4ca0c-db9a-4f8d-9aee-94789e096462.1479794513\""; PHOENIX_ID=0a650c81-1588abd4ab7-f89cab; s_ViewType=10; JSESSIONID=DF48757BB424EF1C49BFF24EA668C98C; aburl=1; cy=2; cye=beijing',
        'Cookie':'aburl=1; cy=2; cye=beijing; JSESSIONID=1F7281EE2EDD5B6D033DBEEE0E476B28',
        'Host':'www.dianping.com',
        'Referer':'http://www.dianping.com/member/32513405',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}


        #if timeout == None':'
		timeout = 30
		urllib2.socket.setdefaulttimeout(float(timeout))
		cookie = cookielib.CookieJar()
		handler = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)
	
		
	def get(self,url,params = None,header = None):
		print ("====proxy===")
		request_url = url
		data = None
		proxyHost = "proxy.abuyun.com"
		proxyPort = "9010"
		proxyUser = "H215X75AO3O6S96D"
		proxyPass = "16DF963DB93D1328"
		proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
			"host" : proxyHost,
			"port" : proxyPort,
			"user" : proxyUser,
			"pass" : proxyPass,
   		}
		proxies = {
			"http"  : proxyMeta,
			"https" : proxyMeta,
  		}
		if params !=None:
			param = urllib.urlencode(params)
			request_url = url + "?" + param 	

		resp = requests.get(request_url, proxies=proxies,headers = HTTP_HEADERS)
		if resp.status_code == 404 or resp.status_code == 403:
			cookie = self.cookie.requestCookie(request_url)
			print (cookie)
			HTTP_HEADERS["Cookie"] = cookie
			print (HTTP_HEADERS)
			resp = requests.get(request_url, proxies=proxies,headers = HTTP_HEADERS)
			
		return (resp.text,resp.status_code)

	def post(self,url,params = None,header = None):
		if params != None:
			result = requests.post(url,data = params ,headers = HTTP_HEADERS).text
		return result	

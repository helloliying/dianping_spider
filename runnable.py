#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from http import  HttpRequest
from httpparser import HttpParser
from queue import Queue
from redisclient import RedisConnect
from mysqlclient import MysqlClient
import time
import sys
import re
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json 
import time


class UrlRunnable:
	
	def __init__(self):
		self.httpRequest = HttpRequest()
		self.httpParser = HttpParser()
		self.redisConn = RedisConnect()
		self.start_url = "http://www.dianping.com/shopall/2/0"
		self.mysqlConn = MysqlClient("127.0.0.1","root","homelink",'dianping',3306)


	def saveHtml(self,url,param,html):
		id = re.findall('[0-9]+',url)[0]
		path = '/homelink/dianping/html/'+param+'/'+id[0:3]+'/'+id[3:6]+'/'
		if os.path.exists(path) == False:
			os.makedirs(path)
		html_path = path + id+'_'+param+'.txt'
		f = open(html_path,"a")
		f.write(html)
		f.flush()

	def linksUrl(self):
		try:
			html = self.httpRequest.get(self.start_url)
			sites = self.httpParser.parseNode(html,'//div[@class="main_w"]/div/div[1]/dl')
			print (sites)
			postDic = {}
			dic_list = ["tag_level_1","tag_level_2","tag_link","create_time","update_time"]
			for site in sites:
				tags = site.xpath('dt/a/text()')
				print (tags)
				link_urls = site.xpath('dd/ul/li/a/@href')
				print (link_urls)
				self.redisConn.sadd("dianping::tag",*link_urls)
				link_tags = site.xpath('dd/ul/li/a/text()')
				for i in range(len(link_tags)):
					postDic["tag_level_1"] = tags[0]
					postDic["tag_level_2"] = link_tags[i]
					postDic["tag_link"] = link_urls[i]
					postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
					postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					self.mysqlConn.insert(dic_list,"storeTag",**postDic)
		except:
			print (sys.exc_info())
		#return link_url

	def StoreUrl(self):

		while self.redisConn.scard("dianping::tag")>0:
	#	while self.redisConn.scard("test") >0 :
			tag = self.redisConn.pop("dianping::tag")
	#		tag = self.redisConn.pop("test")
			url = "http://www.dianping.com"+tag
			print (url)
			
			postDic = {}
			dic_list = ["store_url","store_name","father_url","father_tag","store_score","trade_area","location","cost","review","create_time","update_time","longitude","latitude"]
			
			page = 0
			count = 19
	
			while count>=15 and page<=50:
				page = page+1
				print ("===page==="+str(page))
				try:
					html = self.httpRequest.get(url+'p'+str(page))
					sites = self.httpParser.parseNode(html,'//div[@id="shop-all-list"]/ul/li')
					for site in sites:
						store_urls = site.xpath('div[2]/div[1]/a[1]/@href')
						store_html = self.httpRequest.get("http://www.dianping.com"+store_urls[0])
						
						extract_address = re.findall("({lng:(.*),lat:(.*)})",store_html)
						longitude = extract_address[0][1]
						latitude = extract_address[0][2]
						postDic["longitude"] = longitude 
						postDic["latitude"] =  latitude
						self.saveHtml(store_urls[0],"store",store_html)					
	
						store_names = site.xpath('div[2]/div[1]/a[1]/@title')
						father_tag = site.xpath('div[2]/div[3]/a[1]/span/text()')
   						store_score = site.xpath('div[2]/div[2]/span/@class')
   						trade_area= site.xpath('div[2]/div[3]/a[2]/span/text()')
   						location = site.xpath('div[2]/div[3]/span[@class="addr"]/text()')
   						cost = site.xpath('div[2]/div[2]/a[2]/b/text()')
   						review = site.xpath('div[2]/div[2]/a/b/text()')
   						father_url = tag
						self.redisConn.sadd("dianping::store",store_urls[0])	
						postDic["store_url"] = store_urls[0]
						postDic["store_name"] = store_names[0].replace("'","")
						print (store_names[0])
						postDic["father_url"] = tag
						postDic["father_tag"] = father_tag[0]
						postDic["store_score"] = store_score[0]
						if trade_area:
							postDic["trade_area"] = trade_area[0]
						else :
							postDic["trade_area"] = ''
						postDic["location"] = location[0]
						if cost:
							postDic["cost"] = cost[0]
						else:
							postDic["cost"] = ''
						if review:
							postDic["review"] = review[0]
						else:
							postDic["review"] = ''
						postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                        	postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						self.mysqlConn.insert(dic_list,"store",**postDic)
					self.redisConn.sadd("success::tag::url",url+'p'+str(page))
				
				except:
					self.redisConn.sadd("failed::tag::url",url+'p'+str(page))
					self.redisConn.sadd("failed::tag",tag)
                                        print (sys.exc_info())
				
				count = len(sites)
				time.sleep(5)
		#return link_url


	def UserUrl(self):
		while self.redisConn.scard("dianping::store")>0:
			
			store = self.redisConn.pop("dianping::store") 
			url = "http://www.dianping.com"+store+'/review_more'
			
			dic_list = ["user_url","user_name","user_image","user_level","create_time","update_time"]
			postDic = {}
		
			page = 0
			count = 20 
	
			while count == 20: 
				page = page+1
				try:
					html = self.httpRequest.get(url+'?pageno='+str(page))
					sites = self.httpParser.parseNode(html,'//div[@class="comment-list"]/ul/li')
					for site in sites:
						user_url = site.xpath('div/a/@href')
						print (user_url[0])
						self.redisConn.sadd("dianping::review::user",*user_url)
						self.redisConn.sadd("dianping::wish::user",*user_url)
						self.redisConn.sadd("dianping::checkin::user",*user_url)
						user_name = site.xpath('div/p/a/text()')
						user_image = site.xpath('div/a/img/@src')
						user_level = site.xpath('div/p[2]/span/@class')
						postDic["user_url"] = user_url[0]
						postDic["user_name"] = user_name[0].replace("'","")
						postDic["user_image"] = user_image[0]
						if user_level:
							postDic["user_level"] = user_level[0]
						else:
							postDic["user_level"] = ''
						postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                                postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						self.mysqlConn.insert(dic_list,"user",**postDic)
					self.redisConn.sadd("success::store",store)
				
				except:
					self.redisConn.sadd("failed::store",store)	
					print (sys.exc_info())	

	def UserReviewTrade(self):
	#	while self.redisConn.scard("dianping::review::user")>0:
		while self.redisConn.scard("test")>0:
		#	user = self.redisConn.pop("dianping::review::user")
			user = self.redisConn.pop("test")
			url = "http://www.dianping.com"+user
			print (url)
			postDic = {}
			dic_list = ["user_url","user_name","store_name","store_url","store_score","store_location","review_time","crawl_time","create_time","update_time"]
			
			count = 15
			page = 1

			while count == 15:
				try:
					review_html = self.httpRequest.get(url+'/reviews'+'?pg='+str(page)+'&reviewCityId=2')
					print (url+'/reviews'+'?pg='+str(page)+'&reviewCityId=2')
					sites = self.httpParser.parseHref(review_html,'//div[@id="J_review"]/div[@class="pic-txt"]/ul/li')
					for site in sites:
						store_url = site.xpath('div/div[1]/h6/a/@href')
						print (store_url)
						store_name = site.xpath('div/div[1]/h6/a/text()')
						print (store_name[0])
						store_score = site.xpath('div/div[2]/div[2]/span/@class')
						store_location = site.xpath('div/div[2]/div[1]/p/text()')
						review_time = site.xpath('div/div[2]/div[@class="mode-tc info"]/span[1]/text()')
						review_crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						postDic["user_url"] = user 
						postDic["user_name"] = ''
						postDic["store_name"] = store_name[0]
						postDic["store_url"] = store_url[0]
						postDic["store_score"] = store_score[0]
						postDic["store_location"] = store_location[0]
						postDic["review_time"] = review_time[0]
						postDic["crawl_time"] = review_crawl_time[0]
						postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                                postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						self.mysqlConn.insert(dic_list,"user_review",**postDic)
						
					self.redisConn.sadd("success::review",user)
					page = page+1
					count = len(sites)

				except:	
				 	print (sys.exc_info())	
					self.redisConn.sadd("failed::review",user)		

	def UserWishTrade(self):
	#	while self.redisConn.scard("dianping::wish::user")>0:
		while self.redisConn.scard("test")>0:	
		#	user = self.redisConn.pop("dianping::wish::user")	
			user = self.redisConn.pop("test")
			url = "http://www.dianping.com"+user
			
			dic_list = ["user_url","user_name","store_name","store_url","store_score","store_location","wish_time","crawl_time","create_time","update_time"]
			postDic = {}
			
			count = 30
			page = 1

			while count == 30:
				try:
					wish_html = self.httpRequest.get(url+'/wishlists?pg='+str(page)+'&favorTag=s-1_c-1_t-1')
					sites = self.httpParser.parseNode(wish_html,'//div[@class="pic-txt favor-list"]/ul/li')
					
					for site in sites:
						wish_store_url = site.xpath('div/div[1]/h6/a/@href')
						wish_store_name = site.xpath('div/div[1]/h6/a/text()')
						wish_store_score = site.xpath('div/div[2]/div/p/span[2]/@class')
						wish_store_location = site.xpath('div/div[2]/div[1]/p/text()')
						wish_time = site.xpath('div/div[2]/div[2]/span/i/text()')
						wish_crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						postDic["user_url"] = user
						postDic["user_name"] = ''
						postDic["store_name"] = wish_store_name[0]
						postDic["store_url"] = wish_store_url[0]
						postDic["store_score"] = wish_store_score[0] 
						postDic["store_location"] = wish_store_location[0]
						postDic["wish_time"] = wish_time[0]
						postDic["crawl_time"] = wish_crawl_time[0] 
						postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) 
						postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
						self.mysqlConn.insert(dic_list,"user_wish",**postDic)
					
					self.redisConn.sadd("success::wish",user)
					page = page+1
					count = len(sites)

				except:	
					self.redisConn.sadd("failed::wish",user)
			 		print (sys.exc_info())		


	def UserCheckinTrade(self): 
		
	#	while self.redisConn.scard("dianping::checkin::user")>0:
		while self.redisConn.scard("test")>0:
		#	member = self.redisConn.pop("dianping::checkin::user")
			member = self.redisConn.pop("test")
			url = "http://www.dianping.com"+member
				
			memberId = member.split("/")[2]
			dic_list = ["user_url","user_name","store_name","store_url","store_location","checkin_time","crawl_time","create_time","update_time"]
			postDic = {}			
		
			try:
				checkin_html = self.httpRequest.get(url+'/checkin')
				print (url+'/checkin')	
				total_count = self.httpParser.parseText(checkin_html,'//div[@class="pic-txt head-user"]/div[2]/div[3]/ul/li[4]/a/text()')
				total = re.findall("[1-9]+",total_count[0].encode("utf-8"))[0]
				page = int(total)/20
				
				sites = self.httpParser.parseNode(checkin_html,'//ul[@id="J_list"]/li')
				for site in sites:
					checkin_store_url = site.xpath('h6/a/@href')
					checkin_store_name = site.xpath('h6/a/text()')
					checkin_store_location = site.xpath('p/text()')
					checkin_time = site.xpath('h6/span/text()')
					chechin_crawl_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					postDic["user_url"] = member 
					postDic["user_name"] = ''
					postDic["store_name"] = checkin_store_name[0].replace("'","")
					print (checkin_store_name[0])
					postDic["store_url"] = checkin_store_url[0]
					postDic["store_location"] = checkin_store_location[0]
					postDic["checkin_time"] = checkin_time[0]
					postDic["crawl_time"] = chechin_crawl_time[0]
					postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					self.mysqlConn.insert(dic_list,"user_checkin",**postDic)

				if page :
					for i in range(page):
						time.sleep(5)
						data_form = {"memberId":str(memberId),"page":str(i+2)}
						url = "http://www.dianping.com/ajax/member/checkin/checkinList"
						result = self.httpRequest.post(url,data_form)
						result_list = json.loads(result)["msg"]["checkinList"]
						for checkin in result_list:
							postDic["user_url"] = member
                                       			postDic["user_name"] = ''
                                        		postDic["store_name"] = checkin["shopName"].replace("'","")
                                        		print (checkin["shopName"])
                                        		postDic["store_url"] = ''
                                        		postDic["store_location"] = checkin["shopAddress"]
                                        		postDic["checkin_time"] = checkin["time"]
                                        		postDic["crawl_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                        		postDic["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                                        		postDic["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))						
							self.mysqlConn.insert(dic_list,"user_checkin",**postDic)
				self.redisConn.sadd("success::checkin",member)

			except:	
				self.redisConn.sadd("failed::checkin",member)
			 	print (sys.exc_info())											

	

a = UrlRunnable()
#a.linksUrl()
a.StoreUrl()


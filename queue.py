#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
import threading
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

class Queue:
	def __init__(self):
		self.urls = []
		self.removeUrls = []
		self.errors = []
		self.lock = threading.Lock()
	
	def pop(self):
		self.lock.acquire()
		url = None
		if len(self.urls) >=0:
			url = self.urls.pop()
			self.removeUrls.append(url)
		self.lock.release()
		return url	


	def reverse(self):
		self.urls.reverse()
	
	def size(self):
		return len(self.urls)

	def poll(self, url, force=False):
		self.lock.acquire()
		if self.urls.count([url]) == 0:
			if self.removeUrls.count([url]) == 0:
				self.urls.append(url)
			elif force:
				self.errors.append(url)
		self.lock.release()
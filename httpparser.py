#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class HttpParser:

	def __init__(self):
		pass

	def parseHref(self,content,pattern):
		selector = etree.HTML(content)
		hrefs = selector.xpath(pattern)
		return (hrefs)

	def parseText(self,content,pattern):
		selector = 	etree.HTML(content)
		text = selector.xpath(pattern)
		return text

	def parseNode(self,content,pattern):
		selector = 	etree.HTML(content)
		node = selector.xpath(pattern)
		return node	

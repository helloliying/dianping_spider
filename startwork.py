#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from runnable import UrlRunnable,User
from threadwork import ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#run = UrlRunnable()
run = User()
thread = ThreadPool(runnable=run,num_of_threads = 6)
thread.wait_for_complete()

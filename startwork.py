#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
from runnable import UrlRunnable
from threadwork import ThreadPool

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

run = UrlRunnable()
#run = CompanyRunnable()
#run = CreditRunnable()
#run = LinksRunnable()
#run = ProductRunnable()
#run = ContactRunnable()
thread = ThreadPool(runnable=run,num_of_threads =3)
thread.wait_for_complete()

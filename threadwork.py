#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
import threading
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class  WorkerThread(threading.Thread):

	def __init__(self,runnable,thread_interval=None):
		threading.Thread.__init__(self)
		self.thread_interval = int(1)
		self.runnable = runnable
		self.running = False

	def run(self):
		while self.running:
			try:
				result = self.runnable.run()
				time.sleep(self.thread_interval)
				if result == False:
					self.running = False
			except:
				print (sys.exc_info())
				self.running = False

	def start_running(self):
		self.running = True
		self.start()

	def stop_running(self):
		self.running = False

class ThreadPool:

	def __init__(self,runnable,num_of_threads = None):
		self.threads = []
		self.__createThreadPool(runnable,num_of_threads)

	def __createThreadPool(self,runnable,num_of_threads):
		for i in range(num_of_threads):
			thread = WorkerThread(runnable)
			self.threads.append(thread)
			thread.start_running()

	def wait_for_complete(self):
		while True:
			for thread in self.threads:
				if thread.isAlive() == False:
					thread.join()
					self.threads.remove(thread)

			if len(self.threads):
				break
			#time.sleep(pyspider.config.thread_poll_config.thread_interval)


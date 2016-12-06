#-*-coding:utf8-*-
#! /usr/bin/python
#encoding=utf-8
import logging  
import logging.handlers  

class Logger(object):

    def __init__(self):
        self.logger = self.__createLogger()

    def __createLogger(self):  
    #    LOG_FILE = "/Users/homelink/test/dianping.log"  
        LOG_FILE = "/opt_c/dianping/log/dianping_user.log"
        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 20*1024*1024, backupCount = 10); # 实例化handler  
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)s]"  
        formatter = logging.Formatter(fmt);         # 实例化formatter    
        handler.setFormatter(formatter);            # 为handler添加formatter    
        logger = logging.getLogger('dianping');     # 获取名为xzs的logger    
        logger.addHandler(handler);                 # 为logger添加handler    
        logger.setLevel(logging.DEBUG)
        return logger

    def debug(self,message):
        self.logger.debug(message)

    def info(self,message):
        self.logger.info(message)               
      
  

#! /usr/bin/env python
#-*- coding:utf-8 -*-
import logging, os
from functools import wraps
 
class Logger(object):
    def __init__(self, path='../src/logfiles.log',clevel = logging.WARNING,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        #prt_fmt = logging.Formatter('[%(asctime)s] [%(levelname)s]\n %(message)s', '%Y-%m-%d %H:%M:%S')
        prt_fmt = logging.Formatter('[%(asctime)s]-%(funcName)s-[%(levelname)s]\n %(message)s', '%H:%M:%S')
        #log file to debug for delang
        fmt = logging.Formatter('[%(asctime)s]-[line:%(lineno)d]-FuncName:%(funcName)s-(time:%(relativeCreated)d)-%(levelname)s: %(message)s', '%m-%d %H:%M:%S')
     
        sh = logging.StreamHandler()
        sh.setFormatter(prt_fmt)
        sh.setLevel(clevel)
     
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
 
    def debug(self,message):
        
        self.logger.debug(message)
    #装饰器
    def debug_fun(self,func):

        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = "RUNNING <{}>".format(func.__name__)
            #print(log_string)
            self.logger.info(log_string)
            
# 现在，发送一个通知
            #self.notify()
            try:

                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in "
                err += func.__name__
                self.logger.error(err)
     
                # re-raise the exception
                raise

        return wrapped_function
    
    def info(self,message):
        self.logger.info(message)
 
    def war(self,message):
        self.logger.warn(message)
 
    def error(self,message):
        self.logger.error(message)
    def cri(self,message):
        self.logger.critical(message)
        
class logit(object):
    def __init__(self, path='logfiles.log',clevel = logging.WARNING,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        #prt_fmt = logging.Formatter('[%(asctime)s] [%(levelname)s]\n %(message)s', '%Y-%m-%d %H:%M:%S')
        prt_fmt = logging.Formatter('[%(asctime)s]-%(funcName)s-[%(levelname)s]\n %(message)s', '%H:%M:%S')
        #log file to debug for delang
        fmt = logging.Formatter('[%(asctime)s]-%(funcName)s-%(levelname)s:%(message)s', '%m-%d %H:%M:%S')
     
        sh = logging.StreamHandler()
        sh.setFormatter(prt_fmt)
        sh.setLevel(clevel)
     
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = "Function  <{}>".format(func.__name__)
            print(log_string)
            self.logger.info(log_string)
            
# 现在，发送一个通知
            self.notify()
            try:

                return func(*args, **kwargs)
            except:
                # log the exception
                err = "sThere was an exception in  "
                err += func.__name__
                self.logger.error(err)
     
                # re-raise the exception
                raise

        return wrapped_function
    def notify(self):
# logit只打日志，不做别的
        pass

  
 
if __name__=="__main__":
    logyyx = Logger('yyx.log',logging.ERROR,logging.DEBUG)
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.war('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.cri('一个致命critical信息')
    @logyyx.debug_fun
    def asd(a=0,b=1,v=2):
        logyyx.logger.error('TEST ERROR')
        pass 
    #@logyyx.debug_fun
    #def bd():
        
    #    1/0    
    
    x=asd()
    #y=bd()

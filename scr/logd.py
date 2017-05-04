#! /usr/bin/env python
#coding=gbk
import logging, os
 
class Logger:
    def __init__(self, path,clevel = logging.ERROR,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
       # 打印格式
        prt_fmt = logging.Formatter('[%(asctime)s] [%(levelname)s]\n %(message)s', '%Y-%m-%d %H:%M:%S')
        #储存格式
        fmt = logging.Formatter('%(filename)s-[%(asctime)s]-[%(levelname)s]-line:%(lineno)d\n%(message)s', '%Y-%m-%d %H:%M:%S')

        #设置CMD日志 PRINT 屏幕
        sh = logging.StreamHandler()
        sh.setFormatter(prt_fmt)
        sh.setLevel(clevel)
        #设置文件日志 建立文件夹
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
 
    def debug(self,message):
        self.logger.debug(message)
 
    def info(self,message):
        self.logger.info(message)
 
    def war(self,message):
        self.logger.warn(message)
 
    def error(self,message):
        self.logger.error(message)
    def cri(self,message):
        self.logger.critical(message)
 
if __name__ =='__main__':
 logyyx = Logger('yyx.log',logging.INFO,logging.DEBUG)
 logyyx.debug('一个debug信息')
 logyyx.info('一个info信息')
 logyyx.war('一个warning信息')
 logyyx.error('一个error信息')
 logyyx.cri('一个致命critical信息')

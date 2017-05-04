#! /usr/bin/env python
#coding=gbk
import logging, os
 
class Logger:
    def __init__(self, path,clevel = logging.ERROR,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
       # ��ӡ��ʽ
        prt_fmt = logging.Formatter('[%(asctime)s] [%(levelname)s]\n %(message)s', '%Y-%m-%d %H:%M:%S')
        #�����ʽ
        fmt = logging.Formatter('%(filename)s-[%(asctime)s]-[%(levelname)s]-line:%(lineno)d\n%(message)s', '%Y-%m-%d %H:%M:%S')

        #����CMD��־ PRINT ��Ļ
        sh = logging.StreamHandler()
        sh.setFormatter(prt_fmt)
        sh.setLevel(clevel)
        #�����ļ���־ �����ļ���
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
 logyyx.debug('һ��debug��Ϣ')
 logyyx.info('һ��info��Ϣ')
 logyyx.war('һ��warning��Ϣ')
 logyyx.error('һ��error��Ϣ')
 logyyx.cri('һ������critical��Ϣ')

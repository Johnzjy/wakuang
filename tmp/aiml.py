# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:14:44 2017

@author: 310128142
"""
import aiml
import os
import sys

path=sys.path[0]+'/johnson'
os.chdir(path) #切换工作目录到alice文件夹下，视具体情况而定
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond('LOAD ALICE')

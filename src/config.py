# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:16:26 2017

@author: 310128142
"""

import configparser

#configer= open('user_config.ini','w')
conf =configparser.ConfigParser()

conf.readfp(open('user_config.ini'))
a = conf.get("INI","code")
print(a)


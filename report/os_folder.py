# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:40:38 2017

@author: 310128142
"""

import os
import shutil
import time

s=os.getcwd()
file_list=['base_information', 
           'Brokerage', 
           'CYQ', 
           'MACD_PNG',
           'RSI_SORTING',
           'Trade_Date.csv',
           'unblock']
def remove_file(path,days=3):
    folder_status=os.stat(path)
    #print(folder_status)
    duration=time.time()-folder_status.st_ctime
    if duration > (days*24*360):
         print('this folder creat in %s,clear it!'%time.ctime(folder_status.st_ctime))
         shutil.rmtree(path)
         print('   *'*14)
         print('   *clear done!!*')
         print('   *'*14)
    else :
        print('this object creation time less than %s days'%days)
    
    
    
def clear_macd():
    PATH_LV1=s+'\MACD_PNG'
    if os.path.isdir(PATH_LV1)==True:
        print (time.ctime())
        for child_name in os.listdir(PATH_LV1):
            PATH_LV2=PATH_LV1+'\%s'%child_name
           
            print('')
            print('start clear, ----->[  %s  ]'%child_name)
            print('')
            remove_file(PATH_LV2,days=0)
        print('干净')
    else:
        print('干净')
if __name__=="__main__":
    clear_macd()
    
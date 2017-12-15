# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:14:18 2017

@author: 310128142
"""

'''
DuPontAnalysis
杜邦分析法
测试
'''

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from pylab import * 
import statements



mpl.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
#today=datetime.date.today()
#x=ts.get_profit_data(2017,1)
#x[x.code=='600200']
def roe_load(code,date):
    st_data=statements.Statements(date)
    if st_data.check_files() == True :
        pd=st_data.loading()
        roe= pd[pd['code']==code].roe
        return roe
    else:
        print ('error')
        return np.NaN
     
if __name__=="__main__":
    #x=roe_load('000002','2017-03-01')
    code='000002'
    st='2012-01-01'
    en='2017-09-12'
    df=ts.get_k_data(code,st,en)
    df['roe']=df.date.apply(lambda x:roe_load(code,x))


    
    

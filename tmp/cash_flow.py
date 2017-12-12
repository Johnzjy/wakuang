# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:15:14 2017

@author: 310128142
"""

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
today=datetime.date.today()

class Cash_flow(object):
    def __init__(self,figSN=1):
        
        self.today=datetime.date.today()
        self.code="sh" 
        self.startDate='2016-12-31'
        
        self.endDate='2017-11-28'       
        self.fig=figSN  # this is show which figure 
        self.SN_plt=0  # show how many 
        self.df=pd.DataFrame(self.get_date_ts())
    def get_cf_data(self):
        self.start_strp=datetime.datetime.strptime(self.startDate,"%Y-%m-%d")
        self.cf_data=ts.get_cash_flow(self.code)
        management_cf=self.cf_data.iloc[11]#经营活动产生的现金流量净额 (yuan)
        management_cf=management_cf[1::]
        management_cf.index=management_cf.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))
        investment_cf=self.cf_data.iloc[24]
        investment_cf=investment_cf[1::]
        investment_cf.index=investment_cf.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))
        financing_cf=self.cf_data.iloc[37]#筹资活动产生的现金流量净额
        financing_cf=financing_cf[1::]
        financing_cf.index=financing_cf.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))
        
        
        
        
    def get_date_ts(self):#获取开始数据
        
        self.code_data=ts.get_k_data(self.code,self.startDate,end=self.endDate)
        self.code_data=self.code_data.reset_index()
        self.code_data=self.code_data.sort_index(ascending=True)# 从后倒序
        self.code_data.date=self.code_data.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
        self.code_data=self.code_data.set_index('date')
        if self.endDate == '%s'%self.today:
            todat_realtime=ts.get_realtime_quotes(self.code)
            realtime_price=float(todat_realtime.price)
            realtime_high=float(todat_realtime.high)
            realtime_low=float(todat_realtime.low)
            realtime_open=float(todat_realtime.open)
            realtime_volume=float(todat_realtime.volume)
            
            self.code_data.loc['%s'%self.today,'code']='%s'%self.code
            self.code_data.loc['%s'%self.today,'volume']='%s'%realtime_volume
            self.code_data.loc['%s'%self.today,'open']='%s'%realtime_open
            self.code_data.loc['%s'%self.today,'high']='%s'%realtime_high
            self.code_data.loc['%s'%self.today,'low']='%s'%realtime_low
            self.code_data.loc['%s'%self.today,'close']=realtime_price

    
code='600111'
start='2010-12-22'
end='2017-12-12'
start_strp=datetime.datetime.strptime(start,"%Y-%m-%d")
pd=ts.get_cash_flow(code)
pd.to_csv('cash.csv')
item_name=pd['报表日期']
year=pd.columns[1::]
year=year.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))
management_cf=pd.iloc[11]#经营活动产生的现金流量净额 (yuan)
management_cf=management_cf[1::]
management_cf.index=management_cf.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))
investment_cf=pd.iloc[24]#投资活动产生的现金流量净额
investment_cf=investment_cf[1::]
investment_cf.index=investment_cf.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))
financing_cf=pd.iloc[37]#筹资活动产生的现金流量净额
financing_cf=financing_cf[1::]
financing_cf.index=financing_cf.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))

def get_date_ts(Code,startDate,endDate):#获取开始数据
        
    df=ts.get_k_data(Code,startDate,end=endDate)
    
    df=df.reset_index()
    df=df.sort_index(ascending=True)# 从后倒序
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df.set_index('date')
    if endDate == '%s'%today:
        realtime_price=ts.get_realtime_quotes(Code).price
        realtime_price=float(realtime_price)
        #print('当前价格：%s'%realtime_price)
        df.loc['%s'%today,'close']=realtime_price
    return df

data=get_date_ts(code,start,end)
z=management_cf[management_cf.index>=start_strp]
LAST_NUMBER=management_cf[management_cf.index<start_strp].values[0]
z=z.rename('management_cf_temp')
b=data.join(z)
b=b.fillna(value=0)
def xxxmen(x):
    global LAST_NUMBER
 
    if x==0:
        
        return LAST_NUMBER 
    else:
        LAST_NUMBER =x
        return x

b['management_cf']=b.management_cf_temp.apply(lambda x :xxxmen(x))
ax1=plt.subplot(111)
      
plt.plot(b.index,b.close,"g")
x2=ax1.twinx()#设立爽坐标
plt.plot(b.index,b.management_cf,'r',label='Hilbert')
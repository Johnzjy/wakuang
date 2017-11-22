# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 09:47:46 2017

@author: 310128142
"""


import talib
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

class My_index(object):
    def __init__(self,figSN):
        
        self.today=datetime.date.today()
        self.code="sh" 
        self.startDate='2017-10-31'
        self.endDate='2017-11-14'       
        self.MACD_fastperiod=10 #MACD快速参数
        self.MACD_slowperiod=20#MACD慢速参数
        self.MACD_signalperiod=9#MACD 权重
        self.fig=figSN  # this is show which figure 
        self.SN_plt=0   # show how many 
        self.code_data=self.get_date_ts()
        
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
        return self.code_data
    
    def myMACD(self):
        price=self.code_data['close'].values
        ewma12 = pd.ewma(price,span=self.MACD_fastperiod)
        ewma60 = pd.ewma(price,span=self.MACD_slowperiod)
        dif = ewma12-ewma60
        dea = pd.ewma(dif,self.MACD_signalperiod)
        bar = (dif-dea) 
        print(bar)#有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        return dif,dea,bar
    def myMACD2(self):
        price=self.code_data['close'].values
        ewma12 = pd.Series(price).rolling(window=self.MACD_fastperiod).mean()
        ewma60 = pd.Series(price).rolling(window=self.MACD_slowperiod).mean()
        dif = ewma12-ewma60
        dea = pd.ewma(dif,self.MACD_signalperiod)
        bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        print(bar)
        return dif,dea,bar
    
    def draw_macd(self):
        self.SN_plt=self.SN_plt+1
        #print(self.SN_plt)
        plt.figure(self.SN_plt)
    

    
    #macd, signal, hist = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        macd, signal, hist = self.myMACD()
        ax1=plt.subplot(111)
    
    
        plt.plot(self.code_data.index,self.code_data.close,"y")
        #plt.ylim(df.close.min()-3, df.close.max()+1)
        
        ax2=ax1.twinx()
        plt.plot(self.code_data.index,macd,'r',label='macd dif')   
        plt.plot(self.code_data.index,signal,'b',label='signal dea')
        #plt.bar(df.index,hist,'g',label='hist bar')
        #plt.plot(self.code_data.index,0*df.open,'--')
       # plt.ylim(-1, 3)
        plt.legend(loc='best')
        plt.grid(True)
        
    def draw_macd2(self):
        self.SN_plt=self.SN_plt+1
        print(self.SN_plt)
    

        plt.figure(self.SN_plt)
    #macd, signal, hist = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        macd, signal, hist = self.myMACD2()
        ax1=plt.subplot(111)
    
    
        plt.plot(self.code_data.index,self.code_data.close,"y")
        #plt.ylim(df.close.min()-3, df.close.max()+1)
        
        ax2=ax1.twinx()
        plt.plot(self.code_data.index,macd,'r',label='macd dif')   
        plt.plot(self.code_data.index,signal,'b',label='signal dea')
        #plt.bar(df.index,hist,'g',label='hist bar')
        #plt.plot(self.code_data.index,0*df.open,'--')
       # plt.ylim(-1, 3)
        plt.legend(loc='best')
        plt.grid(True)
    def ST_bands (self):
        '''
        upperband   , 上轨  均线加一倍标准差
        middleband  ，中轨  均线
        lowerband   ，下轨  均线减一倍标准差
    
        '''
        upperband, middleband, lowerband = talib.BBANDS(self.code_data.close.values, timeperiod=10, nbdevup=2, nbdevdn=2, matype=0)
    
        self.code_data['upperband']=upperband
        self.code_data['middleband']=middleband
        self.code_data['lowerband']=lowerband
        return self.code_data
        #print(df)
        
    
    def draw_bands(self):
        plt.plot(self.code_data.index,self.code_data.close,'b')
        plt.plot(self.code_data.index,self.code_data.upperband,'r')
        plt.plot(self.code_data.index,self.code_data.middleband,'k')
        plt.plot(self.code_data.index,self.code_data.lowerband,'r')
        plt.legend(loc='best')
        plt.grid(True)
    
if __name__=="__main__":
    index=My_index(1)
    x=index.ST_bands()
    index.draw_bands()
    print(x)
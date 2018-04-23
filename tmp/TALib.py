
import datetime
import time

import matplotlib.pyplot as plt
import pandas as pd
import talib
import tushare as ts

#import st_imformation as sti

today=datetime.date.today()   # setup date

'''
funcation : download the stock datas as pandas Dataforms
'''

def get_date_ts(Code,startDate,endDate):#获取开始数据

    df=ts.get_k_data(Code,startDate,end=endDate)
    
    df=df.reset_index()
    df=df.sort_index(ascending=True)# 从后倒序
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df.set_index('date')
    if endDate == '%s'%today:
        RealTimeList=ts.get_realtime_quotes(Code)
        df.loc['%s'%today,'close']=float(RealTimeList.price)
        df.loc['%s'%today,'open']=float(RealTimeList.open)
        df.loc['%s'%today,'high']=float(RealTimeList.high)
        df.loc['%s'%today,'low']=float(RealTimeList.low)
        df.loc['%s'%today,'volume']=float(RealTimeList.volume)
    return df

#TODO: timeperiod need adjusts
def AROONOSC(code='sh',startday='2015-01-05',enday='2016-12-21',tp=25):
    """
    AROONOSC is like RSI
    docstring here
        :param code:  stock code of 
        :param startday: start of date
        :param enday: end of date
        :param tp: tp is timeperiod 
    out put:
        dateform as df
    """
    
    df=get_date_ts(code,startday,enday)
    df['aroondown']=talib.AROONOSC(df.high.values,df.low.values,tp)
    print (df)
    return df
def draw_AROONOSC(df): 
    """
    docstring here
        :param df: the data form is pandas 
    """
    ax1=plt.subplot(111)
    plt.plot(df.index,df.close,"g")
    ax2=ax1.twinx()#设立爽坐标
    plt.plot(df.index,df.aroondown,'r',label='DOWN') 
    plt.legend(loc='best')
    plt.grid(True)
    

if __name__=="__main__":
    plt.close()
   #399006 
    '''
   INDEX_LIST = {'sh': 'sh000001', 
                 'sz': 'sz399z001',
                 'hs300': 'sz399300',
                 'sz50': 'sh000016',
                 'zxb': 'sz399005', 
                 'cyb': 'sz399006',
                 'zx300': 'sz399008', 
                 000976 000929 000911 000639 601139
                 'zh500':'sh000905'}
    '''
    code_="sh"
    start_='2016-06-01'
    end_='2018-04-23' 

    for i in range(24,36,1):
        plt.figure(i) 
        VW=AROONOSC(code_,start_,end_,i) 
    #print (VW.AD)
        draw_AROON(VW) 
    plt.show()
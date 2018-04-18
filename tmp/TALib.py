
import talib
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time

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
        realtime_price=ts.get_realtime_quotes(Code).price
        realtime_price=float(realtime_price)
        #print('当前价格：%s'%realtime_price)
        df.loc['%s'%today,'close']=realtime_price
    return df
'''
funcdation : 两只乌鸦
'''
#TODO: this funcation is not adjust the timeperiod . 这一版没有做过测试，
def CDL2CROWS(code='sh',startday='2015-01-05',enday='2016-12-21',tp=11):# MFI - Money Flow Index 
    df=get_date_ts(code,startday,enday)
    
    df['CDL2CROWS']=talib.CDL2CROWS(df.open.values,df.high.values,df.low.values,df.close.values)
    return df
def draw_CDL2CROWS(df): #两只乌鸦
    ax1=plt.subplot(111)
      
    plt.plot(df.index,df.close,"g")
    ax2=ax1.twinx()#设立爽坐标
    plt.plot(df.index,df.CDL2CROWS,'r',label='CDL2CROWS') 
   
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
    code_="600200"
    start_='2017-06-01'
    end_='2018-04-18' 

    #for i in range(3,20,2):
    #plt.figure(i) 
    VW=CDL2CROWS(code_,start_,end_) 
    print (VW)
        #draw_CDL2CROWS(VW) 

     
    #plt.show()


import talib
import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import time


today=datetime.date.today()





def myMACD(price, fastperiod=10, slowperiod=20, signalperiod=9):
    ewma12 = pd.ewma(price,span=fastperiod)
    ewma60 = pd.ewma(price,span=slowperiod)
    dif = ewma12-ewma60
    dea = pd.ewma(dif,span=signalperiod)
    bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar




def draw_macd(code,starttime,endtime):

    
    df=ts.get_hist_data(code,start=starttime,end=endtime)

    df=df.reset_index()
    df=df.sort_index(ascending= False)# 从后倒序
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df.set_index('date')
    if endtime == '%s'%today:
        print ('MACD')
        realtime_price=ts.get_realtime_quotes(code).price
        realtime_price=float(realtime_price)
        print('当前价格：%s'%realtime_price)
        df.loc['%s'%today,'close']=realtime_price

#macd, signal, hist = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

#三个指数都为正
    macd, signal, hist = myMACD(df['close'].values, fastperiod=10, slowperiod=20, signalperiod=9)
    ax1=plt.subplot(111)


    plt.plot(df.index,df.close,"y")
    #plt.ylim(df.close.min()-3, df.close.max()+1)
    
    ax2=ax1.twinx()
    plt.plot(df.index,macd,'r',label='macd dif')   
    plt.plot(df.index,signal,'b',label='signal dea')
    #plt.bar(df.index,hist,'g',label='hist bar')
    plt.plot(df.index,0*df.open,'--')
   # plt.ylim(-1, 3)
    plt.legend(loc='best')
    plt.grid(True)
    

def ewma_day(code_list,days_=30): # 30day EWMA走线
    
    startday=today-datetime.timedelta(days=days_*2)
    
    datas_sh=ts.get_hist_data('sh',start='%s'%startday,end='%s'%today)
  
    every_day=datas_sh.close
    every_day=every_day.reset_index()
    
    every_day=every_day.rename(columns={'close':'szzs'})
    
    for code_ in code_list[1:]:
        datas=ts.get_hist_data(code_,start='%s'%startday,end='%s'%today)
        
        every_day1=datas.close

        #every_day1=every_day1.reset_index()
        ewma30 = pd.ewma(every_day1.values,span=days_)
        #print(ewma30)
        every_day1=pd.Series(data=ewma30,index=every_day1.index,name=code_)
        every_day1=every_day1.reset_index()
        
        
        every_day=pd.merge(every_day,every_day1,on='date',how='outer')
        #every_day=every_day.rename(columns={'close':'%s'%code_})
    
    


    every_day.date=every_day.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    every_day=every_day.set_index('date')
    every_day=every_day.sort_index(ascending= False)# 从后倒序
    
        


    

    return every_day
'''
布林线上下轨
'''
def ST_bands (code,startday,enday):
    '''
    upperband   , 上轨  均线加一倍标准差
    middleband  ，中轨  均线
    lowerband   ，下轨  均线减一倍标准差
    返回 df


    '''
    
    df=ts.get_hist_data(code,start=startday,end=enday)
    df=df.reset_index()
    df=df.sort_index(ascending= False)# 从后倒序
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df.set_index('date')
    if enday == '%s'%today:
        realtime_price=ts.get_realtime_quotes(code).price
        realtime_price=float(realtime_price)
        print('当前价格：%s'%realtime_price)
        df.loc['%s'%today,'close']=realtime_price
    
    upperband, middleband, lowerband = talib.BBANDS(df.close.values, timeperiod=10, nbdevup=2, nbdevdn=2, matype=0)

    df['upperband']=upperband
    df['middleband']=middleband
    df['lowerband']=lowerband
    #print(df)
    return df

def draw_bands(df):
    plt.plot(df.index,df.close,'b')
    plt.plot(df.index,df.upperband,'r')
    plt.plot(df.index,df.middleband,'k')
    plt.plot(df.index,df.lowerband,'r')
    plt.legend(loc='best')
    plt.grid(True)


def VWAP(code='sh',startday='2015-01-05',enday='2016-12-21'):# price 加权平均指标
   
    
    
    SQ={'slower_line':24,'middler_line':6,'fast_line':2}
    if code == 'sh':
        SQ['slower_line']=12
    
    df=ts.get_hist_data(code,start=startday,end=enday)
    df['pvc']=df.close*df.volume
    df=df.reset_index()
    df=df.sort_index(ascending= False)# 从后倒序
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df.set_index('date')
    
    if enday == '%s'%today:
        realtime_price=ts.get_realtime_quotes(code).price
        realtime_price=float(realtime_price)
        print('当前价格：%s'%realtime_price)
        df.loc['%s'%today,'close']=realtime_price
    for name in SQ:
        values=SQ['%s'%name]
        #print(values)
        cnt = 0
        for i in df.index[values-1:]:
            pv_sum=df[cnt:cnt+values].pvc.sum()
            vlo_sum=df[cnt:cnt+values].volume.sum()
            df.loc[i,'%s'%name]=pv_sum/vlo_sum
            cnt= cnt+1
    return df

def draw_VWAP(df): # 画加权平均指数
      
    plt.plot(df.index,df.close,'R',linewidth=2.0)
    plt.plot(df.index,df.slower_line,'B')
    plt.plot(df.index,df.middler_line,'orange')
    plt.plot(df.index,df.fast_line,'g')
    plt.legend(loc='best')
    plt.grid(True) 
    
'''
RSI强弱指标

'''
    
def RSI(code='sh',startday='2015-01-05',enday='2016-12-21',timeperiod=10):# price 加权平均指标    
    #timeperiod=1
    if code == 'sh':
        timeperiod=10
    
    df=ts.get_hist_data(code,start=startday,end=enday)
    
    df=df.reset_index()
    df=df.sort_index(ascending= False)# 从后倒序
    df.date=df.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
    df=df.set_index('date')
    df['RSI']=talib.RSI(df.close.values,timeperiod)
    
    return df

def draw_RSI(df): # 画加权平均指数
    ax1=plt.subplot(111)
      
    plt.plot(df.index,df.close,"b")
    #plt.ylim(df.close.min()-3, df.close.max()+1)
    ax2=ax1.twinx()

    plt.plot(df.index,df.RSI,'g',label='RSI')    


    plt.plot(df.index,0*df.open+30,'--')
    plt.plot(df.index,0*df.open+50,'--')
    plt.plot(df.index,0*df.open+70,'--')
   # plt.ylim(-1, 3)
    plt.legend(loc='best')
    plt.grid(True)

if __name__=="__main__":
    code_='sz'
    start_='2016-01-01'
    end_='2017-03-06'
    
    plt.figure(1)
    VW=VWAP(code_,start_,end_)
    draw_VWAP(VW)
    
    
    plt.figure(2)
    brand=ST_bands(code_,start_,end_)
    draw_bands(brand)
    
    plt.figure(3)
    draw_macd(code_,start_,end_)
    
    plt.figure(4)
    RSI_IDEX=RSI(code_,start_,end_)
    draw_RSI(RSI_IDEX)
   
    plt.show()


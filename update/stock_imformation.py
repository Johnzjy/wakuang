# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 09:54:34 2017

@author: 310128142
fuction: 
    download imformation/下载基本信息
    download 
"""

import tushare as ts
import pandas as pd
import datetime
import sys
from numpy import nan as NaN
sys.path.append("..")
from scr import logd
import json

today=datetime.date.today()


log_STI=logd.Logger('downloading_information.log')

log_STI.info('%s开始下载基本数据信息%s'%('='*16,'='*16))

information_dict={"code"    :"代码",
                  "name"    :"名称",
                  "industry":"所属行业",
                  "area"    :"地区",
                  "pe"      :"市盈率",
                  "outstanding":"流通股本(亿)",
                  "totals":"总股本(亿)",
                  "totalAssets":"总资产(万)",
                   "liquidAssets":"流动资产",
                   "fixedAssets":"固定资产",
                   "reserved":"公积金",
                   "reservedPerShare":"每股公积金",
                   "esp":"每股收益",
                   "bvps":"每股净资",
                   "pb":"市净率",
                   "timeToMarket":"上市日期",
                   "undp":"未分利润",
                   "perundp":"每股未分配",
                   "rev":"收入同比(%)",
                   "profit":"利润同比(%)",
                   "gpr":"毛利率(%)",
                   "npr":"净利润率(%)",
                   "holders":"股东人数"
                   

                   }

def downloading_information(time=3,SAVE=False):
    try :
        ST_basics=ts.get_stock_basics()
        ST_basics=pd.DataFrame(ST_basics)
    except:
        log_STI.error('\n>>basics没有计算成功')
    print (ST_basics.head(9))
    for year in range(2015,2017):
        print(year)
        for Q in range(1,5):
            print(Q)
            ST_basics=download_ACH_Q(year,Q,ST_basics)
    
    if SAVE== True:
        import os
        path=os.path.dirname(os.getcwd())+'\\report\\base_information\\' # 存储路径
        ST_basics.to_csv(path+'Stock_Information.csv',encoding='gbk',header=True)
    return ST_basics

def download_ACH_Q(year,quarter,df):#按照季度获取信息
    Data=df
    try :
        
        achievement=ts.get_report_data(year,quarter)
        achievement=pd.DataFrame(achievement)
    except:
        pass
    achievement=achievement.set_index('code')
    achievement=achievement.sort_index()
    for title_name in achievement.columns:
        print (title_name)
        for code_ in achievement.index[1:]:
            if achievement.at['%s'%code_,'%s'%title_name]!=NaN:
                
                try:
                    #print(achievement.at['%s'%code_,'%s'title_name])
                    Data.ix['%s'%code_,'%s-%s-%s'%(title_name,year,quarter)]=achievement.at['%s'%code_,'%s'%title_name]
                except:
                    buf=achievement.at['%s'%code_,'%s'%title_name]
                    Data.ix['%s'%code_,'%s-%s-%s'%(title_name,year,quarter)]=buf[0]
            else:
                pass
                #print (code_,title_name)
        #print (achievement.head(9))
    return Data

def get_trade_date():# 网上获得交易日期
    data=ts.trade_cal()
    open_day=data[ data.isOpen>0 ]
    open_day['Quarter']=''
    for i in open_day.index:
        DATE=open_day.at[i,'calendarDate']
        
        month=DATE[5:7]
        if month >= '01' and month <='03':
            Qua=DATE[2:4]+'Q1'
        elif month >= '04' and month <='06':
            Qua=DATE[2:4]+'Q2'
        elif month >= '07' and month <='09':
            Qua=DATE[2:4]+'Q3'  
        elif month >= '10' and month <='12':
            Qua=DATE[2:4]+'Q4'
        
        open_day.at[i,'Quarter']=Qua
        
        print(DATE,Qua)
       
    return open_day

def downloading_trade_date():# 存储交易日期
    data=get_trade_date()
    data=data.set_index('calendarDate')    
    import os
    path=os.path.dirname(os.getcwd())+'\\report\\' # 存储路径
    data.to_csv(path+'Trade_Date.csv',encoding='gbk',header=True)
def trade_calendar(year=today.year):#获取一年交易日期 默认为今年
    '''
    item  calendarDate  isOpen Quarter
    '''
    data=pd.read_csv("..\\report\\Trade_Date.csv",encoding='gbk')
    data=data[data['calendarDate']>="%s-01-01"%year]
    data=data[data['calendarDate']<="%s-12-31"%year]
    data=data.set_index('calendarDate')
 
    return data
    
if __name__ == "__main__":
    #x=downloading_information(SAVE=True)
    #x=downloading_trade_date()
    print(trade_calendar())
    
    
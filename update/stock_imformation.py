# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 09:54:34 2017

@author: 310128142
"""

import tushare as ts
import pandas as pd
import datetime
import sys
from numpy import nan as NaN
sys.path.append("..")
from scr import logd

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

def download_ACH_Q(year,quarter,df):
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

if __name__ == "__main__":
    x=downloading_information(SAVE=True)
    
    
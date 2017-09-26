__author__ = 'johnson'

import pandas as pd
import os

def Daily_data(file_tod,file_yes):
    datas_tod= pd.read_csv(file_tod,encoding='gbk')# 读取今天数据
    datas_yes= pd.read_csv(file_yes,encoding='gbk')# 读取昨天数据


    df_broker_tod = datas_tod.set_index(['broker'])
    df_broker_yes = datas_yes.set_index(['broker'])
    datas_tod=datas_tod.sort_index()
    datas_yes=datas_yes.sort_index()
    new_datas= df_broker_tod
    new_datas['今日买入']= '今日新数据'
    new_datas['今日卖出']= '今日新数据'

    for broker_tod in datas_tod['broker']:

        for broker_yes in datas_yes['broker']:


            if broker_yes == broker_tod :
                ixdata_tod= df_broker_tod.ix['%s'%broker_tod] # 检索出这一行的数据
                ixdata_yes= df_broker_yes .ix['%s'%broker_tod]
                new_datas.loc['%s'%broker_tod,'昨日top3']=ixdata_yes['top3']
                new_datas.loc['%s'%broker_tod,'今日买入']= ixdata_tod['bamount']-ixdata_yes['bamount']
                new_datas.loc['%s'%broker_tod,'今日卖出']= ixdata_tod['samount']-ixdata_yes['samount']



    return new_datas




if __name__ == "__main__":

    today_ ='2017-09-21'
    lasttime_='2017-09-18'
    path= '../database/Brokerage/%s/%s_当天买卖5D'%(today_,today_)
    file_tod='../database/Brokerage/%s/%s_Brokerage5D_csv.csv'%(today_,today_)
    file_yes='../database/Brokerage/%s/%s_Brokerage5D_csv.csv'%(lasttime_,lasttime_)
    new=Daily_data(file_tod,file_yes)
    new.to_csv(path + '_csv.csv')
    with pd.ExcelWriter(path + '_excel.xlsx') as writer:
         new.to_excel(writer, sheet_name='Sheet1')

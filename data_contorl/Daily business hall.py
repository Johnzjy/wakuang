__author__ = 'johnson'

import pandas as pd
import os

def Daily_data(today,lastday):
    path= '../report/Brokerage/%s/%s_当天买卖5D'%(today,today)
    file_tod='../report/Brokerage/%s/%s_Brokerage5D_csv.csv'%(today,today)
    file_yes='../report/Brokerage/%s/%s_Brokerage5D_csv.csv'%(lastday,lastday)
    
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
                ixdata_yes= df_broker_yes.ix['%s'%broker_tod]
                new_datas.loc['%s'%broker_tod,'昨日top3']=ixdata_yes['top3']
                new_datas.loc['%s'%broker_tod,'今日买入']= ixdata_tod['bamount']-ixdata_yes['bamount']
                new_datas.loc['%s'%broker_tod,'今日卖出']= ixdata_tod['samount']-ixdata_yes['samount']
    new_datas.to_csv(path + '_csv.csv')
    with pd.ExcelWriter(path + '_excel.xlsx') as writer:
         new_datas.to_excel(writer, sheet_name='Sheet1')
    return new_datas

def ORG_daily(today,lastday):
    path= '../report/Brokerage/%s/%s_当天机构5D'%(today,today)
    file_tod='../report/Brokerage/%s/%s_org_top5D_csv.csv'%(today,today)
    file_yes='../report/Brokerage/%s/%s_org_top5D_csv.csv'%(lastday,lastday)
    
    datas_tod= pd.read_csv(file_tod,encoding='gbk')# 读取今天数据
    datas_yes= pd.read_csv(file_yes,encoding='gbk')# 读取昨天数据
    

    datas_tod['code']=datas_tod['code'].map(lambda x:str(x).zfill(6))
    datas_yes['code']=datas_yes['code'].map(lambda x:str(x).zfill(6))
    df_tod = datas_tod.set_index(['code'])
    df_yes = datas_yes.set_index(['code'])
    datas_tod=datas_tod.sort_index()
    datas_yes=datas_yes.sort_index()
    new_datas= df_tod

    new_datas['bamount_last']=  None
    new_datas['samount_last']= None
    new_datas['net_last']=  None
    new_datas['Diff_buy']=  None
    new_datas['Diff_sell']=  None
    new_datas['Diff_net']=  None


    for code_tod in datas_tod['code']:

        for code_yes in datas_yes['code']:


            if code_yes == code_tod :
              
                ixdata_tod= df_tod.ix['%s'%code_tod] # 检索出这一行的数据

            
                ixdata_yes= df_yes.ix['%s'%code_tod]
            
                new_datas.loc['%s'%code_tod,'bamount_last']=ixdata_yes['bamount']
                new_datas.loc['%s'%code_tod,'samount_last']=ixdata_yes['samount']
                new_datas.loc['%s'%code_tod,'net_last']=ixdata_yes['net']
                new_datas.loc['%s'%code_tod,'Diff_buy']= ixdata_tod['bamount']-ixdata_yes['bamount']
                new_datas.loc['%s'%code_tod,'Diff_sell']= ixdata_tod['samount']-ixdata_yes['samount']

                new_datas.loc['%s'%code_tod,'Diff_net']= ixdata_tod['net']-ixdata_yes['net']
    new_datas.loc['SUM']=new_datas.sum()
    
    print(new_datas)
    new_datas.to_csv(path + '_csv.csv')
    with pd.ExcelWriter(path + '_excel.xlsx') as writer:
         new_datas.to_excel(writer, sheet_name='Sheet1')
    return new_datas


if __name__ == "__main__":

    today_ ='2017-11-22'
    lasttime_='2017-10-12'
    Daily_data(today_,lasttime_)
    ORG_daily(today_,lasttime_)


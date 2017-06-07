# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 09:51:04 2017

@author: 310128142
"""

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import tqdm

def changed_rate_stock(code,start,end):
    df=ts.get_hist_data(code,start,end)
    max_high=df.high.max()
    min_low =df.low.min()
    mean_price=df.close.mean()
    rate= (max_high-min_low)/mean_price*100
    return rate
#查询所有股票这段时间的变化率
def changed_rate_list(code_list,start,end):
    dict_code=pd.DataFrame(code_list,columns=['code'])
    dict_code['changed']=0
    dict_code=dict_code.set_index('code')
    for code in tqdm.tqdm(code_list[0:20],leave=False):
        pre=changed_rate_stock(code,start,end)
        dict_code.loc[code,'changed']=pre
    return dict_code
def changed_rate_all()


if __name__=="__main__":
    code_='sh'
    start_='2017-01-01'
    end_='2017-06-01'
    code_list=pd.read_csv('../list/stock_code_all.csv',encoding='gbk',engine='python')
    code_list.code=code_list.code.apply(lambda x:'%06d'%x)
    x=changed_rate_list(code_list.code,start_,end_)

    print(x)
    #unchanged(code_,start_,end_)
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:36:08 2018

@author: 310128142
"""

import tushare as ts
import pandas as pd
import time
import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
import tqdm

def get_magic(code):
    ProfitDF=ts.get_profit_statement(code)
    ProfitDF=ProfitDF.loc[[8,18,19],]
    ProfitDF=ProfitDF.drop(['报表日期'],axis=1)
    ProfitDF=ProfitDF.astype(np.float64)
    EBIT=ProfitDF.sum()
    BalanceDF=ts.get_balance_sheet(code)
    BalanceDF=BalanceDF.loc[[18,26,41]]
    BalanceDF=BalanceDF.drop(['报表日期'],axis=1)

    BalanceDF=BalanceDF.astype(np.float64)
    BalanceDF=BalanceDF.fillna(0)
    Assets= BalanceDF.loc[18]- BalanceDF.loc[41]+BalanceDF.loc[26]
    magic=EBIT/Assets

   
    #print(magic)
    return magic

def list_input(mode='sh'):
    code_dict={'all':'stock_code_all',
           'sh':'stock_code_sh',
           'cy':'stock_code_cy',
           'sz':'stock_code_sz',
           }
    if mode in code_dict.keys():
        search_file=code_dict[mode]+'.csv'
        #print (search_file)
    else:
        search_file=mode+'.csv'
    print (search_file)
    
    try:

        f=open('..\\list\\%s'%search_file)

        LIST_=pd.read_csv(f)
    except IOError:
        print('can not find files,please change mode.')
        print(os.listdir('list'))
    if LIST_ is not None:
 #       LIST_ = LIST_.drop_duplicates('code')
        LIST_['code'] = LIST_['code'].map(lambda x:str(x).zfill(6))
    return LIST_

def get_all_magic():
    CodeList=list_input('all')
    
    #print(CodeList)
    i=2
    df=get_magic(CodeList.code[i*50])
    df=df.sort_index(ascending =False)
    for code_ in tqdm.tqdm_gui(CodeList.code[i*50+1:i*50+50]):
        time.sleep(3)
        print(code_)
        mg=get_magic(code_)

        mg.name=code_
        df=pd.concat([df,mg],axis=1)
    df.to_csv('..\\report\\magic_%s.csv'%CodeList.code[i*50])
    return df
if __name__=="__main__":
    x=get_all_magic()
    #x.to_csv('..\\report\\magic_600001.csv')
    #x=get_magic('600760')

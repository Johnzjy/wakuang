# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:35:22 2017

@author: 310128142
"""

import technical_indicators as ti
import matplotlib.pyplot as plt
import pandas as pd
import os
import tqdm
import datetime
'''
显示中文文件头
'''
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
code_dict={'all_code':'stock_code_all',
           'sh':'stock_code_sh',
           'cy':'stock_code_cy',
           'sz':'stock_code_sz',
           }
def list_input(mode='sh'):
    if mode in code_dict.keys():
        search_file=code_dict[mode]+'.csv'
        #print (search_file)
    else:
        search_file=mode+'.csv'
    print (search_file)
    
    try:
        f=open('list\\%s'%search_file)
        print (f)
        LIST_=pd.read_csv(f)
    except IOError:
        print('can not find files,please change mode.')
        print(os.listdir('list'))
    '''
    if mode == 'sh': 
        LIST_=pd.read_csv('list/stock_code_sh.csv',encoding='gbk')
    elif mode == 'sz':
        LIST_=pd.read_csv('list/stock_code_sz.csv',encoding='gbk')
    elif mode == 'cy':
        
        LIST_=pd.read_csv('list/stock_code_cy.csv',encoding='gbk')
    else:
        pass
    '''
    if LIST_ is not None:
 #       LIST_ = LIST_.drop_duplicates('code')
        LIST_['code'] = LIST_['code'].map(lambda x:str(x).zfill(6))
    return LIST_

def save_MACD_all(mode,starttime,endtime):
    '''
    保存所有的MACD图
    '''
    DataFame_list = list_input(mode)
    list_code =list(DataFame_list.values)
    files_path= 'report/MACD_PNG/%s'%mode
    if os.path.exists('report/MACD_PNG') == False:
        os.mkdir('report/MACD_PNG')
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.mkdir(files_path)                # 创建目录
    for code_name in tqdm.tqdm(list_code):    
        print(code_name[0],code_name[1])
        fig = plt.figure('%s-%s'%(code_name[0],code_name[1]),figsize=(8, 8))
        fig.set_label('%s'%code_name[1])
        try:
            ti.draw_macd('%s'%code_name[0],starttime,endtime)
        except:
            continue
        fig.suptitle('%s'%code_name[1])

        fig.savefig('report/MACD_PNG/%s/%s.png'%(mode,code_name[0]))
        plt.close(fig) 
'''
存储RSI的图片
'''
def RSI_sorting(mode):
    DataFame_list = list_input(mode)
    list_code =list(DataFame_list.values)
    RSI_df=DataFame_list.set_index('code')
    RSI_df['RSI']=0
   
    endtime='%s'%datetime.date.today()
    starttime='2016-01-01'
    for code_name in tqdm.tqdm(list_code):
        try:
            rsi_=ti.RSI('%s'%code_name[0],starttime,endtime)
            rsi_=rsi_['RSI']
          
            #print(rsi_)
        except:
            continue
        for time_f,data in rsi_.iteritems():
            time_str=str(time_f)[0:10]
            
            RSI_df.loc['%s'%code_name[0],time_str]=data
        
    files_path= 'report/RSI_SORTING/%s'%mode
    if os.path.exists('report/RSI_SORTING') == False:
        os.mkdir('report/RSI_SORTING')
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.mkdir(files_path)                # 创建目录
    RSI_df.to_csv(files_path+'/RSI_sorting_%s.csv'%endtime)   
    print(RSI_df)
    return RSI_df
if __name__=="__main__":

    mode_='sz'
    start_='2016-10-01'
    end_='2019-04-09'
    save_MACD_all(mode_,start_,end_)
    RSI_sorting(mode_)

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 09:35:22 2017

@author: 310128142
"""

import technical_indicators as ti
import matplotlib.pyplot as plt
import pandas as pd
import tqdm
'''
显示中文文件头
'''
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def list_input(mode='sh'):
    
    if mode == 'sh': 
        LIST_=pd.read_csv('list/stock_code_sh.csv',encoding='gbk')
    elif mode == 'sz':
        LIST_=pd.read_csv('list/stock_code_sz.csv',encoding='gbk')
    elif mode == 'cy':
        
        LIST_=pd.read_csv('list/stock_code_cy.csv',encoding='gbk')
    else:
        pass
    LIST_.code=LIST_.code.apply(lambda x:'%06d'%x)
   # LIST_=LIST_.set_index('code')

    return LIST_

DataFame_list = list_input(mode = 'sh')
list_code =list(DataFame_list.values)
start_='2016-07-01'
end_='2017-09-24'
for code_name in tqdm.tqdm(list_code):
    print(code_name[0],code_name[1])
    fig = plt.figure('%s-%s'%(code_name[0],code_name[1]),figsize=(8, 8))
    fig.set_label('%s'%code_name[1])
    try:
        ti.draw_macd('%s'%code_name[0],start_,end_)
    except:
        continue
    fig.suptitle('%s'%code_name[1])
    fig.savefig('report/MACD_PNG/sh/%sw.png'%code_name[0])
    plt.close(fig) 

#plt.show()

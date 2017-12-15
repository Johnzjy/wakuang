# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 08:35:53 2017

@author: 310128142
"""

import tushare as ts
import pandas as pd
import time
import os
import tqdm 
import datetime
from numpy import NaN

class Statements(object):
    #初始化变量

    def __init__(self,data):
        self.data=data
        y,q=date_span(data)
        
        self.set_year=y
     
        self.set_quarter =q



            
            
    def performance(self,flag=True):
        '''
        code,代码
        name,名称
        esp,每股收益
        eps_yoy,每股收益同比(%)
        bvps,每股净资产
        roe,净资产收益率(%)
        epcf,每股现金流量(元)      remove
        net_profits,净利润(万元)
        profits_yoy,净利润同比(%)
        distrib,分配方案           remove
        report_date,发布日期

        下载基本变量
        '''
        print ('正在收集战争报告')
        self.data=ts.get_report_data(self.set_year,self.set_quarter)
        self.data.code=self.data.code.apply(lambda x:int(x))
        self.data=self.data.set_index('code')
        self.data=self.data.drop('distrib',axis=1)
        self.data=self.data.drop('epcf',axis=1)
        self.data=self.data.drop('report_date',axis=1)
        self.data=self.data.drop('bvps',axis=1)
        '''
        利润表￥￥￥￥￥
        code,代码
        name,名称               remove
        roe,净资产收益率(%)      remove
        net_profit_ratio,净利率(%)
        gross_profit_rate,毛利率(%)
        net_profits,净利润(万元) remove
        esp,每股收益             remove
        business_income,营业收入(百万元)
        bips,每股主营业务收入(元)
        '''
        print('\n正在统计战利品')
        self.profit=ts.get_profit_data(self.set_year,self.set_quarter)
        self.profit.code=self.profit.code.apply(lambda x:int(x))
        self.profit=self.profit.set_index('code')
        profit_name=self.profit.pop('name')
        profit_eps=self.profit.pop('eps')
        profit_roe=self.profit.pop('roe')
        profit_net_profits=self.profit.pop('net_profits')
        self.data=pd.merge(self.data,self.profit,how='outer',left_index=True,right_index=True)
        self.data=self.data.reset_index()
        self.data=self.data.drop_duplicates('code',keep='first')
        self.data=self.data.set_index('code')
        '''
        运营能
        code,代码
        name,名称
        arturnover,应收账款周转率(次)
        arturndays,应收账款周转天数(天)
        inventory_turnover,存货周转率(次)
        inventory_days,存货周转天数(天)
        currentasset_turnover,流动资产周转率(次)
        currentasset_days,流动资产周转天数(天)
        '''
        print('\n手残还要秀操作')
        self.opration=ts.get_operation_data(self.set_year,self.set_quarter)
        self.opration.code=self.opration.code.apply(lambda x:int(x))
        self.opration=self.opration.set_index('code')
        self.opration=self.opration.drop('name',axis=1)
        self.data=pd.merge(self.data,self.opration,how='outer',left_index=True,right_index=True)
        self.data=self.data.reset_index()
        self.data=self.data.drop_duplicates('code',keep='first')
        self.data=self.data.set_index('code')
        '''
        成长能力
        code,代码
        name,名称
        mbrg,主营业务收入增长率(%)
        nprg,净利润增长率(%)
        nav,净资产增长率
        targ,总资产增长率
        epsg,每股收益增长率
        seg,股东权益增长率
        '''
        print('\n成长指数重新分配')
        self.growth=ts.get_growth_data(self.set_year,self.set_quarter)
        self.growth.code=self.growth.code.apply(lambda x:int(x))
        self.growth=self.growth.set_index('code')
        self.growth=self.growth.drop('name',axis=1)
        self.data=pd.merge(self.data,self.growth,how='outer',left_index=True,right_index=True)
        self.data=self.data.reset_index()
        self.data=self.data.drop_duplicates('code',keep='first')
        self.data=self.data.set_index('code')
        
        if flag == True:
            self.data=self.data.reset_index()
            self.data.to_csv('../report/base_information/perfprmance_%s-%s.csv'%(self.set_year,self.set_quarter),encoding='gbk',index=False)
            print ('this files have saved')
        elif flag == False:
            pass
        return self.data
    def check_files(self,file=''):
        file_list=os.listdir('../report/base_information/')
        if file =='':
            file = 'perfprmance_%s-%s.csv'%(self.set_year,self.set_quarter)
        else :
            pass
   
        if file in file_list:

            return True
        else:

            return False
        
    def loading(self):
        result_down=self.check_files()
        if result_down == False:
            self.performance()
            print ('%s - %s downloading has done'%(self.set_year,self.set_quarter))
        elif result_down == True:
            print ('%s - %s already downloading'%(self.set_year,self.set_quarter))
        data=pd.read_csv('../report/base_information/perfprmance_%s-%s.csv'%(self.set_year,self.set_quarter),encoding='gbk')
        data.code=data.code.map(lambda x:str(x).zfill(6))

        return data
    def update(self,flag_u= False):
        result_down=self.check_files()
        if result_down == True:
            file_time=os.path.getmtime('../report/base_information/perfprmance_%s-%s.csv'%(self.set_year,self.set_quarter))

            if  (time.time() - file_time)>(24*60*60*30) or flag_u==True:#小于一周
                print ('文件需要更新')
                os.remove('../report/base_information/perfprmance_%s-%s.csv'%(self.set_year,self.set_quarter))
                print ('删除旧文件')
                self.performance()
            else:
                print ('this file do not update')
                
        else:
            self.performance()
            
    def add_label(self):
        result_down=self.check_files()
        if self.set_quarter==1:
            self.startday='%s-04-25'%self.set_year
            self.endday='%s-07-25'%self.set_year
        elif  self.set_quarter==2:
            self.startday='%s-07-25'%self.set_year
            self.endday='%s-10-25'%self.set_year
        elif  self.set_quarter==3:
            self.startday='%s-10-25'%self.set_year
            self.endday='%s-01-25'%(self.set_year+1)
        elif  self.set_quarter==4:
            self.startday='%s-01-25'%(self.set_year+1)
            self.endday='%s-04-25'%(self.set_year+1)
        else:
            print ('季度输入错误')
            
        
        if result_down == True:
            data=pd.read_csv('../report/base_information/perfprmance_%s-%s.csv'%(self.set_year,self.set_quarter),encoding='gbk')
            data.code=data.code.apply(lambda x:'%06d'%x)
            data['earnings']=NaN
            data['fluctuate']=NaN
            
            for item,code_ in  tqdm.tqdm_gui(enumerate(data.code)):
                
                print (item,code_,self.startday,self.endday)
                try:
                    df=ts.get_k_data(code_,self.startday,self.endday)
                    price=df.close
                    price_f=price.iloc[0]
                    price_e=price.iloc[-1]
                    price_max=price.max()
                    price_min=price.min()
                    return_r=(price_e-price_f)/price_f*100 # 收入
                    p_range=(price_max-price_min)/price_min*100 #波动
                    data.ix[item,['earnings']]=return_r
                    data.ix[item,['fluctuate']]=p_range
                    print(price_f,price_e,price_max,price_min)
                    print(return_r.round(-1),p_range.round(-1))
                   
                except:
                    pass
            data.to_csv('../report/base_information/perfprmance_earn_%s-%s.csv'%(self.set_year,self.set_quarter),encoding='gbk',index=False)  

        else:
            pass
        
def date_span(date):
 
    date_trap=datetime.datetime.strptime(date,'%Y-%m-%d')
    m=date_trap.month
    y=date_trap.year
    if m>=1 and m<4:return y,1
    elif m>=4 and m<7:return y,2
    elif m>=7 and m<10:return y,3
    elif m>=10 and m<13:return y,4
    else:
        raise ValueError('datetime error ：%s'%date)        
   
if __name__=="__main__":
    x=Statements('2012-12-01')

    #x.update(flag_u=True)
    #x.update()
    #print(x.loading())
    
    #x.add_label()



# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 11:15:14 2017

@author: 310128142
"""

import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
from pylab import * 
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

mpl.rcParams['font.sans-serif'] = ['SimHei'] #显示中文
today=datetime.date.today()

Cash_item_dic={11:'management_cf',#经营活动产生的现金流量净额
               24:'investment_cf',#投资活动产生的现金流量净额
               37:'financing_cf'#融资活动产生的现金流量净额
               }

    
    
class Cash_flow(object):
    def __init__(self,code_="600111",start_='2016-12-31',end_='2017-11-28'  ):
        
        self.today=datetime.date.today()
        self.code=code_
        self.startDate=start_
        self.endDate=end_   
        self.fig=1  # this is show which figure 
        self.SN_plt=0  # show how many 
        self.get_date_ts()
     
        
        
    def get_cf_data(self,Item_cf):
        cash_name=Cash_item_dic[Item_cf] #get the item name from dict cash folw 
        print (cash_name)
        self.start_strp=datetime.datetime.strptime(self.startDate,"%Y-%m-%d")# deal datetime to strp
        self.cf_data=ts.get_cash_flow(self.code) #get cash flow data
        
        cash_flow_amount=self.cf_data.iloc[Item_cf]#经营活动产生的现金流量净额 (yuan)
        cash_flow_amount=cash_flow_amount[1::] # pass title 
        cash_flow_amount.index=cash_flow_amount.index.map(lambda x:datetime.datetime.strptime(x,"%Y%m%d"))# deal time
        cash_flow_amount_temp=cash_flow_amount[cash_flow_amount.index>=self.start_strp]# 切片一段时间内的 cash flow 数据
        self.MCF_last=cash_flow_amount[cash_flow_amount.index<self.start_strp].values[0]# 获取最后开始时候的cash flow
        cash_flow_amount_temp=cash_flow_amount_temp.rename('%s_temp'%cash_name)#rename Item
        self.code_data=self.code_data.join(cash_flow_amount_temp)# 将 cash flow  数据加入 总数据
        self.code_data=self.code_data.fillna(value=0) # 去除 NAN 改成 0 方便判断
        self.code_data[cash_name]=self.code_data['%s_temp'%cash_name].apply(lambda x :self.fill_zero(x)) # 除零 填数
    
    def fill_zero(self,x):
         
            if x==0:
                
                return self.MCF_last 
            else:
                self.MCF_last =x
                return x
            
        
    def get_date_ts(self):#获取开始数据
        
        self.code_data=ts.get_k_data(self.code,self.startDate,end=self.endDate)
        self.code_data=self.code_data.reset_index()
        self.code_data=self.code_data.sort_index(ascending=True)# 从后倒序
        self.code_data.date=self.code_data.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
        self.code_data=self.code_data.set_index('date')
        if self.endDate == '%s'%self.today:
            todat_realtime=ts.get_realtime_quotes(self.code)
            realtime_price=float(todat_realtime.price)
            realtime_high=float(todat_realtime.high)
            realtime_low=float(todat_realtime.low)
            realtime_open=float(todat_realtime.open)
            realtime_volume=float(todat_realtime.volume)
            
            self.code_data.loc['%s'%self.today,'code']='%s'%self.code
            self.code_data.loc['%s'%self.today,'volume']='%s'%realtime_volume
            self.code_data.loc['%s'%self.today,'open']='%s'%realtime_open
            self.code_data.loc['%s'%self.today,'high']='%s'%realtime_high
            self.code_data.loc['%s'%self.today,'low']='%s'%realtime_low
            self.code_data.loc['%s'%self.today,'close']=realtime_price
class My_CF_plot(QtGui.QWindow):
    def __init__(self,):
        super(My_CF_plot,self).__init__()
        self.win = pg.GraphicsWindow(title="现金流")
        #self.win.resize(1000,600)
        self.win.setWindowTitle('现金流: Plotting')
        self.data=Cash_flow()
        pg.setConfigOptions(antialias=True)
    #设置
    def setCodeDate(self,**kwds):
        for kwd,value in kwds.items():
          
            if kwd in ('Code', 'start', 'end'):
                if not isinstance(value, str):
                    raise ValueError("Argument '%s' must be int" % kwd)
            
            if kwd == 'code':
                    self.data.code = value
            if kwd == 'start':
                    self.data.startDate = value            
            if kwd == 'end':
                    self.data.endDate = value
        self.data.get_date_ts() 
        self.data.get_cf_data(11)
        self.data.get_cf_data(24)
        self.data.get_cf_data(37)

    def Kline_plotting(self):
        
        #numd=self.data.df.reset_index()
        self.numd=self.data.code_data.reset_index()
        x=self.numd.date.apply(lambda x:datetime.datetime.strftime(x,"%Y-%m-%d"))
        self.xdict=dict(x) #转换成字符串字典
        # LABEL 10个图标
        self.maxRegion=len(self.numd.index)
        t=len(self.numd.index)//5
        #提取坐标点
        axis_date = [(i,list(x)[i]) for i in range(0,len(self.numd.index),t)]
 
        #stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis = pg.AxisItem(orientation='bottom') #设置横轴
        stringaxis.setTicks([axis_date, self.xdict.items()])
        stringaxis.setGrid(255)
        stringaxis.setLabel( text='Dates' )
        #stringaxis.setTickSpacing(100,1)
        self.k_plot = self.win.addPlot(row=1,col=0,title="kline",axisItems={'bottom': stringaxis})
        
        self.y=self.numd.close
        self.k_plot.plot(x=list( self.xdict.keys()), y=self.y.values,pen=(0,255,255))
        
        self.k_plot.showGrid(x=True, y=True)
        self.region = pg.LinearRegionItem()
        self.region.setZValue(self.maxRegion/4*3)
        self.region.setRegion([self.maxRegion/4*3, self.maxRegion])
        self.k_plot.addItem(self.region , ignoreBounds=True)
    def ThreePlot(self):
        mg=self.data.code_data.management_cf
        mg=mg.reset_index()
        iv=self.data.code_data.investment_cf
        fn=self.data.code_data.financing_cf
        print(mg,iv,fn)
        bg1 = pg.BarGraphItem(x=mg.index, height=mg.management_cf, width=0.3, brush='r')
        self.win.addItem(bg1)
        
         
         

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    p_=My_CF_plot()
    p_.setCodeDate(code='600362',start='2017-01-01',end='2018-01-09')
    #p_.Kline_plotting()
    p_.ThreePlot()

    #p_.remove_plot()
    #p_.RSI_plotting()
    p_.win.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.exec_()
    
            
'''
    code="600362" 
    startDate='2012-12-20'
    endDate='2017-12-22' 
    x=Cash_flow(code,startDate,endDate)
    x.get_cf_data(11)
    x.get_cf_data(24)
    x.get_cf_data(37)
    ax1=plt.subplot(111)
          
    plt.plot(x.code_data.index,x.code_data.close,"g")
    
    x2=ax1.twinx()#设立爽坐标
    plt.plot(x.code_data.index,x.code_data.management_cf,'r',label=u'经营活动')
    plt.plot(x.code_data.index,x.code_data.investment_cf,'b',label=u'投资活动')
    plt.plot(x.code_data.index,x.code_data.financing_cf,'y',label=u'融资活动')
    plt.legend(loc='best')
    plt.show()
'''    
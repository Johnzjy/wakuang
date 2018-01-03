# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 09:47:46 2017

@author: 310128142
"""


import talib
import tushare as ts
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import datetime
import time
import numpy as np
import sys

class My_index(object):
    def __init__(self,figSN=1):
        
        self.today=datetime.date.today()
        self.code="sh" 
        self.startDate='2016-12-31'
        self.endDate='2017-11-28'       
        self.MACD_fastperiod=10 #MACD快速参数
        self.MACD_slowperiod=20#MACD慢速参数
        self.MACD_signalperiod=9#MACD 权重
        self.fig=figSN  # this is show which figure 
        self.SN_plt=0  # show how many 
        self.df=pd.DataFrame(self.get_date_ts())
        
    def get_date_ts(self):#获取开始数据
        
        self.code_data=ts.get_k_data(self.code,self.startDate,end=self.endDate)

        self.code_data=self.code_data.sort_index(ascending=True)# 从后倒序
    
        self.code_data.date=self.code_data.date.apply(lambda x:datetime.datetime.strptime(x,"%Y-%m-%d"))
        #self.code_data.date=self.code_data.date.apply(lambda x:matplotlib.dates.date2num(x))
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
        return self.code_data
    '''
    def plot_init(self):
        self.SN_plt=self.SN_plt+1
        print(self.SN_plt)
        #plt.figure(self.SN_plt)
        fig, ax = plt.subplots(self.SN_plt)
        plt.subplots_adjust(left=0.25, bottom=0.27)
        plt.legend(loc='best')#输出标签，保持在最优模式
        plt.grid(True)
        return fig,ax
    
    def polt_end(self):
        axcolor = 'lightgoldenrodyellow'
        a0 = 5
        f0 = 3
        axfreq = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
        axamp = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        self.sfreq = Slider(axfreq, 'Freq', 0.1, 30.0, valinit=f0)
        self.samp = Slider(axamp, 'Amp', 0.1, 10.0, valinit=a0)
        self.sfreq.on_changed(self.update)
        self.samp.on_changed(self.update) 
        '''       

 
    def myMACD(self):
        price=self.df['close'].values
        ewma12 = pd.ewma(price,span=self.MACD_fastperiod)
        ewma60 = pd.ewma(price,span=self.MACD_slowperiod)
        dif = ewma12-ewma60
        dea = pd.ewma(dif,self.MACD_signalperiod)
        bar = (dif-dea) 
        #print(bar)#有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
        return dif,dea,bar
    def myMACD2(self):
        price=self.df['close'].values
        ewma12 = pd.Series(price).rolling(window=self.MACD_fastperiod).mean()
        ewma60 = pd.Series(price).rolling(window=self.MACD_slowperiod).mean()
        dif = ewma12-ewma60
        dea = pd.ewma(dif,self.MACD_signalperiod)
        bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
      
        return dif,dea,bar
    
    def draw_macd(self):
        ax1=self.plot_init()       
    #macd, signal, hist = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        macd, signal, hist = self.myMACD()
        #ax1=plt.subplot(111)
    
    
        plt.plot(self.df.index,self.df.close,"y")
        #plt.ylim(df.close.min()-3, df.close.max()+1)
        
        ax2=ax1.twinx()
        plt.plot(self.df.index,macd,'r',label='macd dif')   
        plt.plot(self.df.index,signal,'b',label='signal dea')
        #plt.bar(df.index,hist,'g',label='hist bar')
        #plt.plot(self.code_data.index,0*df.open,'--')
       # plt.ylim(-1, 3)

        
    def draw_macd2(self):
        ax1=self.plot_init()  
    #macd, signal, hist = talib.MACD(df['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)

        macd, signal, hist = self.myMACD2()
        #ax1=plt.subplot(111)
    
    
        plt.plot(self.df.index,self.df.close,"y")
        #plt.ylim(df.close.min()-3, df.close.max()+1)
        
        ax2=ax1.twinx()
        plt.plot(self.df.index,macd,'r',label='macd dif')   
        plt.plot(self.df.index,signal,'b',label='signal dea')
        #plt.bar(df.index,hist,'g',label='hist bar')
        #plt.plot(self.code_data.index,0*df.open,'--')
       # plt.ylim(-1, 3)

    def ST_bands (self):
        '''
        upperband   , 上轨  均线加一倍标准差
        middleband  ，中轨  均线
        lowerband   ，下轨  均线减一倍标准差
    
        '''
        upperband, middleband, lowerband = talib.BBANDS(self.df.close.values, timeperiod=10, nbdevup=2, nbdevdn=2, matype=0)
    
        self.df['upperband']=upperband
        self.df['middleband']=middleband
        self.df['lowerband']=lowerband
        return self.df
        #print(df)
        
    
    def draw_bands(self):
        self.ST_bands()#运行bans 数据
        plt.plot(self.df.index,self.df.close,'b')
        plt.plot(self.df.index,self.df.upperband,'r')
        plt.plot(self.df.index,self.df.middleband,'k')
        plt.plot(self.df.index,self.df.lowerband,'r')
        plt.legend(loc='best')
        plt.grid(True)
    '''
    RSI强弱指标
    
    '''
        
    def RSI(self,timeperiod=10):# price 加权平均指标    
        #timeperiod=1
        if self.code == 'sh':
            timeperiod=10
    
        self.df['RSI']=talib.RSI(self.df.close.values,timeperiod)#调用RSI函数计算RSI  因子设为10
        
    
    
    def draw_RSI(self): # 画加权平均指数
        self.RSI(self)
        fig,ax1=self.plot_init()  

        
        plt.plot(self.df.index,self.df.close,"k")
        #plt.ylim(df.close.min()-3, df.close.max()+1)
        ax2=ax1.twinx()
        
        plt.plot(self.df.index,self.df.RSI,'-',c='y',label='RSI')    
    
    
        plt.plot(self.df.index,0*self.df.open+20,'--')
        plt.plot(self.df.index,0*self.df.open+50,'--')
        plt.plot(self.df.index,0*self.df.open+80,'--')
       # plt.ylim(-1, 3)
        self.polt_end(fig,)

    '''
    def VWAP(self):# price 加权平均指标
        SQ={'slower_line':24,'middler_line':6,'fast_line':2}
        if self.code == 'sh':
            SQ['slower_line']=12
        else:
            pass
        self.code_data['pvc']=self.df.close[0:-2] * self.df.volume[0:-2]

        for name in SQ:
            values=SQ['%s'%name]
            #print(values)
            cnt = 0
            for i in df.index[values-1:]:
                pv_sum=self.code_data[cnt:cnt+values].pvc.sum()
                vlo_sum=self.code_data[cnt:cnt+values].volume.sum()
                self.code_data.loc[i,'%s'%name]=pv_sum/vlo_sum
                
                #cnt= cnt+1
    
    def draw_VWAP(df): # 画加权平均指数
          
        plt.plot(df.index,df.close,'R',linewidth=2.0)
        plt.plot(df.index,df.slower_line,'B')
        plt.plot(df.index,df.middler_line,'orange')
        plt.plot(df.index,df.fast_line,'g')
        plt.legend(loc='best')
        plt.grid(True) 
    '''
    
class My_plot(pg.GraphItem):
    def __init__(self,parent=None):
        super(My_plot,self).__init__()
        self.win = pg.GraphicsWindow(title="技术指标")
        self.win.resize(1000,600)
        self.win.setWindowTitle('技术指标: Plotting')
        self.data=My_index()
        pg.setConfigOptions(antialias=True)
    def macd_plotting(self):
        macd, signal, hist = self.data.myMACD()
        
        #numd=self.data.df.reset_index()
        numd=self.data.df.reset_index()
        x=numd.date.apply(lambda x:datetime.datetime.strftime(x,"%Y-%m-%d"))
        xdict=dict(x) #转换成字符串字典

        #stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis = pg.AxisItem(orientation='bottom') #设置横轴
        stringaxis.setTicks([xdict.items()])
        stringaxis.setGrid(255)
        stringaxis.setLabel( text='Dates' )
        stringaxis.setTickSpacing(100,1)
        self.macd_plot = self.win.addPlot(row=1,col=0,title="kline",axisItems={'bottom': stringaxis})
        
        self.y=numd.close
        self.macd_plot.plot(list(xdict.keys()), self.y)
        
        self.macd_plot.showGrid(x=True, y=True)
        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        self.region.setRegion([10, 200])
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this 
        # item when doing auto-range calculations.
        self.macd_plot.addItem(self.region , ignoreBounds=True)
 
    def update_plotting(self):  
        self.update_plot = self.win.addPlot(row=2,col=0,title="Multiple curves")
        self.update_plot.setAutoVisible(y=True)
        self.update_plot.plot(x=self.y.index,y=self.y.values)
        self.region.sigRegionChanged.connect(self.update)
        self.update_plot.sigRangeChanged.connect(self.updateRegion)
        print('1')
        self.region.setRegion([100, 200])
        #self.RSI_plot.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
        #self.RSI_plot.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Green curve")
        #self.RSI_plot.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="Blue curve")
        #cross hair
        
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.update_plot.addItem(self.vLine, ignoreBounds=True)
        self.update_plot.addItem(self.hLine, ignoreBounds=True)
        self.vb = self.update_plot.vb
        self.proxy = pg.SignalProxy(self.update_plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
    def mouseMoved(self,evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.update_plot.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x())
            if index > 0 and index < len(self.y.values):
                label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

               


   # def update(self):
    #    self.update_plot.setXRange(self.region.getRegion(), padding=0)
    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.update_plot.setXRange(minX, maxX, padding=0)   

    def updateRegion(self):
        self.region.setRegion(self.update_plot.getViewBox().viewRange()[0])
    
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    p_=My_plot()
    p_.macd_plotting()
    p_.update_plotting()

    #p_.RSI_plotting()
    app.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.exec_()
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib as mpl
import matplotlib.ticker as mtick
import matplotlib.animation as animation
import tushare as ts
import pandas as pd
import datetime
code ='600871' 
    
class real_datas(object):
        
    def __init__(self,ax,code):
        #mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
        self.code=code
        self.data_int=ts.get_realtime_quotes(code)
        self.line, = ax.plot([], [], lw=2)
        self.mark, = ax.plot([], [], lw=2,marker='h', markeredgecolor='r')#设置箭头
        self.high_plot, = ax.plot([], [],ls=':',color ='r' ,lw=2,label='high')#设置上限
        self.low_plot, = ax.plot([], [],ls=':',color ='r' ,lw=2,label='high')#设置上限
        #self.high,=ax.plot([], [], lw=2)
        self.ax=ax
        self.mid_price=float(self.data_int.pre_close[0])
        self.ax.set_xlim(0, 20)
        self.ax.set_ylim(self.mid_price*0.9, self.mid_price*1.1)
        self.xdata, self.ydata = [], []
        self.mk_xdata,self.mk_ydata=[],[]
        self.ax2=self.ax.twinx()#建立第二ya ax
        fmt='%.1f\%'
        yticks = mtick.FormatStrFormatter(fmt)
        self.ax2.set_ylim(-10,10) #设置第二轴百分比
        self.ax.set_title("%s"%code)#设置title
        del self.xdata[:]
        del self.ydata[:]
        self.ax.grid()
        self.ax.set_aspect('auto', 'datalim')
        self.time_template = '%s\nchanged = %.3f'
        self.time_text = self.ax.text(0.01, 1.05, '', transform=self.ax.transAxes)
        print('init done')

    def init(self):#初始化
        self.line.set_data(self.xdata,self.ydata)
        self.mark.set_data(self.xdata,self.ydata)
        self.high_plot.set_data(self.xdata,self.ydata)
        self.low_plot.set_data(self.xdata,self.ydata)
        self.ax.add_line(self.line)
        self.ax.add_line(self.mark)
        

        print(float(self.data_int.high[0]))
       # self.high.set_data([self.xdata,float(self.data_int.high[0])])
        print ('will begin')
        return self.line,
    def data_gen(self,t=0):
        cnt = 0
     
    
        while 1:
       
            datas=ts.get_realtime_quotes(self.code)
            cnt += 1
            t +=1 
            price=float(datas.price[0])
            pre_close_=float(datas.pre_close[0])
            prechange=(price-pre_close_)/pre_close_*100
            yield t, price,prechange

    def run(self,data):
        # update the data
        t, y ,b= data
        self.xdata.append(t)
        time_now=datetime.datetime.now() 
        time_now=time_now.strftime('%b-%d %H:%M:%S %a')
        #print (time_now)
        self.ydata.append(y)
        xmin, xmax = self.ax.get_xlim()
        print('>',end='')
    
        if t >= xmax:
            self.ax.set_xlim(xmin, xmax*1.2)
            self.ax.figure.canvas.draw()
        turn=t//10 + 2
        self.mark.set_data(self.xdata[-1],self.ydata[-1])
        self.line.set_data(self.xdata,self.ydata)
        self.high_plot.set_data(self.xdata[-turn:],float(self.data_int.high[0]))
        self.low_plot.set_data(self.xdata[-turn:],float(self.data_int.low[0]))

        self.time_text.set_text(self.time_template % (time_now,b))
    
        #bar.set_data(b,v,0.1)
        return self.line,self.time_text
fig1, ax1 = plt.subplots()

x=real_datas(ax1,'sh')

ani = animation.FuncAnimation(fig1, x.run, x.data_gen, blit=False, interval=1000,
                                  repeat=False, init_func=x.init)

plt.show()
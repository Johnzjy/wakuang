# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:32:54 2017

@author: 310128142
"""

import tushare as ts

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mc

'''
0：name，股票名字
1：open，今日开盘价
2：pre_close，昨日收盘价
3：price，当前价格
4：high，今日最高价
5：low，今日最低价
6：bid，竞买价，即“买一”报价
7：ask，竞卖价，即“卖一”报价
8：volume，成交量 maybe you need do volume/100
9：amount，成交金额（元 CNY）
10：b1_v，委买一（笔数 bid volume）
11：b1_p，委买一（价格 bid price）
12：b2_v，“买二”
13：b2_p，“买二”
14：b3_v，“买三”
15：b3_p，“买三”
16：b4_v，“买四”
17：b4_p，“买四”
18：b5_v，“买五”
19：b5_p，“买五”
20：a1_v，委卖一（笔数 ask volume）
21：a1_p，委卖一（价格 ask price）
...
30：date，日期；
31：time，时间；
'''
class real_datas:
    CODECNT =0
    FIG = 0
  #  fig, ax = plt.subplots()
  #  ax.set_ylim(0, 6)
  #  ax.set_xlim(-10, 10)
    def __init__(self,code):
        self.code =code
    #    self.note=note
        self.date=      ts.get_realtime_quotes(code)
        self.name=      self.date.name[0]
        self.open=      self.date.open[0]
        self.price=     float(self.date.price[0])
        self.bid=       float(self.date.bid[0])
        self.volume=    float(self.date.volume[0])
        self.amount=    float(self.date.amount[0])
        self.ask=       float(self.date.ask[0])
        self.pre_close=     float(self.date.pre_close[0])                    
        self.change=(self.price - float(self.pre_close)) / self.pre_close
        self.color= 'read' if self.change > 0.0 else 'green'
        self.buy=       int(self.date.b1_v[0]) + int(self.date.b2_v[0]) + int(self.date.b3_v[0]) + int(self.date.b4_v[0]) +int(self.date.b5_v[0])
        self.sell=      int(self.date.a1_v[0]) + int(self.date.a2_v[0]) + int(self.date.a3_v[0]) + int(self.date.a4_v[0]) +int(self.date.a5_v[0])
        self.BID_ASD=   self.buy+self.sell
        self.__class__.CODECNT +=1
        
     
    def draw_color(self):
        fig_number =self.__class__.CODECNT
        sub_number =self.__class__.FIG
        ax1=self.ax.set_ylim(0, fig_number)
        buy_len=self.buy / self.BID_ASD *20
        
        change_100=self.change * 100
        
        sell_len=20- buy_len 
        
#Draw broken barh         
        ax1.broken_barh([(-10, buy_len), (buy_len - 10,sell_len)], (sub_number*1, 0.1),
                         cmap=plt.cm.hot,
                         facecolors=(mc.cnames['tomato'],mc.cnames['skyblue'])#'#00FF00'),#  orangered 柠檬

                         )
#Draw changed
        if change_100 >=0:
            ax1.broken_barh([(0,change_100)], (sub_number*1 +0.1, 0.9),facecolors=('red'))
        else:
            
            ax1.broken_barh([(change_100, 0 - change_100)], (sub_number*1 +0.1, 0.9),facecolors=('lime'))# 黄绿色
        
        plt.scatter(-5, 1, s=1000, c=mc.cnames['skyblue'],alpha=0.5)
        self.__class__.FIG +=1
x=real_datas('600362')

#df[['code','name','price','bid','ask','volume','amount','time']]
#x=real_datas('600362')
#y=real_datas('600781')
#z=real_datas('600361')
#x.draw_color()
#print(x.FIG)
#y.draw_color()
#print(x.FIG)
#z.draw_color()
#print(x.FIG)
#plt.show()

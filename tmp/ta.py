# In[2]:

import matplotlib.pyplot as plt
# 引入相依套件
import numpy as np
import pandas as pd
from numpy import random

# 引入檔案
# 資料來源 3008 大立光 2012-8/1 ~ 2014-12/09
# http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report201412/201412_F3_1_8_3008.php?STK_NO=3008&myear=2014&mmon=12
datapath = '/Users/wy/Desktop/3008.txt'
data = pd.read_csv(datapath)

# In[3]:

# 看檔案前N筆
data.head(5)

# In[4]:

# data詳細資料 總數,平均數,標準差...
data.describe()

# In[5]:

# 技術分析資料來源
# http://hymar.myweb.hinet.net/study/stock/theory/

# In[6]:


# Rise Ratio 漲幅比
def RR(data):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止 第一筆data沒有更舊的
        if item - 1 >= 0:
            # (今日收盤價 - 昨日收盤價)/昨日收盤價
            tmp = (data['Close'][item - 1] - data['Close'][item]
                   ) / data['Close'][item] * 100
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  RR 欄位
    data['RR'] = tmpSeries


# In[7]:


# 威廉指標(WMS%R或%R)
def WMS(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day + 1 >= 0:
            # 9日WMS%R =(9日內最高價-第9日收盤價) / (9日內最高價-9日內最低價)*100
            # [item-day+1:item+1] 今日區間 [item-day+1] 第N日 583-9=574+1=575
            tmp = (data['High'][item - day + 1:item + 1].max() -
                   data['Close'][item - day + 1]) / (
                       data['High'][item - day + 1:item + 1].max() -
                       data['Low'][item - day + 1:item + 1].min()) * 100
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  WMS 欄位
    data['WMS'] = tmpSeries


# In[8]:


# 買賣意願指標 day 建議26
def BR(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day >= 0:
            # 26日BR = (今日最高價 - 昨日收盤價)26天累計總數 / (昨日收盤價 - 今日最低價)26天累計總數
            # [(item-day+1)-1:(item+1)-1] 有-1 今日區間 [(item-day+1):(item+1)] 昨日區間
            tmp = (data['High'][(item - day + 1) - 1:(item + 1) - 1].sum() -
                   data['Close'][item - day + 1:item + 1].sum()) / (
                       data['Close'][item - day + 1:item + 1].sum() -
                       data['Low'][(item - day + 1) - 1:(item + 1) - 1].sum())
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  BR 欄位
    data['BR'] = tmpSeries


# In[9]:


# 買賣氣勢指標 day建議26
def AR(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day + 1 >= 0:
            # 26日AR = (最高價 - 開盤價)26天累計總數 / (開盤價 - 最低價)26天累計總數
            # [item-day+1:item+1] 今日區間
            tmp = (data['High'][item - day + 1:item + 1].sum() -
                   data['Open'][item - day + 1:item + 1].sum()) / (
                       data['Open'][item - day + 1:item + 1].sum() -
                       data['Low'][item - day + 1:item + 1].sum())
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  AR 欄位
    data['AR'] = tmpSeries


# In[10]:


# 平均成交量 mean volumn day建議12
def MV(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day + 1 >= 0:
            # N日平均量 = N日內的成交量總和 / N
            # [item-day+1:item+1] 今日區間
            tmp = data['Volume'][item - day + 1:item + 1].mean()
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  MV 欄位
    data['MV'] = tmpSeries


# In[11]:


# 移動平均線(MA，Moving Average) 建議12
def MA(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day + 1 >= 0:
            # 移動平均數 = 採樣天數的股價合計 / 採樣天數
            # [item-day+1:item+1] 今日區間
            tmp = data['Close'][item - day + 1:item + 1].mean()
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  MA 欄位
    data['MA' + str(day)] = tmpSeries


# In[12]:


# 心理線(PSY) 建議13
def PSY(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day >= 0:
            # 13日PSY值 = ( 13日內之上漲天數 / 13 ) * 100
            # [item-day+1-1:item+1-1] 跳一天 最早的天沒有RR值
            count = 0
            for a in data['RR'][item - day + 1 - 1:item + 1 - 1]:
                if a > 0:
                    count += 1
            tmp = float(count) / float(13) * 100
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  PSY 欄位
    data['PSY'] = tmpSeries


# In[13]:


# 能量潮(OBV) 建議12
def OBV(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day >= 0:
            # 今日OBV值 = 最近12天股價上漲日成交量總和 - 最近12天股價下跌日成交量總和
            # 先由 ['RR'] 求出boolean值 > 0 True 套入['Volume']符合True全加起來
            bolRise = data['RR'][item - day + 1 - 1:item + 1 - 1] > 0
            sumVolRise = data['Volume'][item - day + 1 - 1:item + 1 - 1][
                bolRise].sum()
            bolDesc = data['RR'][item - day + 1 - 1:item + 1 - 1] < 0
            sumVolDesc = data['Volume'][item - day + 1 - 1:item + 1 - 1][
                bolDesc].sum()

            tmp = sumVolRise - sumVolDesc
            #             可切換 OBV累積12日移動平均值 = (最近12天股價上漲日成交量總和 - 最近12天股價下跌日成交量總和) / 12
            #             tmp = (sumVolRise-sumVolDesc)/12
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  OBV 欄位
    data['OBV'] = tmpSeries


# In[14]:


# 數量指標(VR) 建議12
def VR(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day >= 0:
            # VR = ( N日內上漲日成交值總和 + 1/2*N日內平盤日成交值總和) / ( N日內下跌日成交值總和 + 1/2*N日內平盤日成交值總和)* 100％
            # 先由 ['RR'] 求出boolean值 > 0 True 套入['Volume']符合True全加起來
            bolRise = data['RR'][item - day + 1 - 1:item + 1 - 1] > 0
            sumVolRise = data['Volume'][item - day + 1 - 1:item + 1 - 1][
                bolRise].sum()

            bolNorm = data['RR'][item - day + 1 - 1:item + 1 - 1] == 0
            sumVolNorm = data['Volume'][item - day + 1 - 1:item + 1 - 1][
                bolNorm].sum()

            bolDesc = data['RR'][item - day + 1 - 1:item + 1 - 1] < 0
            sumVolDesc = data['Volume'][item - day + 1 - 1:item + 1 - 1][
                bolDesc].sum()

            tmp = (sumVolRise + 0.5 * sumVolNorm) / (
                sumVolDesc + 0.5 * sumVolNorm) * 100
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  VR 欄位
    data['VR'] = tmpSeries


# In[15]:


# 相對強弱指標(RSI) 建議6
def RSI(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day >= 0:
            # 6日RSI=100*6日內收盤上漲總幅度平均值 / (6日內收盤上漲總幅度平均值 - 6日內收盤下跌總幅度平均值)
            # 先由 ['RR'] 求出boolean值 > 0 True 套入['Volume']符合True全加起來
            bolRise = data['RR'][item - day + 1 - 1:item + 1 - 1] > 0
            meanRise = data['RR'][item - day + 1 - 1:item + 1 - 1][
                bolRise].mean()
            bolDesc = data['RR'][item - day + 1 - 1:item + 1 - 1] < 0
            meanDesc = data['RR'][item - day + 1 - 1:item + 1 - 1][
                bolDesc].mean()

            tmp = 100 * meanRise / (meanRise - meanDesc)
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  RSI 欄位
    data['RSI'] = tmpSeries


# In[16]:


# 乖離率(BIAS)
def BIAS(data, day):
    # 由於 data 新到舊 0~xxx，遞增，因此需反轉陣列
    dataList = range(data['Date'].size)
    dataList.reverse()
    tmpList = []

    for item in dataList:
        # 防止前day沒有data
        if item - day + 1 >= 0:
            # N日乖離率 = (當日股價 - N日股價移動平均數) / N日平均股價
            tmp = (data['Close'][item - day + 1] -
                   data['MA' + str(day)][item - day + 1]
                   ) / data['MA' + str(day)][item - day + 1] * 100
            tmpList.append(tmp)

    # 前day 沒data會出現NA
    tmpList.reverse()
    tmpSeries = pd.Series(tmpList)

    # create  BIAS 欄位
    data['BIAS'] = tmpSeries

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:01:47 2018

@author: 310128142
"""
from pyecharts import Pie, Timeline, Grid, TreeMap
import tushare as ts
import datetime, os
import numpy as np
import pandas as pd

x = ts.get_stock_basics()
df = ts.fund_holdings('2017', '4')
print(df)
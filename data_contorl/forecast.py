# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:38:02 2017

@author: 310128142
"""

import tushare as ts

x=ts.forecast_data(2017,2)
profit=x[x['type']=="预增"] 
profit=profit.sort_values('report_date',ascending=False)

print (profit)
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:28:54 2018

@author: 310128142
"""
from pyecharts import Pie,Timeline,Grid,TreeMap
import tushare as ts
import datetime,os
import numpy as np
import pandas as pd

def Top10Holder(codenumber,startdate='2014-10-10'):
    if len(codenumber) !=6:
        return False
    elif len(codenumber) == 6:
        datestr = startdate.split("-")
        thisyear = datestr[0]
    
        df2 = ts.top10_holders(code=codenumber, gdtype="1")
    
        test = df2[1]["quarter"].tolist()
    
        df_ready = df2[1]
        idxlist = []
        for idx, val in enumerate(test):
            a = val.split("-")
            if a[0] == thisyear:
                # print a[0],idx
                idxlist.append(idx)
            elif a[0]> thisyear:
                idxlist.append(idx)
        thing = df_ready.loc[idxlist]
        thing =pd.DataFrame(thing)
    
        thing = thing.sort_values(["quarter", "name"])
        quarterlist=thing.quarter.value_counts()
        quarterlist=quarterlist.index.sort_values()
        pietimeline = Timeline(height=600,
                               width =1000,
                               timeline_left=20,
                               timeline_right=100,
                               is_auto_play=False,
                               timeline_bottom=0,
                               timeline_symbol='diamond',
                               )
        
        for quarters in list(quarterlist):
            df=thing[thing["quarter"]==quarters]
            df.h_pro=df.h_pro.apply(lambda x : float(x))
            df.hold=df.hold.apply(lambda x : float(x))
            sum_pro=round(df.h_pro.sum(),2)
            sum_hold=round(np.mean(df.hold/df.h_pro)*sum_pro,0)
         
    
            s = pd.Series({'name':'其他', 'h_pro': 100-sum_pro,'hold':sum_hold})
            df=df.append(s,ignore_index=True)
            #df=df.sort_values(["name"])
     
        
         
            pie=Pie('%s'%quarters+"-"+"top10holder",title_pos='outside')
            TopPie=pie.add('', 
                        df.name, df.hold, radius=[20, 45], 
                        center=[45,50],
                        is_legend_show=True,
                        is_label_show=True,
                       # is_visualmap=True,
                        is_more_utils=True,
                        is_toolbox_show=True,
                        legend_pos='left',
                        legend_orient='vertical',
                        legend_top=25,
                        legend_text_size=12,
                        label_text_size=10,
                        
                        label_formatter = "{b}:\n {c}万股\n{d}%")
          
    

            #gird= Grid()
            #gird.add(pie,grid_bottom="20%")
            #gird.add(tab,grid_bottom="60%")
            pietimeline.add(pie, quarters,)
            #pietimeline.top('40%')
        print('time line done')

        return pietimeline
if __name__=="__main__":
    print(os.getcwd())
    try:
        os.remove(os.getcwd()+'/top10.html')
    except:
        pass
    x=Top10Holder('600111')
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "top10.html")) 

        #pietimeline.show_config()
    x.render(path=file_path)

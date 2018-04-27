# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 10:28:54 2018

@author: 310128142
"""
from pyecharts import Pie,Timeline,Grid,TreeMap
import pyecharts
import tushare as ts
import datetime,os
import numpy as np
import pandas as pd
#TODO: 需要增加code title and 同期大股东进出原因
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
    
        thing = thing.sort_values(["quarter", "name"])#排序所有流通股股东
 
        quarterlist=thing.quarter.value_counts()
        quarterlist=quarterlist.index.sort_values()
        timeline = Timeline(height=600,
                               width =800,
                               timeline_left=20,
                               timeline_right=100,
                               is_auto_play=False,
                               timeline_bottom=0,
                               timeline_symbol='diamond',
                               )
        year_index=thing.quarter.apply(lambda x: x[0:4])
        yearlist=year_index.value_counts()
        yearlist= yearlist.index.sort_values()


        #print(quarterlist,year)
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
            TopPie =pie.add('', 
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
                        label_text_color="#100",
                        tooltip_text_color="#F0F",
                        #is_label_emphasis=False,#是否显示高亮
                        
                        label_formatter = "{b}:\n {c}万股\n{d}%")
          
    
            
            #gird= Grid()
            #gird.add(pie,grid_bottom="20%")
            #gird.add(tab,grid_bottom="60%")
            #pietimeline.add(pie, quarters,)
            timeline.add(pie,quarters,)
            #page = pyecharts.Page()
            #page.add(pie)
            #page.add(_treemap)
            #timeline.add(pie,quarters,)
            #timeline.add(_treemap,quarters,)

            #pietimeline.top('40%')
        trmtimeline = Timeline(height=1200,
                               width =800,
                               timeline_left=20,
                               timeline_right=100,
                               is_auto_play=False,
                               timeline_bottom=0,
                               timeline_symbol='diamond',
                               )
        #for y in list(yearlist):
            
        datas_index=[]
        for i, _year in enumerate(year_index):
            if _year in list(yearlist)[-1:]:
                datas_index.append(i)
            else:
                pass
        
        print (thing.loc[datas_index,:])
        collect_datas=thing.iloc[datas_index,:3]
        collect_datas.hold=collect_datas.hold.apply(lambda x : float(x))
        print(collect_datas)
        name=collect_datas['name']
        collect_datas.drop(labels=['name'], axis=1,inplace = True)
        collect_datas.insert(2, 'name', name)
        print(collect_datas.get_values())
        tr = pyecharts.ThemeRiver("TOP 10 hold 河流图 ",
                            height=800,
                            width =800,)
        tr.add(name.get_values(), collect_datas.get_values(), is_label_show=False)
        #trmtimeline.add(tr,"%s"%y,)
        page = pyecharts.Page()
        
       # page.add(trmtimeline)
        page.add(timeline)
        page.add(tr)
        '''
        them_dates=[]
        for i in thing.index:
            print (i)
            collect_datas=thing[thing.index==i].iloc[:, 0:3]
            name=collect_datas['name']
            collect_datas.drop(labels=['name'], axis=1,inplace = True)
            collect_datas.insert(2, 'name', name)
            print (collect_datas.get_values())
        '''

        print('time line done')

        return page
if __name__=="__main__":
    print(os.getcwd())
    try:
        os.remove(os.getcwd()+'/top10.html')
    except:
        pass
    x=Top10Holder('600200')
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "top10.html")) 

        #pietimeline.show_config()
    x.render(path=file_path)

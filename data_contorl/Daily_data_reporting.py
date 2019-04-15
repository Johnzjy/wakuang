import tushare as ts
import datetime
import os
import pandas as pd
from pandas import options
todaytime=datetime.date.today()
#todaytime= '2017-06-20'
print(todaytime)

'''
下载每天所有股票的数据，并存储
'''
def init_path(path_=None):#初始化当前路径
    if path_ is None:
        files_path = '../report/Brokerage'
    else:
        files_path =path_
    
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.makedirs(files_path)                # 创建目录
        
def download__today_alldata():
    ALL_datas=ts.get_today_all()# 读取去当天数据
    files_path= '../report/Daily_database'
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.makedirs(files_path)                # 创建目录
    ALL_datas.to_csv('../report/Daily_database/%s_full_stock_csv.csv'%todaytime,encoding='gbk') #存储到CSV
    #存储到xlsx文件中
    with pd.ExcelWriter('../report/Daily_database/%s_full_stock_xlx.xlsx'%todaytime) as writer:
        ALL_datas.to_excel(writer, sheet_name='Sheet1')
    print('today data base to save %s_database.csv'%todaytime)
'''
def get_5min_data(code):
    5mdata=ts.get_hist_data('%s'%code, ktype='5') 
    5m.to_csv('%s_%sdatabase.csv'%(code,todaytime))
    print('5min data base to save %s_database.csv'%code)

'''
'''
下载规定日期的交易笔数
'''
def download_datas_ST1D(code,time):
    ALL_datas=ts.get_tick_data(code,date=time)
    files_path = '../report/Daily_database/%s/funding'%code
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.makedirs(files_path)                # 创建目录
    ALL_datas.to_csv(files_path+'/%s_sum_amount_csv.csv'%(time),encoding='gbk')
    with pd.ExcelWriter(files_path+'/%s_sum_amount_xlx.xlsx'%(time)) as writer:
        ALL_datas.to_excel(writer, sheet_name='Sheet1')
    print('%s data base to save >>> '%time+files_path)
    return ALL_datas

def download_Large_amount(time,code,vols):

    data_L=ts.get_sina_dd(code , date=time ,vol=vols)
    files_path = '../report/Daily_database/big_amu'+code
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.makedirs(files_path)                # 创建目录5
    data_L.to_csv(files_path+'/%s_LGamount%s_csv.csv'%(time,vols),encoding='gbk')
    with pd.ExcelWriter(files_path+'/%s_LGamount%s_xlx.xlsx'%(time,vols)) as writer:
        data_L.to_excel(writer, sheet_name='Sheet1')
    print('\n%s 大单 have been saved'%time)

def download_brokerage(time ):
    list=[5,10,30]
    for i in list:
        try:
            Datas_b=ts.broker_tops(days= i)
        except:
            continue
        files_path = '../report/Brokerage/%s'%time
        
        if os.path.exists(files_path) == False: # 判断文件是不是存在
            os.makedirs(files_path)                # 创建目录
            print(files_path)
        if Datas_b is None: #data cant download from WEB
            continue
        else:
            pass
        Datas_b.to_csv(files_path+'/%s_Brokerage%sD_csv.csv'%(time,i),encoding='gbk')
        with pd.ExcelWriter(files_path+'/%s_Brokerage%sD_xlx.xlsx'%(time,i)) as writer:
            Datas_b.to_excel(writer, sheet_name='Sheet1')
        print('\n%s %s营业厅数据 have been saved'%(time,i))

def download_org_top(time ): 
    list=[5,10,30]
    for i in list:
        Datas_b=  ts.inst_tops(days= i)
        files_path = '../report/Brokerage/%s'%time
        if os.path.exists(files_path) == False: # 判断文件是不是存在
            os.makedirs(files_path)                # 创建目录
        if Datas_b is None: #data cant download from WEB
            continue
        else:
            pass
        Datas_b.to_csv(files_path+'/%s_org_top%sD_csv.csv'%(time,i),encoding='gbk')
        with pd.ExcelWriter(files_path+'/%s_org_top%sD_xlx.xlsx'%(time,i)) as writer:
            Datas_b.to_excel(writer, sheet_name='Sheet1')
        print('\n%s %s机构席位 have been saved'%(time,i))
        
'''
获取最近一个交易日机构席位成交明细统计数据
'''       
def download_Orgday(time ):

    Datas_b=  ts.inst_detail()
    files_path = '../report/Brokerage/%s'%time
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.makedirs(files_path)                # 创建目录
    if Datas_b is None: #data cant download from WEB
        return None
    else:
        pass
    Datas_b.to_csv(files_path+'/%s_Orgday_csv.csv'%(time),encoding='gbk')
    with pd.ExcelWriter(files_path+'/%s_Orgday_xlx.xlsx'%(time)) as writer:
        Datas_b.to_excel(writer, sheet_name='Sheet1')
    print('\n%s机构席位一天 have been saved'%(time))
        
def download_top_list(time):

    Datas_b= ts.top_list(time)

    files_path = '../report/Brokerage/%s'%todaytime
    if os.path.exists(files_path) == False: # 判断文件是不是存在
        os.makedirs(files_path)                # 创建目录
    if Datas_b is None: #data cant download from WEB
         return None
    else:
        pass
    Datas_b.to_csv(files_path+'/%s_top_list_csv.csv'%(todaytime),encoding='gbk')
    with pd.ExcelWriter(files_path+'/%s_top_list_xlx.xlsx'%(todaytime)) as writer:
        Datas_b.to_excel(writer, sheet_name='Sheet1')
    print('\n%s龙虎have been saved'%(todaytime))


'''
下载一段时间内的数据

未使用
'''
def get_1by1_data(startime,endtime):
    dataform = pd.read_csv('../information_folder/sh_name_csv.csv',encoding='gbk') # 读取list文件
    list_st= dataform['code']   #读取列表
    for code_st in list_st:
        code_st = '%06d'%code_st
        datas=ts.get_hist_data(code_st,start='2016-07-01',end='2016-07-27')
        datas.to_csv('../all_data/%s_today_ticks.csv'%code_st)
        print(code_st)




if __name__ == "__main__":
    init_path()
    #for ladays in tims.Fworkday(2):

     #   download_datas_ST1D('600221',ladays)
    #todaytime=

    download_brokerage(todaytime)
    download_org_top(todaytime)
    download_Orgday(todaytime)
 
 #   download_top_list(None)
    #get_1by1_data(1,2)


import pyecharts
import pandas as pd
import get_date
import tushare as ts 
import calendar


def fund_holdings():
    Quar_list=get_date.get_quarter()
    df= ts.fund_holdings(2017,4)
    print(Quar_list)

#TODO : 这个函数存在问题
def get_quart_fund_hold(quart= None):
    if quart is None:
        quart ="2017-2"
    else:
        pass   
    try :
        df=pd.read_csv('../report/base_information/fund_hold_%s.csv'%quart,encoding='gbk')
    except:
        _quart=quart.split("-")
        df= ts.fund_holdings(2017,4)
        print(_quart)
        print(df)
        df=pd.DataFrame(df)

        df.to_csv('../report/base_information/fund_hold_%s.csv'%quart)

get_quart_fund_hold()
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 09:54:34 2017

@author: 310128142
fuction: 
    download imformation/下载基本信息
    download 
"""

import tushare as ts
import pandas as pd
import datetime
import sys
import os
from numpy import nan as NaN
sys.path.append("..")
from src import logd
import json
from src import code_list

today = datetime.date.today()

log_STI = logd.Logger('downloading_information.log')

log_STI.info('%s开始下载基本数据信息%s' % ('=' * 16, '=' * 16))
#todo:完成字典
information_dict = {
    "base": {
        "code": "代码",
        "name": "名称",
        "industry": "所属行业",
        "area": "地区",
        "pe": "市盈率",
        "outstanding": "流通股本(亿)",
        "totals": "总股本(亿)",
        "totalAssets": "总资产(万)",
        "liquidAssets": "流动资产",
        "fixedAssets": "固定资产",
        "reserved": "公积金",
        "reservedPerShare": "每股公积金",
        "esp": "每股收益",
        "bvps": "每股净资",
        "pb": "市净率",
        "timeToMarket": "上市日期",
        "undp": "未分利润",
        "perundp": "每股未分配",
        "rev": "收入同比(%)",
        "profit": "利润同比(%)",
        "gpr": "毛利率(%)",
        "npr": "净利润率(%)",
        "holders": "股东人数",
    },
    "predict": {
        "code": "代码",
        "name": "名称",
        "predict_eps": "每股收益",
        "predict_eps_yoy": "每股收益同比(%)",
        "predict_bvps": "每股净资产",
        "predict_roe": "净资产收益率(%)",
        "predict_epcf": "每股现金流量(元)",
        "predict_net_profits": "净利润(万元)",
        "predict_profits_yoy": "净利润同比(%)",
        "predict_distrib": "分配方案",
        "predict_report_date": "发布日期",
    },
    "cashflow": {
        "cf_sales": "经营现金净流量对销售收入比率",
        "rateofreturn": "资产的经营现金流量回报率",
        "cf_nm": "经营现金净流量与净利润的比率",
        "cf_liabilities": "经营现金净流量对负债比率",
        "cashflowratio": "现金流量比率",
    },
    "fund_hold": {
        "fund_nums": "基金家数",
        "fund_nlast": "与上期相比",  #（增加或减少了）
        "fund_shares": "基金持股数（万股）",
        "fund_clast": "与上期相比",
        "fund_amount": "基金持股市值",
        "fund_ratio": "占流通盘比率",
    },
}


def downloading_information(time=3, SAVE=True):
    """
    获取全STOCK 数据
    """
    year = 2018
    quarter = 1
    df = pd.read_csv("../list/stock_code_all.csv", encoding='gbk')
    rt_df = df
    df["code"] = df['code'].map(lambda x: str(x).zfill(6))

    ST_basics = ts.get_stock_basics()
    ST_basics = ST_basics.drop(["name"], axis=1)
    ST_basics = ST_basics.reset_index()
    df = pd.merge(df, ST_basics, how="left", on="code")

    print("\n\n process downloading the pre-announcement datas for %s -Q%s" %
          (year, quarter))
    pre_announcement = ts.get_report_data(year, quarter + 1)
    pre_announcement.columns = information_dict["predict"]
    pre_announcement = pre_announcement.drop(["name"], axis=1)
    df = pd.merge(df, pre_announcement, how="left", on="code")

    print("\n\n process downloading the profit datas           for %s -Q%s" %
          (year, quarter))
    profit_df = ts.get_profit_data(year, quarter)
    profit_df = profit_df.drop(["name"], axis=1)

    df = pd.merge(df, profit_df, how="left", on="code")

    print("\n\n process downloading the operation datas        for %s -Q%s" %
          (year, quarter))
    op_df = ts.get_operation_data(year, quarter)
    op_df = op_df.drop(["name"], axis=1)
    df = pd.merge(df, op_df, how="left", on="code")

    print("\n\n process downloading the growth datas           for %s -Q%s" %
          (year, quarter))
    growth_df = ts.get_growth_data(year, quarter)
    growth_df = growth_df.drop(["name"], axis=1)
    df = pd.merge(df, growth_df, how="left", on="code")

    print("\n\n process downloading the debt datas           for %s -Q%s" %
          (year, quarter))
    debt_df = ts.get_debtpaying_data(year, quarter)
    debt_df = debt_df.drop(["name"], axis=1)
    df = pd.merge(df, debt_df, how="left", on="code")

    print("\n\n process downloading the cashflow datas        for %s -Q%s" %
          (year, quarter))
    cashflow_df = ts.get_cashflow_data(year, quarter)
    cashflow_df = cashflow_df.drop(["name"], axis=1)
    df = pd.merge(df, cashflow_df, how="left", on="code")

    print("\n\n process downloading the funds holding  datas  for %s -Q%s" %
          (year, quarter))
    fund_df = ts.fund_holdings(year, quarter)
    fund_df = fund_df.drop(["name"], axis=1)
    fund_df = fund_df.drop(["date"], axis=1)
    fund_df.rename(
        columns={
            "num": "fund_nums",
            "nlast": "fund_nlast",
            "count": "fund_shares",
            "clast": "fund_clast",
            "amount": "fund_amount",
            "ratio": "fund_ratio",
        },
        inplace=True)
    df = pd.merge(df, fund_df, how="left", on="code")
    df = df.drop_duplicates("code", keep='first', inplace=False)
    df = df.set_index("code")

    #profit_df=profit_df.set_index("code")
    #df=pd.concat([df,profit_df],axis=1,join_axes=[df.index])
    #df.columns=df.columns +information_dict["predict"].keys[2:]

    #print (pre_announcement)
    '''
    for year in range(2015,2017):
        print(year)
        for Q in range(1,5):
            print(Q)
            ST_basics=download_ACH_Q(year,Q,ST_basics)
    '''
    if SAVE == True:

        path = os.path.dirname(os.getcwd()) + '\\report\\'  # 存储路径
        df.to_csv(path + 'Stock_Information.csv', encoding='gbk', header=True)

    return df
#TODO: 
def read_stock_inoformation_csv():
    path = os.path.dirname(os.getcwd())+ '\\report\\Stock_Information.csv'
    print (path)
    df= pd.read_csv(path, encoding='gbk')
    return df
    

def download_ACH_Q(year, quarter, df):  #按照季度获取信息
    Data = df
    try:

        achievement = ts.get_report_data(year, quarter)
        achievement = pd.DataFrame(achievement)
    except:
        pass
    achievement = achievement.set_index('code')
    achievement = achievement.sort_index()
    for title_name in achievement.columns:
        print(title_name)
        for code_ in achievement.index[1:]:
            if achievement.at['%s' % code_, '%s' % title_name] != NaN:

                try:
                    #print(achievement.at['%s'%code_,'%s'title_name])
                    Data.ix['%s' % code_,
                            '%s-%s-%s' % (
                                title_name, year,
                                quarter)] = achievement.at['%s' % code_,
                                                           '%s' % title_name]
                except:
                    buf = achievement.at['%s' % code_, '%s' % title_name]
                    Data.ix['%s' % code_,
                            '%s-%s-%s' % (title_name, year, quarter)] = buf[0]
            else:
                pass
                #print (code_,title_name)
        #print (achievement.head(9))
    return Data


def get_trade_date():  # 网上获得交易日期
    data = ts.trade_cal()
    open_day = data[data.isOpen > 0]
    open_day['Quarter'] = ''
    for i in open_day.index:
        DATE = open_day.at[i, 'calendarDate']

        month = DATE[5:7]
        if month >= '01' and month <= '03':
            Qua = DATE[2:4] + 'Q1'
        elif month >= '04' and month <= '06':
            Qua = DATE[2:4] + 'Q2'
        elif month >= '07' and month <= '09':
            Qua = DATE[2:4] + 'Q3'
        elif month >= '10' and month <= '12':
            Qua = DATE[2:4] + 'Q4'

        open_day.at[i, 'Quarter'] = Qua

        print(DATE, Qua)

    return open_day


def downloading_trade_date():  # 存储交易日期
    data = get_trade_date()
    data = data.set_index('calendarDate')
    import os
    path = os.path.dirname(os.getcwd()) + '\\report\\'  # 存储路径
    data.to_csv(path + 'Trade_Date.csv', encoding='gbk', header=True)


def trade_calendar(year=today.year):  #获取一年交易日期 默认为今年
    '''
    item  calendarDate  isOpen Quarter
    '''
    data = pd.read_csv("..\\report\\Trade_Date.csv", encoding='gbk')
    data = data[data['calendarDate'] >= "%s-01-01" % year]
    data = data[data['calendarDate'] <= "%s-12-31" % year]
    data = data.set_index('calendarDate')

    return data


if __name__ == "__main__":
    x= read_stock_inoformation_csv()
    #x=downloading_trade_date()

# -*- coding: utf-8 -*-
"""
Created on Wed May 16 10:21:45 2018

@author: 310128142
"""
import tushare as ts
import pandas
import datetime
import time
import os
import sys
import tqdm


class FudAnalysis(object):
    def __init__(self, code_input=None):
        self.code = code_input
        self.today = datetime.date.today()
        self._date = str(self.today)
        self.base_datas = ts.get_stock_basics()


    @property
    def date(self):
        return self._date

    @property
    def year(self):
        return self._date[0:4]
#TODO: 季度数据目前还没有增加
    @property
    def quarter(self):
        return '2'

    @property
    def month(self):
        return self._date[5:7]

    @property
    def day(self):
        return self._date[8:10]

    @property
    def name(self):  # 中文名称
        _name = self.search_stock_basics().name.values
        return _name

    @property
    def industry(self):  # 所属行业
        return self.search_stock_basics().industry.values

    @property
    def totals(self):  # 总股本（亿）
        _totals = list(self.search_stock_basics().totals.values)
        _totals = _totals + ['亿股']
        return _totals

    @property
    def outstanding(self):
        _out = list(self.search_stock_basics().outstanding.values)
        _out = _out + ['亿股']
        return _out

    @property
    def pb(self):  # 市净率
        return self.search_stock_basics().pb.values[0]

    @property
    def pe(self):  # 市盈率
        return self.search_stock_basics().pe.values[0]
    @property
    def bvps(self):#每股净资产
        return self.search_stock_basics().bvps.values[0]
    @property
    def esp(self):  # 每股收益
        return self.search_stock_basics().esp.values[0]
    
    @property
    def open(self):#当日开盘价格
        data=self.get_now_price().open.values[0]
        return float(data)
    @property
    def high(self):#当日最高点
        data=self.get_now_price().high.values[0]
        return float(data)
    
    @property
    def low(self): #当日最低点
        data=self.get_now_price().low.values[0]
        return float(data)
    @property
    def price(self): #当前价格
        data=self.get_now_price().price.values[0]
        return float(data)
    @property
    def vol(self): #当前交易量
        data=self.get_now_price().volume.values[0]
        return float(data)
    @property
    def amount(self): #当前交易金额
        data=self.get_now_price().amount.values[0]
        return float(data)
    @property
    def turnover(self):
        pass

    def search_stock_basics(self):  # 搜寻股票在基本数据
        df = self.base_datas.reset_index()
        if self.code in df.code.values:
            return df[df['code'] == self.code]
        else:
            pass
    def get_now_price(self):
        df=ts.get_realtime_quotes(self.code)
        return df
    def check_code(self):
        if len(self.code) == 6:
            return True
        else:
            return False


#TODO: 业绩预告因为发布时间不同，所有系统所存的文件未必是最新的，所哟定期需要更新。目前不提供自动更新

    def check_forecast(self,upgrade=False):
        """
        检查该季度内是否发布业绩预告，放在report里面
        Parameters
        ----------
        self.code : stock code
        self.year : 年份
        self.quarter : 季度
        Returns
        -------
        if not search forecast , return None.
        code ：
        name ：
        type : 预升
        report_date :
        pre_eps :
        range:
        """
        _path = '../report/forecast_%s-%s.csv' % (self.year, self.quarter)
        if os.path.exists(_path) and (upgrade == False):
            all_forecast = pandas.read_csv(_path, encoding='gbk', header=0)

            all_forecast.code = all_forecast.code.map(
                lambda x: str(x).zfill(6))
            #all_forecast=all_forecast.set_index(['code'])

        else:
            print('there is not files,watting download %s' % self.year)
            all_forecast = ts.forecast_data(int(self.year), int(self.quarter))
            all_forecast.to_csv(_path, encoding='gbk')

        if self.code in all_forecast.code.values:
            stock_forecast = all_forecast[all_forecast['code'] == self.code]
            return stock_forecast  #print (stock_forecast)
        else:
            print('< %s has not forecast >' % self.code)
            return None

    def restricted_stcok(self, durting=None):
        """
        检查为未来一年的限售股信息

        Parameters
        ----------
        durting 默认值为 12  往后查询多少个月

        Returns
        -------

        """
        if durting is None:
            durting = 6
        else:
            pass
        _month = int(self.month)
        _year = int(self.year)
        rsd = pandas.DataFrame()  #rsd => Restricted Stock Datas
        for i in tqdm.tqdm(range(0, durting)):
            if _month > 12:
                _year += 1
                _month = 1

            else:
                pass
            try:
                rs_m = ts.xsg_data(year=_year, month=_month)
                print(_month, _year)
                rsd = rsd.append(rs_m, ignore_index=True)
            except:
                print('this month data error')
                pass
            _month += 1
        _path = '../report/restricted_stock_%s.csv' % (self.year)
        return rsd

    def check_rs(self, durting=None):
        """
        检查stock 是否在这里面解禁股中

        Parameters
        ----------
        self: 
        durting=None: 定义未来的月份默认12 月

        Returns
        -------

        """
        if durting is None:
            durting = 12
        else:
            pass
        _rsd = self.restricted_stcok(durting=durting)

        if _rsd is None:
            print('the data has error.')
            return None
        elif self.code in _rsd.code.values:
            return _rsd[_rsd['code'] == self.code]
        else:
            print('no restricted stcok for next %s months' % durting)
            return None

if __name__ == "__main__":
    x = FudAnalysis('600362')
    df = x.get_now_price()
    z=ts.get_czce_daily()
    print(x.name, x.code,)
    print(x.base_datas)

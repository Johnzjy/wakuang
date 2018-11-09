import tushare as ts
import pandas as pd
import os

SYS_DIR = os.path.dirname(os.getcwd())#系统路径

class Market(object):

    __num = 0
    __codelist=[]
        
    @classmethod
    def addStockNum(cls):
        cls.__num += 1
        
    @classmethod
    def getStockNum(cls):
        return cls.__num
    
    @classmethod
    def getStockList(cls):
        return cls.__codelist
    @classmethod
    def addStockList(cls,code):
        cls.__codelist.append(code)
    
    def __new__(self,code): #继承stock 导入多重参数
        Market.addStockNum()
        Market.addStockList(code)
        return super(Market,self).__new__(self)


class Stock(Market):
    def __init__(self,codestr):
        #TODO:strp input
        self.code=codestr
        self.profit=self.read_files(mode="profit")
        self.cash=self.read_files(mode="cash")
        self.balance=self.read_files(mode="balance")
        self.infor=self.get_stock_information()
        self.realtime_datas=self.get_realtime_data()
        
        
    def read_files(self, _code=None, mode="profit"):
        """
        
        读取财务报表

        Parameters
        ----------
        self: 
        _code=None:  输入code
        mode="profit":  模式 profit 利润表； cash 现金表； balance  资产负债表

        Returns
        -------

        """
        if _code is not None:
            self.code = _code
        else:
            _code = self.code
        if mode in ["profit", "cash", "balance"]:
            _path = SYS_DIR + "\\report\\StockData\\%s\\%s_%s.csv" % (_code,_code, mode)
            
        else:
            raise ValueError("mode input is error!")
        df = pd.read_csv(
            _path, encoding="gbk")  # 返回一个pandas.core.frame.DataFrame 类型
        df.drop([1])
        return df
    def load_all_stock_information(self,_code=None,):
        """
        
        读取财务报表

        Parameters
        ----------
        self: 
        _code=None:  输入code
        mode="profit":  模式 profit 利润表； cash 现金表； balance  资产负债表

        Returns
        -------

        """
        if _code is not None:
            self.code = _code
        else:
            _code = self.code
        _path= SYS_DIR + "\\report\\Stock_Information.csv"
        df = pd.read_csv(
            _path, encoding="gbk")  # 返回一个pandas.core.frame.DataFrame 类型
        df["code"]=df["code"].map(lambda x: str(x).zfill(6))
        return df
    @property
    def report_date(self): #报告日期
        return self.profit.columns[2]
     
        
    def get_stock_information(self):
        df=self.load_all_stock_information()
        return  df[df["code"]==self.code].loc[0]
    
    def get_realtime_data(self,_code=None):
        if _code is not None:
            self.code=_code
        else:
            _code=self.code
        
        df=ts.get_realtime_quotes(_code)
        return df
        
    @property
    def pe(self): #市盈率
        return self.infor.pe
    @property
    def name(self):#名称
        return self.infor.name
    @property
    def outstanding(self):#circulation shares 流通的股票 单位万股
        return self.infor.outstanding
    @property
    def totals(self):#总发行
        return self.infor.totals
    @property
    def eps(self):#每股收益
        return self.infor.eps

    @property
    def bvps(self):
        return self.infor.bvps

    @property
    def net_profits(self):#当前利润
        return self.infor.net_profits

    @property
    def industry(self):#所属板块
        return self.infor.industry
    
    @property
    def holders(self):
        return self.infor.holders

    @property
    def nifoa(self): #经营业务收入净额 NET INCOME FROM OPERATING ACTIVITIES
        nifoa_list=self.cash[ self.cash["报表日期"]=="经营活动产生的现金流量净额"]
        nifoa=nifoa_list[self.report_date].values[0]
        return nifoa

    @property
    def cffia(self):#投资活动产生的现金流量净额
        cffia_list=self.cash[ self.cash["报表日期"]=="投资活动产生的现金流量净额"]
        cffia=cffia_list[self.report_date].values[0]
        return cffia
    @property
    def cfffa(self):#筹资活动产生的现金流量净额
        cfffa_list=self.cash[ self.cash["报表日期"]=="筹资活动产生的现金流量净额"]
        cfffa=cfffa_list[self.report_date].values[0]
        return cfffa
    @property
    def price(self):
        return float(self.realtime_datas.price.values[0])
    @property
    def amount(self):
        return float(self.realtime_datas.amount.values[0])
    @property
    def per_close(self):
        return float(self.realtime_datas.per_close.values[0])

    
    
if __name__=="__main__":
    a=Stock("000001")


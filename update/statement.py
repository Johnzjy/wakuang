"""
                           █████                                              
                          ░░███                                               
 █████ ███ █████  ██████   ░███ █████ █████ ████  ██████   ████████    ███████
░░███ ░███░░███  ░░░░░███  ░███░░███ ░░███ ░███  ░░░░░███ ░░███░░███  ███░░███
 ░███ ░███ ░███   ███████  ░██████░   ░███ ░███   ███████  ░███ ░███ ░███ ░███
 ░░███████████   ███░░███  ░███░░███  ░███ ░███  ███░░███  ░███ ░███ ░███ ░███
  ░░████░████   ░░████████ ████ █████ ░░████████░░████████ ████ █████░░███████
   ░░░░ ░░░░     ░░░░░░░░ ░░░░ ░░░░░   ░░░░░░░░  ░░░░░░░░ ░░░░ ░░░░░  ░░░░░███
                                                                      ███ ░███
                                                                     ░░██████ 
                                                                      ░░░░░░  
"""

import pandas as pd
import tushare as ts
import os
import sys
import numpy as np
import time
PATH = os.path.dirname(os.path.abspath(__file__))  #利用__file__找到当前路径
os.chdir(PATH)
sys.path.append('..')
print("\n\n", os.getcwd(), "\n\n")

from src import code_list
from update import code_list_cvs

stock_3s = {
    "profit": {
        0: "operating _income",  #营业收入
        13: "operating_expenditure",  #营业支出
        18: "osperating_profit",  #营业利润
        23: "net_profit",  #净利润
        26: "mgsy",  #每股收益
    },
    "cash": {
        0: "d",
        1: "e",
        2: "f",
    },
    "balance": {
        0: "g",
        1: "h",
        2: "l",
    }
}


#zjy
#TODO:
class StockFolder():
    """
    建立stock 数据库文件夹
    """

    def __init__(self):
        self.code = "000001"
        self.__sys_dir = os.path.dirname(os.getcwd())
        self.mode = "profit"
        self.def_path=self.__sys_dir + "\\report\\StockData"
    
    def stock_dirs(self, path=None):  # 获取现在的stock的目录
        if path is None:
            path =self.def_path
        pass
        return path + "\\%s" % self.code

    def creat_folder(self):
        """
        创建code 目录
        """
        path = self.def_path
        if os.path.exists(path) is True:
            if os.path.exists(path + "\\%s" % self.code) is True:
                pass
            else:
                os.makedirs(path + "\\%s" % self.code)
                print("\nCreat %s folder \n" % self.code)  # log massage
        else:
            os.makedirs(path)
            print("Creat %s" % path)  # log massage
            self.creat_folder()

    def delete_dirs(self):
        """
        删除目录
        """
        pass

    def delete_stock(self):
        """
        清空文件夹
        """

        pass

    def check_folder_date(self, _path=None):
        """
        检查文件夹修改信息
        """
        if _path is None:
            _path = self.__sys_dir
        else:
            pass
        return os.stat(_path)
    def folder_and_files(self):
        """
        return report folders list
        [path,[files1,files2,file3]],[]......
        """
        
        f_list=[]
        for root, dirs, files in os.walk(self.def_path):
            dir_list=[root,files]
            if len(files) == 3:
               f_list.append(dir_list)
        
            else:
                pass
        return f_list
    
    def folders_list(self):
        
        x=pd.DataFrame(self.folder_and_files())
        return x[0]
    

class StockStatement(StockFolder):
    """
    获取财务报表，并处理数据。
    """

    def __init__(self):
        StockFolder.__init__(self)
        self.code = "0000001"
        self.mode = "profit"

    def download_statement(self, _code=None, _path=None):
        """
        下载财务报表
        
        """

        if _code is not None:
            self.code = _code
        else:
            pass
        if _path is None:
            self.creat_folder()
            _path = self.stock_dirs()
        else:
            pass

        print("\n start up the %s statement downloading...\n" % self.code)

        self.profit = ts.get_profit_statement(self.code)
        self.profit = self.profit.drop([0])
        time.sleep(1)
        #print (">>>",end="")
        self.profit.to_csv(
            _path + "\\%s_profit.csv" % self.code, encoding="gbk")
        #print (">>>",end="")
        self.cash = ts.get_cash_flow(self.code)
        self.cash = self.cash.drop([0])
        time.sleep(1)
        #print (">>>",end="")
        self.cash.to_csv(_path + "\\%s_cash.csv" % self.code, encoding="gbk")
        #print (">>>",end="")
        self.balance = ts.get_balance_sheet(self.code)
        time.sleep(1)
        #print (">>>",end="")
        self.balance.to_csv(
            _path + "\\%s_balance.csv" % self.code, encoding="gbk")
        #print (">\n")
        print("  completed downloading!")

    def dafs(self):
        """
        Download all financial statements

        下载所有股票的财务报表



        Parameters
        ----------
        self: 

        Returns
        -------
        按照code 存储在report  StockDate 中
        """
        __list = code_list.list_all()
        import tqdm
        for c in tqdm.tqdm(__list):
            self.download_statement(_code=c)

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
            _path = self.stock_dirs() + "\\%s_%s.csv" % (_code, mode)
        else:
            raise ValueError("mode input is error!")
        df = pd.read_csv(
            _path, encoding="gbk")  # 返回一个pandas.core.frame.DataFrame 类型
        df.drop([1])
        return df

    #TODO: 加入
    def _calculate_ones_yoy(self,
                            df=None,
                            year_1="20180331",
                            year_2="20170331"):
        """
        计算报表中两个报表之间的百分比
        参数： year_1 ：此期报表
              year_2  : 上期报表
        """
        if df is None:  #如果是None  则读取默认数据
            df = self.read_files(mode=self.mode)
        else:
            pass
        col_name = df.columns.tolist()
        
        col_name.insert(col_name.index("%s" % year_1) + 1, "%s_yoy" % year_1)
        df = df.reindex(columns=col_name)
        try:
            df["%s_yoy" % year_1] = (
                df["%s" % year_1].astype(np.float) - df["%s" % year_2].astype(
                    np.float)) / df["%s" % year_2].astype(np.float)  #计算并返还Datafram
        except:
            df["%s_yoy" % year_1] = None
        return df

    def calculate_yoy(self, save=True):
        """
        计算此报表中所有数据
        """
        try:  #尝试读取一遍文件，不行，重新下载再读

            yoy_df = self.read_files(mode=self.mode)  #尝试读取文件 如果没有信息则下载

        except:
            self.download_statement()
            yoy_df = self.read_files(mode=self.mode)

        col_name = yoy_df.columns.tolist()

        for i in col_name[2:]:
            if i[-4:] == "_yoy":
                continue
            else:
                pass
            frist_year = int(i)
            second_year = frist_year - 10000
            if str(second_year) in col_name:
                if "%s_yoy" % frist_year not in col_name:
                    yoy_df = self._calculate_ones_yoy(
                        df=yoy_df,
                        year_1="%s" % frist_year,
                        year_2="%s" % second_year)
        if save is True:
            yoy_df = yoy_df.drop(["Unnamed: 0"], axis=1)
            yoy_df.to_csv(
                self.stock_dirs() + "\\%s_%s.csv" % (self.code, self.mode),
                encoding="gbk")
        return yoy_df

    def cal_tree_statement(self):
        """
        计算个股三张表的同比数据
        """
        __mode_temp = self.mode
        for i in ["profit", "cash", "balance"]:

            self.mode = i
            self.calculate_yoy()
            print("process : calculat %s Year-on-year growth for %s\n" %
                  (i, self.code))
        self.mode = __mode_temp
        return True

    def cal_all_yoy(self):
        """
        Calculate all stock statements year - on - year data
        if the report has not the stock finance statements, will download before calculate.
        """
        __list = code_list.list_all()
        import tqdm
        for c in tqdm.tqdm(__list):
            self.code = c
            self.cal_tree_statement()
            
class ThreeCashFlows(StockFolder):
    """
    获取财务报表，并处理数据。
    """

    def __init__(self):
        StockFolder.__init__(self)
   
        self.fl=list(self.folders_list())
    def get_TCF(self,_code=None,_date=None):# get Three Cash Flows from folders
        if _date is None:
            _date = "20180630"
        if _code is None:
            _code =self.code
        df =self.read_cashcsv_data(_code)
        
        nifoa_v=df[ df["报表日期"]=="经营活动产生的现金流量净额"]
        cffia_v=df[ df["报表日期"]=="投资活动产生的现金流量净额"]
        cfffa_v=df[ df["报表日期"]=="筹资活动产生的现金流量净额"]
        
       
        tcf={ " nifoa" : nifoa_v[_date].get_values()[0], #经营业务收入净额 NET INCOME FROM OPERATING ACTIVITIES
              " cffia" : cffia_v[_date].get_values()[0], #投资活动产生的现金流量净额 cash flow from investment activities
              " cfffa" : cfffa_v[_date].get_values()[0], #筹资活动产生的现金流量净额 Cash flows from financing activities
                }
        return tcf
            
    
    def read_cashcsv_data(self,_code=None):
        if _code is None :
            _code =self.code
        _path =self.def_path +"\\%s"%_code
          
        if len(_code) is 6 and _path in self.fl:
      
            file_path=_path+"\\%s_cash.csv"%_code

            df=pd.read_csv(file_path,encoding="gbk")
  
            return df.drop(['Unnamed: 0'],axis=1)
        else:
            return None
    def check_cash_status(self,_code=None,_date=None):
        """
        检查现金流状态
        """
        if _date is None:
            _date = "20180630"
        if _code is None:
            _code =self.code
        df =self.get_TCF(_code,_date)
        _v=df.values()
        _v=list(_v)
        if (_v[0] >= 0) and (_v[1] >= 0) and(_v[2] >= 0) : # +++
            return "status_1"
        elif _v[0] >= 0 and _v[1] >= 0 and _v[2] < 0 :# ++-
            return "status_2"
        elif _v[0] >= 0 and _v[1] < 0 and _v[2] >= 0 :#+-+
            return "status_3"        
        elif _v[0] >= 0 and _v[1] < 0 and _v[2] < 0 :#+--
            return "status_4"
        elif _v[0] < 0 and _v[1] >= 0 and _v[2] >= 0 :#-++
            return "status_5"
        elif _v[0] < 0 and _v[1] >= 0 and _v[2] < 0 :#-+-
            return "status_6"
        elif _v[0] < 0 and _v[1] < 0 and _v[2] >= 0 :#--+
            return "status_7"
        elif _v[0] < 0 and _v[1] >= 0 and _v[2] < 0 :#---
            return "status_8"
        else:
            return None
    def get_cash_status_all(self,code_list,date_list):
        df=pd.DataFrame(index=code_list,columns=date_list)
        
        for c in code_list:
            for d in date_list:
                df.at[c,d]=self.check_cash_status(_code=c,_date=d)
        
        return df
        


if __name__ == "__main__":

    creat = ThreeCashFlows()
    creat.code="000021"
    c_l=["000021","000001","000011","000010","000005","000007"]
    d_l=["20180630","20180331","20170630"]
    x=creat.get_cash_status_all(c_l,d_l)
    #creat.cal_tree_all()
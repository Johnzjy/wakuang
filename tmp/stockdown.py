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

    def stock_dirs(self, path=None):  # 获取现在的stock的目录
        if path is None:
            path = self.__sys_dir + "\\report\\StockData"
        pass
        return path + "\\%s" % self.code

    def creat_folder(self):
        """
        创建code 目录
        """
        path = self.__sys_dir + "\\report\\StockData"
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
        self.profit.to_csv(_path + "\\%s_cash.csv" % self.code, encoding="gbk")
        #print (">>>",end="")
        self.balance = ts.get_balance_sheet(self.code)
        time.sleep(1)
        #print (">>>",end="")
        self.profit.to_csv(
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

        df["%s_yoy" % year_1] = (
            df["%s" % year_1].astype(np.float) - df["%s" % year_2].astype(
                np.float)) / df["%s" % year_2].astype(np.float)  #计算并返还Datafram
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

    def cal_tree_all(self):
        """
        Calculate all stock statements year - on - year data
        if the report has not the stock finance statements, download before calculate.
        """
        __list = code_list.list_all()
        import tqdm
        for c in tqdm.tqdm(__list):
            self.code = c
            self.cal_tree_statement()

if __name__ == "__main__":

    creat = StockStatement()
    creat.cal_tree_all()
    #creat.cal_tree_all()
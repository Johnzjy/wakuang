import pandas as pd    
import tushare as ts   
import os 
import sys

import time
sys.path.append('..')

from src import code_list
from update import code_list_cvs

#path=os.path.dirname(os.getcwd())+'\\list\\' # 存储路径
#print (path)
#code_list_cvs.update_list()

class StockFolder():
    def __init__(self):
        self.code ="000001"
        self.__sys_dir=os.path.dirname(os.getcwd())
        
    def creat_folder(self):
        """
        创建code 目录
        """
        path = self.__sys_dir +  "\\report\\StockData"
        if os.path.exists(path) is True:
            if os.path.exists(path+"\\%s"%self.code) is True:
                pass
            else:
                os.makedirs(path+"\\%s"%self.code)
                print ("\nCreat %s folder \n"%self.code) # log massage
                self.stock_dirs= path+"\\%s"%self.code
            self.stock_dirs= path+"\\%s"%self.code
        else:
            os.makedirs(path)
            print("Creat %s"%path) # log massage
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

    def check_folder_date(self,_path=None):
        """
        检查文件夹修改信息
        """
        if _path is None:
            _path =self.__sys_dir
        else:
            pass
        return os.stat(_path)
    
class StockData(StockFolder):
    def __init__(self):
        StockFolder.__init__(self)
        self.code="600362"
    def download_statement(self,_code=None,_path=None):
        if _code is None:
            _code =self.code
        else:
            self.code = _code
        if _path is None:
            self.creat_folder()
            _path= self.stock_dirs
        else:
            pass

        print("\n start up the %s statement downloading...\n"%_code)

        self.profit=ts.get_profit_statement(_code)
        time.sleep(1)
        #print (">>>",end="")
        self.profit.to_csv(_path+"\\%s_profit.csv"%_code)
        #print (">>>",end="")
        self.cash=ts.get_cash_flow(_code)
        time.sleep(1)
        #print (">>>",end="")
        self.profit.to_csv(_path+"\\%s_cash.csv"%_code)
        #print (">>>",end="")
        self.balance=ts.get_balance_sheet(_code)
        time.sleep(1)
        #print (">>>",end="")
        self.profit.to_csv(_path+"\\%s_balance.csv"%_code)
        #print (">\n")
        print ("  completed downloading!")
    def download_all(self):
        __list=code_list.list_all()
        import tqdm
        for c in tqdm.tqdm(__list):
            self.download_statement(_code= c)
    def read_files(self,_code=None,mode="profit"):
        if _code is not None:
            self.code =_code
        else:
            _code =self.code
        _path=self.stock_dirs+"\\%s_profit.csv"%_code
        df=pd.read_csv()
        
        

if __name__ == "__main__":
    creat =StockData()
    #creat.download_statement()
    creat.download_all()
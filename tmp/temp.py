import pandas as pd
import os
import tushare as ts





class Statements(object):
    def __init__(self,):
        self.filetype=["profit","cash","balance"]
        self.code= "600002"
        
    def get_path(self):
        __path= os.getcwd()
        return __path
    
'''
    def remove_file(self,__path = None):
        if __path is None :
            __path = self.get_path()
        else:
            pass
        os.remove(__path)
'''     
        
    def get_statement(self,down= True):
        self.profit=ts.get_profit_statement(self.code)
        self.cash=ts.get_cash_flow(self.code)
        self.balance=ts.get_balance_sheet(self.code)
        
        if down is True:
            for __tpye in self.filetype:
                __path = self.get_path()+"\\"+__tpye+"%s.csv"%self.code
                if __tpye is "profit":
                    self.profit.to_csv(__path)
                elif  __tpye is "cash":
                    self.cash.to_csv(__path)
                elif  __tpye is "balance":
                    self.balance.to_csv(__path)
                    
        
if __name__ == "__main__":
    a= Statements()
    a.get_statement()


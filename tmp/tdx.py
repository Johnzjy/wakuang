import pytdx
from pytdx.hq import TdxHq_API
import pandas
import datetime
tdx_api=TdxHq_API()
from pytdx.params import TDXParams
IP = '119.147.212.81'
PORT = 7709
def get_k_data_tdx(Code=None, startDate=None, endDate=None):
    if Code is None :
        Code = '000001'
    else:
        pass
    if startDate is None:
        startDate = "2017-01-01"
    else:
        pass
    if endDate is None:
        endDate = '2018-01-01'
    else:
        pass
    with tdx_api.connect(IP, PORT):
        data=tdx_api.get_k_data(Code,startDate,endDate)
        data=pandas.DataFrame(data)
        data.date=data.date.apply(
                lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
    print (data)
    return data

def get_stock_number():
    with tdx_api.connect(IP, PORT):
        data=tdx_api.get_security_count(1)
        print(data)
def get_stock_list_tdx():
    with tdx_api.connect(IP, PORT):
        data=tdx_api.get_security_list(1,0)
        data=pandas.DataFrame(data)
        print(data)

def get_data_tdx():
    with tdx_api.connect(IP, PORT):
        data = tdx_api.get_finance_info(0, '000001')
        data =pandas.Series(data)
        print (data)
def get_block_tdc():
    with tdx_api.connect(IP, PORT):
        data=tdx_api.get_and_parse_block_info("block.dat")
        data=pandas.DataFrame(data)
        print(data)
get_block_tdc()
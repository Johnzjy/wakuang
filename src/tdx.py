import datetime

import pandas
import pytdx
from pytdx.hq import TdxHq_API
from pytdx.params import TDXParams
from tqdm import tqdm


class TDX(object):
    '''
    This class is tong da xin data source.
    We can use it to get down the stock datas.
    Tushare can't get minter line and or year line.
    TDX can search index of stock and funds.
    '''
    def __init__(self):
        self.tdx_api = TdxHq_API()
        self._ip = '119.147.212.81'  #输入IP
        self._port = 7709  #端口
        self._code = '600200'
        self._market = 1  #市场代码 0:深圳，1:上海
        self._startdate = "2017-01-01"
        self.today = datetime.date.today()
        self._enddate = datetime.datetime.strftime(self.today, '%Y-%m-%d')

        self.mkt_segment = {
            'sh': '60',
            "sz": '00',
            "cyb": "30",
        }  #segment  当前板块开始字符串
    def __str__(self):
        return 'TDX object (code : %s)' % self.code
    @property
    def IP(self):  # IP
        return self._ip

    @property
    def PORT(self):
        return self._port

    @property
    def code(self):  #定义stock code 属性
        return self._code

    @code.setter  #设定code
    def code(self, code_input):
        """
        The setter of the code property
        """
        if not isinstance(code_input, str):  #确定是否是字符串
            raise ValueError('the code must string!')
        if not len(code_input) == 6:  #确定长度
            raise ValueError('the code value error,the len must SIX !')
        if code_input.startswith('60'):  #确定表头
            self._market = 1
        elif code_input.startswith('00'):
            self._market = 0
        elif code_input.startswith('30'):
            self._market = 0
        else:
            raise ValueError('this code is not stock code')
        self._code = code_input

    @property
    def startdate(self):  #开始日期
        return self._startdate

    @startdate.setter  #设置日期
    def startdate(self, date_input):
        """
        The setter of the start date property
        """
        if not isinstance(date_input, str):
            raise ValueError('the date must string!')
        if not len(date_input) == 8:
            raise ValueError(
                'the date value error,the date formet must xxxx-xx-xx !')
        self._startdate = date_input

    @property  #结束日期
    def enddate(self):
        return self._enddate

    @enddate.setter
    def enddate(self, date_input):
        """
        The setter of the start date property
        """
        if not isinstance(date_input, str):
            raise ValueError('the date must string!')
        if not len(date_input) == 8:
            raise ValueError(
                'the date value error,the date formet must xxxx-xx-xx !')
        self._enddate = date_input

    def get_day_data_tdx(self):  #获取K line
        with tdx_api.connect(IP, PORT):
            data = tdx_api.get_k_data(self.code, self.startdate, self.enddate)
            data = pandas.DataFrame(data)
            data.date = data.date.apply(
                lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
        return data

    #TODO: 现在是用800点进行计数，以后会细化功能
    def get_k_data_tdx(self, k_mode=9):
        """
        获取k 线图，总计800 点

        Parameters
        ----------
        k_mode= 0-11 
                    0 5分钟K线 
                    1 15分钟K线 
                    2 30分钟K线 
                    3 1小时K线 
                    4 日K线
                    5 周K线
                    6 月K线
                    7 1分钟
                    8 1分钟K线 9 日K线
                    10 季K线
                    11 年K线

        Returns
        -------

        """
        with self.tdx_api.connect(self.IP, self.PORT):
            data = self.tdx_api.get_security_bars(k_mode, self._market,
                                                  self.code, 0, 800)

            data = pandas.DataFrame(data)
            #data.date = data.date.apply(
            #    lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))
        return data

    def len_market(self):  #市场有多少只股票
        with tdx_api.connect(IP, PORT):
            _len = tdx_api.get_security_count(self._market)
        return _len

    def get_page_tdx(self, block=None):

        if block is None:
            market = 1
            page = [0]
        elif block in ['sh', 'SH']:
            market = 1
            page = [13, 14]
        elif block in ['sz', 'SZ']:
            print('block for shenzhen')
            market = 0
            page = [0, 1]
        elif block in ['cyb', 'CYB']:
            print('block for chuang ye ban')
            market = 0
            page = [7, 8]
        else:
            pass
        code_list_df = pandas.DataFrame()
        with tdx_api.connect(IP, PORT):
            for pn in page:
                data = tdx_api.get_security_list(market, pn * 1000)
                data = pandas.DataFrame(data)
                print(data)
                code_list_df = code_list_df.append(data, ignore_index=True)
        return code_list_df

    def get_base_finace_tdx(self):
        with tdx_api.connect(IP, PORT):
            data = tdx_api.get_finance_info(0, '000001')
            data = pandas.Series(data)
            print(data)

    def get_min_data(self):
        from pytdx.params import TDXParams
        with tdx_api.connect(IP, PORT):
            data = tdx_api.get_history_minute_time_data(
                TDXParams.MARKET_SH, '600300', 20161209)
            data = pandas.DataFrame(data)
            print(data)

    #TODO: 需要确定 0: buy  1 : sell
    def get_tick_data(self):
        """
        历史分笔交易：time 顺序； price ; vol ;buyorsell [1:] [0:];

        sh 60 13000-14000


        Parameters
        ----------

        Returns
        -------

        """
        print('start ')
        data = pandas.DataFrame()
        with tdx_api.connect(IP, PORT):
            for i in [2000, 0000]:
                df = tdx_api.get_history_transaction_data(
                    TDXParams.MARKET_SH, "600547", i, 2000, 20160308)
                df = pandas.DataFrame(df)

                data = data.append(df, ignore_index=True)

        return data

    def get_tick_today(self):
        """
        Get every time the each deal for today.每组数最大len 2 k 所以要确定的数据长度

        Parameters
        ----------
        self: 

        Returns
        -------

        """

        with tdx_api.connect(IP, PORT):
            data = pandas.DataFrame()
            for i in [0, 2000]:
                df = tdx_api.get_transaction_data(TDXParams.MARKET_SZ,
                                                  '000001', i, 2000)
                df = pandas.DataFrame(df)
                data = data.append(df, ignore_index=True)
            print(data)
        return data

    def get_block(self):
        with tdx_api.connect(IP, PORT):
            data = tdx_api.get_and_parse_block_info("block.dat")
            data = pandas.DataFrame(data)
            print(data)

    def get_market_segment_list(self, mkt):
        data = self.get_page_tdx(mkt)
        self.code_list = pandas.DataFrame()
        pbar = tqdm(total=len(data.code))
        mkt_hard = self.mkt_segment[mkt]
        for idx, _code in enumerate(data.code):
            pbar.update(1)
            if _code.startswith(mkt_hard, 0, 2):
                self.code_list = self.code_list.append(
                    data.loc[idx], ignore_index=True)
        return self.code_list

    def get_sh_list(self):
        return self.get_market_segment_list('sh')

    def get_sz_list(self):
        return self.get_market_segment_list('sz')

    def get_cyb_list(self):
        return self.get_market_segment_list('cyb')


if __name__ == "__main__":
    a = TDX()
    x = a.get_data_tdx()
    print(x)

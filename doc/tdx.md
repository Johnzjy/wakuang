TDX（通达信）
=====

## TDX  
    通达信是通过pytdxlib扩展的数据接口
    目前用了基本的数据接口，未使用扩展和其他的

### class TDX
    .code ： stock 代码
    .PORT :  通达信服务器端口
    get_k_data_tdx ：收集K 线 
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
    get_sh_list ：获取上证板块所有股票代码
    get_sz_list ：获取深圳版块所有股票代码
    get_cyb_list：获取创业板块所有股票代码

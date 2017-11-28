wakuang
=======

wakuang 是一个平台包，支持python3.6

所需要的第三方库：
    .. `tushare`
    .. `TA-lib`
    .. `pandas`
    .. `PYQT4`
    .. `tqdm`
    .. `wechat-sdk`
    
功能介绍
--------

#data_contorl|
            .. CYQ.py :计算筹码分布
            .. Daily_data_reporting.py :统计每天龙虎榜，机构大单 买入卖出情况 分5 日，15日，30日
            .. Daily business hall.py  ：处理Daily_data_reporting中的数据
            .. stock_unblocked.py  ：下载解禁股票
            
#scr         |
            .. Action_main.py   ：GUI下的执行文件
            .. colors.py        ：字体颜色文件
            .. config.py        ：config文件
            .. email_163.py     ：邮箱文件
            .. wechat_tuling.py ：微信和图灵机
            .. Graph.py         ：GUI绘图
            .. layout.py        ：GUIlayout
            .. logd.py          ：log文件 建立装饰包
            

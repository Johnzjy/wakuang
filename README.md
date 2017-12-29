# ![wakuang][WK]  
WaKuang(挖矿)
=======
[![Build Status](https://travis-ci.org/meolu/walle-web.svg?branch=master)](https://travis-ci.org/meolu/walle-web)
[![John.zhang](https://img.shields.io/badge/Powered_by-John_Zhang-green.svg?style=flat)](http://www.yiiframework.com/)

wakuang 是一个平台包，支持python3.6.引入tuling API : [Tuling官方主页](http://www.tuling123.com/openapi/api)

所需要的第三方库：  
    .. `tushare`  
    .. `TA-lib`  
    .. `pandas`  
    .. `PYQT4`  
    .. `tqdm`  
    .. `wechat-sdk`  
    .. `gmsdk-2.9.9-py3-none-any`(http://www.myquant.cn/gm2/downloads/)  
    
功能介绍
--------

data_contorl
 

* CYQ.py : 计算筹码分布  
* Daily_data_reporting.py : 统计每天龙虎榜，机构大单 买入卖出情况 分5 日，15日，30日  
* Daily business hall.py ：处理Daily_data_reporting中的数据  #
* stock_unblocked.py ：下载解禁股票
* [technical_indicators](#technical_indicators)：技术指标
scr           

* Action_main.py   		：GUI下的执行文件  
* colors.py       		：`字体颜色文件` 
* config.py       		：config文件  
* email_163.py    		：邮箱文件  
* wechat_tuling.py 		：微信和图灵机  
* Graph.py       		：GUI绘图  
* layout.py      		：GUIlayout  
* logd.py       		：log文件 建立装饰包 
Fun

### technical_indicators
	* get_date_ts(Code,startDate,endDate):获取数据
		* parameter
			 > Return:Dateframe
			 > Code:代码
			 > startDate:开始日期
			 > endDate:结束日期
			 
To Do List
----------
- [x] 已做
- [ ] 未做做
- [ ] Travis CI integration
- [ ] Mail events：specify kinds of events
- [ ] Gray released：specify servers
- [ ] Websocket instead of poll
- [ ] A manager of static source
- [ ] Configure variables
- [ ] Support Docker
- [ ] Open api
- [ ] Command line
版本             
---
**0.0**
=======

[WK]:https://github.com/Johnzjy/wakuang/blob/master/scr/ico/title.jpg

# ![wakuang][WK]  
WaKuang(挖矿 by John zhang)[![email](https://img.shields.io/badge/email-aprzephyr%40163.com-ff69b4.svg)](http://shields.io/) 
=======
[![Build Status](https://travis-ci.org/meolu/walle-web.svg?branch=master)](https://travis-ci.org/meolu/walle-web)
[![John.zhang](https://img.shields.io/badge/Powered_by-John_Zhang-green.svg?style=flat)](http://www.yiiframework.com/)
[![PY Version](https://img.shields.io/pypi/pyversions/Django.svg)](http://shields.io/) 
[![code size](https://img.shields.io/badge/code%20size-355k-orange.svg)](http://shields.io/) 

### Installation
------------
Wakuang 是一个量化平台，支持python3.6.引入掘金回测机制 [掘金官方主页](https://www.myquant.cn/) 
通过大数据处理，分析和挖掘二级市场波动变化。亦可以编写量化交易策略，引入Decision Tree等机器学习算法。

##### 所需要的第三方库：  
    .. `tushare`  
    .. `TA-lib`  
    .. `pandas`  
    .. `PYQT4`  
    .. `tqdm`  
    .. `wechat-sdk`  
    .. `gmsdk-2.9.9-py3-none-any`(http://www.myquant.cn/gm2/downloads/)  
    
## 功能介绍
--------
[x] 已完成 [ ] 未完成
## data_contorl
 
* [x] [technical_indicators](#technical_indicators)：技术指标
* [x] [CYQ](#CYQ) : 计算筹码分布  
* [x] Daily_data_reporting.py : 统计每天龙虎榜，机构大单 买入卖出情况 分5 日，15日，30日  
* [x] Daily business hall.py ：处理Daily_data_reporting中的数据  
* [x] stock_unblocked.py ：下载解禁股票
* [ ] DuPontAnalysis:杜邦分析法
* [ ] forecast:现金流评估


## scr           

* [x] Action_main.py   		：GUI下的执行文件  
* [x] main_loop.py   		：文本式菜单
* [x] colors.py       		：`字体颜色文件` 
* [x] config.py       		：config文件  
* [x] email_163.py    		：邮箱文件  
* [x] wechat_tuling.py 		：微信和图灵机  
* [x] Graph.py       		：GUI绘图  
* [x] layout.py      		：GUIlayout  
* [x] logd.py       		：log文件 建立装饰包 
##Fun

### technical_indicators
技术指标计算，利用传统的指标算法构建有效符合A股。

```
```
* get_date_ts(Code,startDate,endDate):获取数据 
	* parameter 
		 > Return:Dateframe
		 > Code:代码
		 > startDate:开始日期
		 > endDate:结束日期
### CYQ  筹码分析
对股票每个价位的交易进行统计计算，已完成对庄家和主要压力点的测算
##### PQ 
```
计算每天筹码交易 单位（手，100股）
返回每天交易量，交易次数
```
* PQ(code,date)
    * parameter 
		 > Return:list
		 > Code:代码
		 > Date:开始日期
##### CYQ
```
计算一段日期内的筹码分布
```
* CYQ
    * parameter 
		 > Return:
		 > 
		 > 
##### Draw_CYQ
```
画出一段时间内的筹码 价格 量  时间，存图路径../report/CYQ/
```		
* Draw_CYQ
    * parameter 
		 > Return:list
		 > Code:代码
		 > Date:开始日期
 

To Do List
----------
- [x] 已做
- [ ] 未做做
- [ ] build cash flow display
- [ ] completed GUI
- [ ] Mail events：specify kinds of events
- [ ] Wechat events
- [ ] Open api
- [ ] Command line
版本             
---
**0.0**
=======

### history
2017年12月29日16:58:06 对README.MD 框架完成修订  @author: John zhang 


[WK]:https://github.com/Johnzjy/wakuang/blob/master/scr/ico/title.jpg

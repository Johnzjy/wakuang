# ![wakuang][WK]  
WaKuang(挖矿 by John zhang) 
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
|Lib | 描述 |版本|
|:----:| :----: |:----|
|tushare|股票数据接口|
|pyqtgraph| 绘图工具|
|TA-lib|  （TA-Lib 通过pip直接安装可能会出错，需要下载.whl格式文件。[Ta-lib](/doc/ta-lib.md) 查询）|0.4.10
|pyecharts| 图表绘图工具|0.1.4|
|pandas|数据格式处理|  0.20.3|
|PYQT5|GUI绘制功能，还需要qtpy支持|5.9.2|  
|wechat-sdk|微信接口|  
|tqdm|进度条小工具|4.14.0
|html5lib| HTML 协议 lib
|gmsdk|回测框架（选项）|gmsdk-2.9.9-py3-none-any`(http://www.myquant.cn/gm2/downloads/) 
|rqalpha|回测机制框架（选项）| 
    
## 功能介绍
--------
####KLIN ,MACD ，RSI 等基本指  
```  目前在GUI可以调用，Kline，MACD，布林线，RSI等常用指标。在technical_indicators中用户还可以完成，自由的算法设定。目前痛过迭代运算，回测A股3000多只股票过去三年的交易情况，优化了常规算法的参数。```  	
# ![k][kline]

####十大股东排行榜  
```  输入股票code之后，软件会自动计算设定区域内的大股东排行。方便大家查询证金等国家队动向。```  
# ![t][charts]
[x] 已完成 [ ] 未完成
## data_contorl
 
* [x] [technical_indicators](#technical_indicators)：技术指标
* [x] [CYQ](#CYQ) : 计算筹码分布  
* [x] Daily_data_reporting.py : 统计每天龙虎榜，机构大单 买入卖出情况 分5 日，15日，30日  
* [x] Daily business hall.py ：处理Daily_data_reporting中的数据
* [x] Top10shareholder.py ：查询个股top10流通股持有率    
* [x] stock_unblocked.py ：下载解禁股票
* [ ] DuPontAnalysis:杜邦分析法
* [ ] forecast:现金流评估
* [x] GUI_2: 软件界面   
* [x] GUI_2: top 10 股东排行榜



## src (source file)          

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
- [x] completed GUI_2 （the frist version compeled，add RSI）
- [ ] Mail events：specify kinds of events
- [ ] Wechat events
- [ ] Open api
- [ ] Command line
- [ ] 准备调研的接口[安妮信息](http://smartanni.com/ )
```
神奇公式
- [ ]核心指标之一：选取便宜的股票，也就是选取息税前盈余／企业价值（EBIT/EV）高的股票，其中EV = market value of equity + net interest-bearing debt，即企业价值=市值+净有息债务

- [x]核心指标之二：选取好的业务，也就是选取有形资本回报率（Return on Capital）高的股票，其中Return on Capital = EBIT / (Net WorkingCapital + Net Fixed Assets)，即资本回报率 = 息税前利润 /（净流动资本 + 净固定资产）

GARP的核心主要是PEG

策略说明：

1、公司的资产负债率小于等于 25%
这一条对公司的负债水平做出了要求。较低的资产负债率可以让公司灵活的应对各种突发事件可能对公司带来的冲击。

2、公司每股净现金大于 0
公司的每股现金流为正值，表示公司处于建康的营运状态中，每股收益的含金量很高。

3、当前股价与每股自由现金流量比小于 10(市现率)
这一规则对股票的估值水平提出了要求，并以公司的财务灵活性指标作为估值的基准。

4、市盈率在所有股票中在30%以下(首先PE必须大于0)

5、PEG=市盈率/盈利增长率<0.5
这一规则说明市盈率的增长不及盈利的增长，股票价格处于相对低位，体现了彼得.林奇偏好成长兼具价值股票的



```
版本             
---
**1.1**
=======
[![email](https://img.shields.io/badge/email-aprzephyr%40163.com-ff69b4.svg)](http://shields.io/)  

### history
2017年12月29日16:58:06 对README.MD 框架完成修订  @author: John zhang 


[WK]:https://github.com/Johnzjy/wakuang/blob/master/scr/ico/title.jpg
[charts]:/scr/ico/top10charts.PNG
[kline]:/scr/ico/kline.PNG

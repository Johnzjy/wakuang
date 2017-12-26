
WaKuang(挖矿)
=======

wakuang 是一个平台包，支持python3.6.引入tuling API('http://www.tuling123.com/openapi/api')

所需要的第三方库：  
    .. `tushare`  
    .. `TA-lib`  
    .. `pandas`  
    .. `PYQT4`  
    .. `tqdm`  
    .. 'wechat-sdk'  
    .. 'gmsdk-2.9.9-py3-none-any'(http://www.myquant.cn/gm2/downloads/)  
    
功能介绍
--------

#data_contorl  

            .. CYQ.py 		:计算筹码分布  
            .. Daily_data_reporting.py :统计每天龙虎榜，机构大单 买入卖出情况 分5 日，15日，30日  
            .. Daily business hall.py  ：处理Daily_data_reporting中的数据  
            .. stock_unblocked.py 	：下载解禁股票  
#scr           

            .. Action_main.py   	：GUI下的执行文件  
            .. colors.py       ：字体颜色文件  
            .. config.py       ：config文件  
            .. email_163.py     ：邮箱文件  
            .. wechat_tuling.py 	：微信和图灵机  
            .. Graph.py       	：GUI绘图  
            .. layout.py       ：GUIlayout  
            .. logd.py        ：log文件 建立装饰包 
            
版本             
---
**0.0**
~~~~
=======

Markdown 语法速查表  
1 标题与文字格式  
标题  
# 这是 H1 <一级标题>  
## 这是 H2 <二级标题>  
###### 这是 H6 <六级标题>  
文字格式  
**这是文字粗体格式**  
*这是文字斜体格式*  
~~在文字上添加删除线~~  
2 列表  
无序列表  
* 项目1  
* 项目2  
* 项目3  
有序列表  
1. 项目1  
2. 项目2  
3. 项目3  
   * 项目1  
   * 项目2  
3 其它  
图片  
![图片名称](http://gitcafe.com/image.png)  
链接  
[链接名称](http://gitcafe.com)  
引用  
> 第一行引用文字  
> 第二行引用文字  
水平线  
***  
代码  
`<hello world>`  
代码块高亮  
```ruby  
  def add(a, b)  
    return a + b  
  end  
```  
表格  
  表头  | 表头  
  ------------- | -------------  
 单元格内容  | 单元格内容  
 单元格内容l  | 单元格内容  


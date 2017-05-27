# -*- coding: utf-8 -*-
"""
Created on Tue May  2 13:39:17 2017

@author: 310128142
"""
import technical_indicators as ti
import matplotlib.pyplot as plt
from scr import colors
import configparser
import warnings
import time
warnings.filterwarnings("ignore")

today = time.strftime('%Y-%m-%d %H:%M:S %A',time.localtime(time.time()))
flag=True
ini_filename='user_config.ini'
color=colors.colors()

conf =configparser.ConfigParser()
conf.readfp(open(ini_filename))
config_dict= dict(conf.items('INI'))

code    = conf.get("INI","code")
start   = conf.get("INI","start")
end     = conf.get("INI","end")

'''
MACD = True if conf.get("INI","MACD")    == 'True'  else  False,
RSI  = True if conf.get("INI","RSI")     == 'True'  else  False,
Kline= True if conf.get("INI","Kline")   == 'True'  else  False,
BULIN= True if conf.get("INI","BULIN")   == 'True'  else  False,
'''


#打印标题 
def print_titel():
    txt='''Python 3.6 Anaconda custom (32-bit)
测试版本 -> 上传GITHUB-wakuang
现在时间 -> %s       '''%(today)
    print (color.Grey(txt))

#打印 config   
def print_config(): #打印 cconfig 信息
    
    print('-'*36)
    print('please check information and run code ')
    print(color.Yellow_nor('$'),'   code     :',color.Purple('%s'%conf.get("INI",'code')))
    print(color.Yellow_nor('$'),'start_time  :',color.Purple('%s'%conf.get("INI",'start')))
    print(color.Yellow_nor('$'),' end_time   :',color.Purple('%s'%conf.get("INI",'end')))
    print("selection the index")
    for key_ , values_ in config_dict.items():
        
        if values_ == 'True':
            
            print('              |- ',key_)
    print('-'*16,color.Blue_nor("MEMU"),'-'*16)
    

def print_section(dict_config):
    for num_c,key_c in enumerate(dict_config.keys()):
        if dict_config[key_c] == 'True':
            print(key_c)
            

def ST_band():
    ti.draw_macd(code,start,end)
    plt.show()
    

def set_index(index):
    get_trp=input(color.Red_nor("是否选择%s,Y/N:"%index)).strip()
    
    if get_trp in ('y','Y','yes') :
        config_dict['%s'%index]='True'
        print(color.Red('++++++++++++已添加 %s\n'%index))
        conf.set('INI','%s'%index,'True')
    elif get_trp in ('n', 'N','no'):
        config_dict["%s"%index]='False'
        print(color.Red('------------已删除 %s\n'%index))
        conf.set('INI','%s'%index,'False')
    else:
        print('quit')
        quit_code(get_trp)
        
    conf.write( open(ini_filename, 'r+') ) 

def set_macd():#设置macd
    set_index('macd')
def set_rsi():#设置RSI
    set_index('rsi')
def set_adx():#设置 adx
    set_index('adx')
def set_bulin():#设置布林线
    set_index('bulin')
def set_kline():#设置 K线
    set_index('kline')
def set_adosc():#设置 adosc
    set_index('adosc')

def set_code():
     get_trp=input(color.Red_nor("输入开始年:")).strip()
     print (get_trp)
def set_startime():
     get_trp=input(color.Red_nor("输入开始年（2000-2020）:")).strip()
     if get_trp<'2020' and get_trp>'2000':
         
         Y = get_trp
     else :
         print ('输入错误，请从新输入')
         set_startime()
     get_trp=input(color.Red_nor("输入开始月（01-12）:")).strip()
     if get_trp<'12' and get_trp>'01':
         
         M = get_trp
     else :
         print ('输入错误，请从新输入')
         set_startime()
     get_trp=input(color.Red_nor("输入开始日(01-31):")).strip()
     if get_trp<'31' and get_trp>'01':
         
         D=get_trp
     else :
         print ('输入错误，请从新输入')
         set_startime()
     time = Y+'-'+ M +'-'+D
     print(time)
    
    
def set_endtime():
    print('set_time2')
      
def running():#开始画图
    code_=conf.get("INI","code")
    start_  = conf.get("INI","start")
    end_    = conf.get("INI","end")
    for key_ , values_ in config_dict.items():
        
        if values_ == 'True':
            print("现在进行构建%s\n"%key_)
            if key_ == 'macd':#run MACD
                ti.draw_macd(code_,start_,end_)
            elif key_ == 'rsi':
               RSI_IDEX = ti.RSI(code_,start_,end_)
               ti.draw_RSI(RSI_IDEX)
            elif key_ == 'adx':
               ADX_IDEX=ti.ADX(code_,start_,end_)
               ti.draw_ADX(ADX_IDEX)
            elif key_ == 'adocs':
                ADOSC_IDEX=ti.ADOSC(code_,start_,end_)
                ti.draw_ADOSC(ADOSC_IDEX)
    plt.show()
          
memu = {    "开始":{
                    '画图':running,
                    },
            '设置index':
                {
                   "布林线":set_bulin,
                   "MACD": set_macd,
                   "RSI强弱":set_rsi,
                   "多空比对":set_adx,
                   "AD Oscillator Chaikin震荡指标":set_adosc,
                   "K线":set_kline
                    
                 },
            "coed/日期":
                {
                    "设置code":set_code,
                    "设置起始时间":set_startime,
                    "设置结束时间":set_endtime,
                        },
            "第二级":
                {
                    "第三级1":"123",
                    "第三级2":"112"
                    },

                   
            }
def quit_code(input_str):
    if input_str== '':
        exit_strip=input(color.Red_nor("按Y退出：")).strip()
        if exit_strip == 'y'or 'Y':
            global flag
            flag = False
            return True
        else:
            return False
        
def go_back(input_str):
    if input_str== '':
        exit_strip=input(color.Red_nor("按Y返回：")).strip()
        if exit_strip == 'y'or 'Y':
            return True
        else:
            return False
def print_memu(memu_):
    for num_,key_ in enumerate(memu_.keys()):
        print (color.Green('----->'),color.Blue_nor(num_),'   ',color.Blue(key_))
        
        
def get_next(memu_,item_):
    item_=int(item_)
    key_=list(memu_.keys())[item_]
    memu_next=memu_['%s'%key_]
    return memu_next,key_



def loop_memu():
    print_titel()
    global flag
    while(flag):
        print_config()
        for num_f,key_f in enumerate(memu.keys()):
            print (color.Green('->'),color.Blue_nor(num_f),'   ',color.Blue(key_f))
            memu_1=memu['%s'%key_f]
            #print(memu_1)
        
        get_trp_1=input(color.Red_nor("请输入一级菜单号,按enter退出：")).strip()
        quit_code(get_trp_1)
        for num_f in enumerate(memu.keys()):
           
            if get_trp_1 == '%s'%num_f[0]:
                memu_1,key=get_next(memu,get_trp_1)
                print_memu(memu_1) 
                len_memu= len(memu_1)
                list_str=['0','1','2','3','4','5','6','7','8','9']
                list_trp=list_str[0:len_memu]
                get_trp_2=input(color.Red_nor("请输入二级菜单号,按enter返回上一级：")).strip()
                if get_trp_2 in list_trp:
                    
                    num_=int(get_trp_2)
                    key_3=list(enumerate(memu_1))[num_][1]
                    print (key_3)
                    memu_1['%s'%key_3]()
                else:
                    
                    go_back(get_trp_2)

                    

            else:
                pass


if __name__=="__main__":
    loop_memu()
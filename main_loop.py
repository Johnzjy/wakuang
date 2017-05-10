# -*- coding: utf-8 -*-
"""
Created on Tue May  2 13:39:17 2017

@author: 310128142
"""
import technical_indicators as ti
import matplotlib.pyplot as plt
from scr import colors
import configparser
import datetime

flag=True
color=colors.colors()
today=datetime.date.today()
def prin_titel():
    txt='''
测试版本-> 上传GITHUB-wakuang
现在时间-> %s        '''%today
    print (color.Grey(txt))

def read_config(ini_key):
    conf =configparser.ConfigParser()
    conf.readfp(open('user_config.ini'))
    ini_str = conf.get("INI","%s"%ini_key)
    return ini_str

def ST_band():
    ti.draw_macd(code_,start_,end_)
    plt.show()

def ACD():
    print ('ACD')
    

def bcd():
    print('hello world')
memu = {
            'IND':
                {
                   "布林线":ST_band,
                   "BCD":bcd,
                   "RSI":"RSI",
                   "OBV":"OBV"
                    
                 },
            "第二级":
                {
                    "第三级1":"123",
                    "第三级2":"112"
                    },
                   
            }
def quit_code(input_str):
    if input_str== '':
        exit_strip=input("按Y退出：").strip()
        if exit_strip == 'y':
            global flag
            flag = False
            return True
        else:
            return False
def go_back(input_str):
    if input_str== '':
        exit_strip=input(color.Red("按Y返回：")).strip()
        if exit_strip == 'y':
            return True
        else:
            pass
def print_memu(memu_):
    for num_,key_ in enumerate(memu_.keys()):
        print ('----->',num_,'   ',key_)
        
        
def get_next(memu_,item_):
    item_=int(item_)
    key_=list(memu_.keys())[item_]
    memu_next=memu_['%s'%key_]
    return memu_next,key_



def loop_memu():
    prin_titel()
    global flag
    while(flag):
        for num_f,key_f in enumerate(memu.keys()):
            print (color.Green('->'),color.Blue(num_f),'   ',color.Blue(key_f))
            memu_1=memu['%s'%key_f]
            #print(memu_1)

        get_trp_1=input(color.Red("请输入一级菜单号,按enter退出：")).strip()
        quit_code(get_trp_1)
        for num_f in enumerate(memu.keys()):
           
            if get_trp_1 == '%s'%num_f[0]:
                memu_1,key=get_next(memu,get_trp_1)
                print_memu(memu_1)                
                get_trp_2=input(color.Red("请输入二级菜单号,按enter返回上一级：")).strip()
                if go_back(get_trp_2)== True:
                    continue
               
                elif get_trp_2 == '0':
                    key_3=list(enumerate(memu_1))[0][1]
                    print (key_3)
                    memu_1['%s'%key_3]()
                    
                    

            else:
                pass


if __name__=="__main__":
    
    code_=read_config('code')
    start_=read_config('start')
    end_=read_config('end')
    loop_memu()
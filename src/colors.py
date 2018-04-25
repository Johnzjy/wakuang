# -*- coding: utf-8 -*-
"""
Created on Mon May  8 12:25:17 2017

@author: 310128142
"""

STYLE = {
        'fore':
        {   # 前景色
            'default'   : '',
            'black'    : 30,   #  黑色
            'red'      : 31,   #  红色
            'green'    : 32,   #  绿色
            'yellow'   : 33,   #  黄色
            'blue'     : 34,   #  蓝色
            'purple'   : 35,   #  紫红色
            'cyan'     : 36,   #  青蓝色
            'white'    : 37,   #  白色
        },

        'back' :
        {   # 背景
            'default'   : '',
            'black'     : 40,  #  黑色
            'red'       : 41,  #  红色
            'green'     : 42,  #  绿色
            'yellow'    : 43,  #  黄色
            'blue'      : 44,  #  蓝色
            'purple'    : 45,  #  紫红色
            'cyan'      : 46,  #  青蓝色
            'white'     : 47,  #  白色
        },

        'mode' :
        {   # 显示模式
            'default'   : '',
            'mormal'    : 0,   #  终端默认设置
            'bold'      : 1,   #  高亮显示
            'underline' : 4,   #  使用下划线
            'blink'     : 5,   #  闪烁
            'invert'    : 7,   #  反白显示
            'hide'      : 8,   #  不可见
        },

        'default' :
        {
            'end' : 0,
        },
}
class colors(object):

    def use_style(self,string, mode='', fore='', back=''):
        mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'].keys() else ''
        fore = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'].keys() else ''
        back = '%s' % STYLE['back'][back] if back in STYLE['back'].keys() else ''
        style = ';'.join([s for s in [mode, fore, back] if s])

        style = '\x1B[%sm' % style if style else ''
        end = '\x1B[%sm' % STYLE['default']['end'] if style else ''
        return '%s%s%s' % (style, string, end)
    def Red(self,string):
        self.out=self.use_style(string, mode='bold',fore="red",back='default')
        return self.out
    def Red_nor(self,string):
        self.out=self.use_style(string, mode='normal',fore="red",back='default')
        return self.out    
    def Yellow(self,string):
        self.out=self.use_style(string, mode='bold',fore="yellow",back='default')
        return self.out
    def Yellow_nor(self,string):
        self.out=self.use_style(string, mode='normal',fore="yellow",back='default')
        return self.out
    def Blue(self,string):
        self.out=self.use_style(string, mode='bold',fore="blue",back='default')
        return self.out
    def Blue_nor(self,string):
        self.out=self.use_style(string, mode='normal',fore="blue",back='default')
        return self.out
    def Cyan(self,string):# 青蓝
        self.out=self.use_style(string, mode='bold',fore="cyan",back='default')
        return self.out
    def Green(self,string):# 青蓝
        self.out=self.use_style(string, mode='bold',fore="green",back='default')
        return self.out
    def Green_inv(self,string):# 青蓝
        self.out=self.use_style(string, mode='invert',fore="green",back='default')
        return self.out
    def Green_ul(self,string):# 青蓝
        self.out=self.use_style(string, mode='underline',fore="green",back='default')
        return self.out
    def Black(self,string):# 黑
        self.out=self.use_style(string, mode='bold',fore="default",back='default')
        return self.out
    def Grey(self,string):# 灰
        self.out=self.use_style(string, mode='bold',fore="black",back='default')
        return self.out
    def Purple(self,string):# 灰
        self.out=self.use_style(string, mode='bold',fore="purple",back='default')
        return self.out
    def War(self,string):
        self.out=self.use_style(string, mode='bold',fore="red",back='yellow')
        return self.out
    def High_BG(self,string):
        self.out=self.use_style(string, mode='bold',fore="blue",back='green')
        return self.out
    def High_YB(self,string):
        self.out=self.use_style(string, mode='bold',fore="blue",back='green')
        return self.out
    def Titel(self,string):
        self.out=self.use_style(string, mode='bold',fore="white",back='black')
        return self.out    
def test():
    col=colors()
    print (col.use_style('正常显示'))
    print ('')

    print ("测试显示模式")
    print (col.use_style('高亮',   mode = 'bold')),
    print (col.use_style('下划线', mode = 'underline'),)

    print (col.use_style('闪烁',   mode = 'blink'),)
    print (col.use_style('反白',   mode = 'invert'),)
    print (col.use_style('不可见', mode = 'hide'))
    print ('')


    print ("测试前景色")
    print (col.use_style('黑色',   fore = 'black'),)
    print (col.use_style('红色',   fore = 'red'),)
    print (col.use_style('绿色',   fore = 'green'),)
    print (col.use_style('黄色',   fore = 'yellow'),)
    print (col.use_style('蓝色',   fore = 'blue'),)
    print (col.use_style('紫红色', fore = 'purple'),)
    print (col.use_style('青蓝色', fore = 'cyan'),)
    print (col.use_style('白色',   fore = 'white'))
    print ('')


    print ("测试背景色")
    print (col.use_style('黑色',   back = 'black'),)
    print (col.use_style('红色',   back = 'red'),)
    print (col.use_style('绿色',   back = 'green'),)
    print (col.use_style('黄色',   back = 'yellow'),)
    print (col.use_style('蓝色',   back = 'blue'),)
    print (col.use_style('紫红色', back = 'purple'),)
    print (col.use_style('青蓝色', back = 'cyan'),)
    print (col.use_style('白色',   back = 'white'))

   
if __name__ == "__main__":
    col=colors()
    for m in STYLE['mode']:
        for b in STYLE['back']:
            for f in STYLE['fore']:
                print(col.use_style("%s-%s-%s"%(m,f,b),mode='%s'%m,back='%s'%b,fore='%s'%f))
                
    print (col.Grey('test'))

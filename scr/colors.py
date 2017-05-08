# -*- coding: utf-8 -*-
"""
Created on Mon May  8 12:25:17 2017

@author: 310128142
"""

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
STYLE = {
        'fore': {
                'black': 30, 'red': 31, 'green': 32, 'yellow': 33,
                'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37,
        },
        'back': {
                'black': 40, 'red': 41, 'green': 42, 'yellow': 43,
                'blue': 44, 'purple': 45, 'cyan': 46, 'white': 47,
        },
        'mode': {
                'bold': 1, 'underline': 4, 'blink': 5, 'invert': 7,
        },
        'default': {
                'end': 0,
        }
}
class colors:
    def use_style(self,string, mode='', fore='', back=''):
        mode = '%s' % STYLE['mode'][mode] if STYLE['mode'].has_key(mode) else ''
        fore = '%s' % STYLE['fore'][fore] if STYLE['fore'].has_key(fore) else ''
        back = '%s' % STYLE['back'][back] if STYLE['back'].has_key(back) else ''
        style = ';'.join([s for s in [mode, fore, back] if s])
        style = '\033[%sm' % style if style else ''
        end = '\033[%sm' % STYLE['default']['end'] if style else ''
        return '%s%s%s' % (style, string, end)
    def Red(self,string_):
        return self.use_style(string_, mode='bold')
if __name__ == "__main__":
    print (colors.Red('BLOD'))
    

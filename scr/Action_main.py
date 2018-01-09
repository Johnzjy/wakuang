# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:18:13 2017

@author: 310128142

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import random


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
try :
    import logd
    LOG= logd.Logger('GUI.log')
except:
    from scr import logd
    LOG= logd.Logger('./scr/GUI.log')

import technical_indicators2 as ti

@LOG.debug_fun
def check_code(code):
    if code == 'sz':
        return code
    elif str(code).isdigit()==True:
        if len(code)== 6:
            
            return code
        else :
            return False
    else:
        return False
    
class PlotCanvas(FigureCanvas):
 
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #fig = Figure(figsize=(width, height), dpi=dpi)
        #super(PlotCanvas,self).__init__()
        
        
        
        fig=Figure()
    
      
        self.index=ti.My_index(self,fig)
        #self.axes = fig.add_subplot(111)
        print(2)
        FigureCanvas.__init__(self, fig)
        print(3)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
 
    @LOG.debug_fun
    def plot(self):

       #ax = self.figure.add_subplot(111)
      
        self.index.draw_macd()

        self.draw()
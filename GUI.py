# -*- coding: utf-8 -*-
"""
Created on Thu May  4 16:04:22 2017

@author: 310128142
"""

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class mywindow(QtWidgets.QWidget): 
    def __init__(self):
        super(mywindow,self).__init__()
        self.initUI()
    def initUI(self):

        self.setGeometry(300, 300, 250, 150)
        
        self.setWindowTitle('挖矿')
        self.setWindowIcon(QtGui.QIcon('ruby.jpg'))        
       # self.
        self.show()
        
def main():

    app = QtWidgets.QApplication(sys.argv)
    widows =mywindow()
    label= QtWidgets.QLabel(widows)
    label.setText("挖矿")
      

    widows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
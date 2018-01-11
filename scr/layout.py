# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from qtpy import QtCore, QtWidgets,QtWidgets,QtGui
from qtpy.QtWebEngineWidgets import QWebEngineView
import time
import os,sys


try :
    import Action_main,logd
    LOG= logd.Logger('GUI.log')
except:
    from scr import Action_main,logd
    LOG= logd.Logger('./scr/GUI.log')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1600,800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        
        self.create_kline_page(MainWindow)
        #self.stacked_layout = QtWidgets.QStackedLayout()
        #self.stacked_layout.addWidget(self.create_kline_page(MainWindow))


    @LOG.debug_fun
    def create_kline_page(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow) #主框
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        #main window
        self.mainLayout=QtWidgets.QGridLayout(self.centralwidget)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.topLayout(self.mainLayout,0,0)
        
        

        
        
        
        self.bottomLayout=QtWidgets.QHBoxLayout() # 底层layout 设置 框 包括gridLayout
        self.bottomLayout.setObjectName(_fromUtf8("bottomLayout"))
        self.mainLayout.addLayout(self.bottomLayout,1,0)
        
        
        self.gridLayout = QtWidgets.QGridLayout()#左侧区域
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)# I have no idea how layouts work
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget) #End Date
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_2.sizePolicy().hasHeightForWidth())
        self.dateEdit_2.setSizePolicy(sizePolicy)
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.gridLayout.addWidget(self.dateEdit_2, 4, 1, 1, 1)
        
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)#Start date
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.gridLayout.addWidget(self.dateEdit, 4, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)  #Shows "enddate"
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget) #Displays stock according to business type
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("历史数据"))
        self.verticalLayout_3.addWidget(self.treeWidget)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 3)
        '''
        设置日期按钮
        '''
        self.DateLinkButton = QtWidgets.QPushButton(self.centralwidget)
        self.DateButtonATT()
        self.gridLayout.addWidget(self.DateLinkButton, 4, 2, 1, 1)
        
        
        self.comboBox = QtWidgets.QComboBox(self.centralwidget) #Combobox for Selecting type of graph
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 3, 2, 1, 1)
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.treeWidget_2.sizePolicy().hasHeightForWidth())
        self.treeWidget_2.setSizePolicy(sizePolicy)#Shows what graphs are selected
        self.treeWidget_2.setObjectName(_fromUtf8("treeWidget_2"))
        self.treeWidget_2.headerItem().setText(0, _fromUtf8("绘图项"))
        self.gridLayout.addWidget(self.treeWidget_2, 5, 0, 1, 3)# 左侧列表 绘图项
        self.gridLayout.setColumnStretch(0, 60)
        self.gridLayout.setColumnStretch(1, 20)
        self.gridLayout.setColumnStretch(2, 20)
        self.bottomLayout.addLayout(self.gridLayout)
        
        
        
        self.verticalLayout = QtWidgets.QGridLayout()#
        self.verticalLayout.setObjectName(_fromUtf8("grph"))
        
        
        
        self.widget = QtWidgets.QGraphicsView(self.centralwidget)#设置输入图画
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))

        
        #self.widget = Action_main.PlotCanvas(self,width=5,hegit=4) #This is for displaying html content generated by pyecharts
       # self.widget = QWebEngineView()#This is for displaying html content generated by pyecharts
        self.verticalLayout.addWidget(self.widget)
        self.bottomLayout.addLayout(self.verticalLayout)
        self.bottomLayout.setStretch(0, 1)
        self.bottomLayout.setStretch(1, 15)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QToolBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #self.menubar.setNativeMenuBar(False)
        self.combobox = QtWidgets.QComboBox()
        self.menubar.addWidget(self.combobox)
        self.combobox.addItems(["K线", "复权", "分笔数据", "历史分钟","十大股东"])
        self.comboBox.setFixedSize(55,40)

        MainWindow.addToolBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    #顶层 layout
    '''
    设置日期按钮属性定义
    '''
    def DateButtonATT(self):
        self.DateLinkButton.setObjectName(_fromUtf8("SetDate"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DateLinkButton.sizePolicy().hasHeightForWidth())
        self.DateLinkButton.setSizePolicy(sizePolicy)
        self.DateLinkButton.setText(_fromUtf8(""))
        self.DateLinkButton.setIcon(QtGui.QIcon(QtGui.QPixmap('scr/ico/date_r.ico')))
        self.DateLinkButton.setFlat(True)
        self.DateLinkButton.setIconSize(QtCore.QSize(20,20))
        
        #self.DateLinkButton.released.connect(self.DateLinkButton.setIcon(QtGui.QIcon(QtGui.QPixmap('scr/ico/date_r.ico'))))
        
    def topLayout(self,layout,x=0,y=0):
        self.topGrid=QtWidgets.QGridLayout()
        self.topGrid.setObjectName(_fromUtf8("topGrid"))
        layout.addLayout(self.topGrid,x,y)
        self.topGrid.setColumnStretch(0, 20)
        self.topGrid.setColumnStretch(1, 20)
        self.topGrid.setColumnStretch(2, 20)
        self.topGrid.setColumnStretch(3, 60)
        self.topGrid.setColumnStretch(4, 20)
        self.topGrid.setColumnStretch(5, 20)
        self.topGrid.setColumnStretch(6, 20)
        self.clockui()
        self.topGrid.setSpacing(2)
        self.topGrid.addWidget(self.lcd,0,6)
        
        self.code_line=self.code_layout('code')
        self.topGrid.addLayout(self.code_line,0,3)

        #self.startButton=QtWidgets.QPushButton('Run')
        #self.topGrid.addWidget(self.startButton,0,0)
        
        self.codelabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.codelabel.sizePolicy().hasHeightForWidth())
        self.codelabel.setSizePolicy(sizePolicy)
        self.codelabel.setObjectName(_fromUtf8("label"))
        self.codelabel.setText(_translate("MainWindow", "上海", None))
        self.topGrid.addWidget(self.codelabel, 0,0)
        
    def code_layout(self,name):
        lineGrid=QtWidgets.QGridLayout()
        
        self.code_edit=QtWidgets.QLineEdit()
        self.code_edit.setPlaceholderText('输入code')
        self.code_edit.setAlignment(QtCore.Qt.AlignCenter)
        lineGrid.addWidget(self.code_edit,0,0)
        self.searchButton=QtWidgets.QPushButton()
   
        self.searchButton.setIcon(QtGui.QIcon(QtGui.QPixmap('scr/ico/search_r.ico')))
        self.searchButton.setFlat(True)

        self.searchButton.setIconSize(QtCore.QSize(20,20))
        #self.searchButton.setStyleSheet("border: 0px")
        lineGrid.addWidget(self.searchButton,0,1)
        return lineGrid
    #设置时钟UI
    def clockui(self):
        self.lcd=QtWidgets.QLCDNumber()
        self.lcd.setDigitCount(10)
        self.lcd.setMode(self.lcd.Dec)
        self.lcd.display(time.strftime("%X",time.localtime()))
        self.timer=QtCore.QTimer()
        self.timer.setInterval(1000)       
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOut)
    #LED aydispl
    def onTimerOut(self):  
        self.lcd.display(time.strftime("%X",time.localtime()))
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("Tuchart", "Tuchart", None))
        self.label.setText(_translate("MainWindow", "Start", None))
        self.label_2.setText(_translate("MainWindow", "End", None))
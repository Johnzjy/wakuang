import sys
from qtpy.QtWidgets import QTreeWidgetItem,QMenu,QApplication,QAction,QMainWindow,QWidget
from qtpy import QtGui,QtWidgets,QtCore
from qtpy.QtCore import Qt,QUrl,QDate
from qtpy.QtWebEngineWidgets import QWebEngineView
import MACD_RUNNING_ALL as ma
import time
import clock
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

class mywindow(QMainWindow): 
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.initUI()
        zsparent = QTreeWidgetItem(self.ui.treeWidget)
        zsparent.setText(0, "股票指数")
        zsnames = ["上证指数-sh", "深圳成指-sz", "沪深300指数-hs300", "上证50-sz50", "中小板-zxb", "创业板-cyb"]
        #股票列表
        for k in zsnames:
            child = QTreeWidgetItem(zsparent)
            child.setText(0, k)
        zsparent2 = QTreeWidgetItem(self.ui.treeWidget)    
        zsparent2.setText(0,"上海")
        shanghai=ma.list_input('sh')
        list_name=list(shanghai.values)
        for code in list_name:
            child = QTreeWidgetItem(zsparent2)
            child.setText(0, '%s %s'%(code[0],code[1]))
            
        #print(shanghai)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.openMenu)

        
    def initUI(self):

        self.show()
        
    def openMenu(self,position):
        indexes = self.ui.treeWidget.selectedIndexes()
        item = self.ui.treeWidget.itemAt(position)


        db_origin = ""
        #if item.parent():
         #   db_origin = item.parent().text(0)
        collec = str(item.text(0).encode("utf-8"))
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level = level + 1
            menu = QMenu()
            #print((collec, db_origin))
            if level ==0:
                pass
            else:
                #keyarray = GetKeys(collec, db_origin)
                #if "Open" in keyarray:
                if self.ui.combobox.currentText()==u"K线":
                    menu.addAction(QAction("Kline", menu, checkable=True))
                    menu.addAction(QAction("Open", menu, checkable=True))
                    menu.addAction(QAction("Close", menu, checkable=True))#open up different menu with different kind of graphs
                    menu.addAction(QAction("High", menu, checkable=True))
                    menu.addAction(QAction("Low", menu, checkable=True))
                    menu.addAction(QAction("Volume", menu, checkable=True))
                    #menu.addAction(QAction("P_change", menu, checkable=True))
                    #menu.addAction(QAction("Turnover",menu,checkable=True))
                if self.ui.combobox.currentText()==u"复权":
                    menu.addAction(QAction("Kline", menu, checkable=True))
                    menu.addAction(QAction("Open", menu, checkable=True))
                    menu.addAction(QAction("Close", menu, checkable=True))
                    menu.addAction(QAction("High", menu, checkable=True))
                    menu.addAction(QAction("Low", menu, checkable=True))
                    menu.addAction(QAction("Volume", menu, checkable=True))
                    menu.addAction(QAction("Amount", menu, checkable=True))
                if self.ui.combobox.currentText()==u"分笔数据":
                    menu.addAction(QAction("分笔", menu, checkable=True))
                if self.ui.combobox.currentText()==u"历史分钟":
                    menu.addAction(QAction("Kline", menu, checkable=True))
                    menu.addAction(QAction("Open", menu, checkable=True))
                    menu.addAction(QAction("Close", menu, checkable=True))
                    menu.addAction(QAction("High", menu, checkable=True))
                    menu.addAction(QAction("Low", menu, checkable=True))
                    menu.addAction(QAction("Volume", menu, checkable=True))
                    menu.addAction(QAction("Amount", menu, checkable=True))
                if self.ui.combobox.currentText()==u"十大股东":
                    menu.addAction(QAction("季度饼图", menu, checkable=True))
                    #menu.addAction(QAction("持股比例", menu, checkable=True))
                #for g in keyarray:
                #menu.addAction(QAction(g, menu, checkable=True))
        menu.triggered.connect(lambda action: self.methodSelected(action, collec))
        menu.exec_(self.ui.treeWidget.viewport().mapToGlobal(position))

#消息窗口
'''
class MessageBox(QtWidgets,QWidget):
    def __init__(self,parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("消息窗口演示程序")
    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self,'确认退出','你确定要退出么？',
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
'''            
        
class Ui_MainWindow(object):
    def setupUi(self,MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowTitle('WAKUANG')
        MainWindow.resize(800, 600) #定义大小
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        
        self.create_kline_page(MainWindow)
        
        
    def create_kline_page(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        self.main_Layout=QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_Layout.setObjectName(_fromUtf8("main_Layout"))
        self.small_layout=QtWidgets.QGridLayout()
        self.small_layout.setObjectName(_fromUtf8("main_Layout"))

        
        
        self.main_Layout.setStretch(0,1)
        self.main_Layout.setStretch(1,1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.main_Layout.addLayout(self.horizontalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1,-1, 0)# 设置contens控件间距 Margins
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
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commandLinkButton.sizePolicy().hasHeightForWidth())
        self.commandLinkButton.setSizePolicy(sizePolicy)
        self.commandLinkButton.setText(_fromUtf8(""))
        self.commandLinkButton.setObjectName(_fromUtf8("commandLinkButton"))
        self.gridLayout.addWidget(self.commandLinkButton, 4, 2, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget) #Combobox for Selecting type of graph
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.gridLayout.addWidget(self.comboBox, 3,2, 1,1)
       
        self.treeWidget_2 = QtWidgets.QTreeWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.treeWidget_2.sizePolicy().hasHeightForWidth())
        self.treeWidget_2.setSizePolicy(sizePolicy)#Shows what graphs are selected
        self.treeWidget_2.setObjectName(_fromUtf8("treeWidget_2"))
        self.treeWidget_2.headerItem().setText(0, _fromUtf8("绘图项"))
        self.gridLayout.addWidget(self.treeWidget_2, 5, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 60)#设置比例
        self.gridLayout.setColumnStretch(1, 20)
        self.gridLayout.setColumnStretch(2, 20)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.widget = QWebEngineView() #This is for displaying html content generated by pyecharts
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 15)
        MainWindow.setCentralWidget(self.centralwidget)
        self.memu_bar(MainWindow)
        self.menubar = QtWidgets.QToolBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        #self.menubar.setNativeMenuBar(False)
        self.combobox = QtWidgets.QComboBox()
        self.menubar.addWidget(self.combobox)
        self.menubar.addAction(self.exitButton)
        self.combobox.addItems(["K线", "复权", "分笔数据", "历史分钟","十大股东"])
        self.comboBox.setFixedSize(55,40)

        MainWindow.addToolBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        

        #self.lcd.setMode(self.lcd.Dec)
        self.clockui(MainWindow)
        self.small_layout.setSpacing(2)
        self.small_layout.addWidget(self.lcd,0,2)
        self.startButton=QtWidgets.QPushButton('Run')
        self.small_layout.addWidget(self.startButton,0,0)
        
    def clockui(self,MainWindow):
        self.lcd=QtWidgets.QLCDNumber()
        self.lcd.setDigitCount(10)
        self.lcd.setMode(self.lcd.Dec)
        self.lcd.display(time.strftime("%X",time.localtime()))
        self.timer=QtCore.QTimer()
        self.timer.setInterval(1000)       
        self.timer.start()
        self.timer.timeout.connect(self.onTimerOut)
    def onTimerOut(self):  
        self.lcd.display(time.strftime("%X",time.localtime()))
    def memu_bar(self,MainWindow):
        self.mainMenu = QMainWindow.menuBar(MainWindow)
        self.mainMenu.setNativeMenuBar(False)
        self.fileMenu = self.mainMenu.addMenu('File')  #建立文件明
        
        self.exitButton = QAction(QtGui.QIcon(), 'Exit', MainWindow)
        self.exitButton.setShortcut('Ctrl+Q')
        self.exitButton.setStatusTip('Exit application')
        #messg=QtWidgets.QMessageBox.question(MainWindow, 'Message', "Do you like Python?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        self.exitButton.triggered.connect(MainWindow.close)#设置退出动作
        #exitButton.triggered.connect(messg)
        
        self.fileMenu.addAction(self.exitButton)
        
        self.saveButton=QAction(QtGui.QIcon(), 'Save', MainWindow)
        self.saveButton.setShortcut('Ctrl+s')
        self.saveButton.setStatusTip('Exit application')
        self.saveButton.triggered.connect(MainWindow.saveGeometry)#设置save动作
        self.fileMenu.addAction(self.saveButton)
      
    def retranslateUi(self, MainWindow):
       # MainWindow.setWindowTitle(_translate("Tuchart", "Tuchart", None))
        self.label.setText(_translate("MainWindow", "Start", None))
        self.label_2.setText(_translate("MainWindow", "End", None))
        
def main():

    app = QtWidgets.QApplication(sys.argv)
    widows =mywindow()
    label= QtWidgets.QLabel(widows)
    label.setText("挖矿")
      

    widows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    print('start')
    main()
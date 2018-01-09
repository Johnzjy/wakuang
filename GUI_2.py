#-*- coding:utf-8 -*-
from __future__ import print_function
import os,sys,sip,time
from datetime import datetime,timedelta
from qtpy.QtWidgets import QTreeWidgetItem,QMenu,QApplication,QAction,QMainWindow
from qtpy import QtGui,QtWidgets,QtCore
from qtpy.QtCore import Qt,QUrl,QDate
from scr import Graph,layout
#from scr.Graph import graphpage
from scr.layout import Ui_MainWindow
from scr import Action_main,logd
from pandas import DataFrame as df
import MACD_RUNNING_ALL as ma
import technical_indicators2 as t2
import pandas as pd
import tushare as ts
import pickle 
import json
list1 = []
LOG= logd.Logger('./scr/GUI.log')

class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        
        curdate = time.strftime("%Y/%m/%d") #gets current time to put into dateedit
        dateobj = datetime.strptime(curdate, "%Y/%m/%d")#converts to datetime object
        past = dateobj - timedelta(days = 7)  #minus a week to start date
        pasttime = datetime.strftime(past, "%Y/%m/%d")
        QPast = QDate.fromString(pasttime,"yyyy/MM/dd") #convert to qtime so that widget accepts the values
        Qcurdate = QDate.fromString(curdate,"yyyy/MM/dd")
        zsparent = QTreeWidgetItem(self.ui.treeWidget)
        zsparent.setText(0, "股票指数")
        zsparent.setIcon(0, QtGui.QIcon('scr/ico/internet.png'))
        zsnames = ["上证指数-sh", "深圳成指-sz", "沪深300指数-hs300", "上证50-sz50", "中小板-zxb", "创业板-cyb"]
        #股票列表
        for k in zsnames:
            child = QTreeWidgetItem(zsparent)
            child.setText(0, k)
        zsparent2 = QTreeWidgetItem(self.ui.treeWidget)    
        zsparent2.setText(0,"上海")
        zsparent2.setIcon(0, QtGui.QIcon('scr/ico/batman.png'))
        
        shanghai=ma.list_input('sh')
        
        list_name=list(shanghai.values)
        for code in list_name:
            child = QTreeWidgetItem(zsparent2)
            child.setText(0, '%s %s'%(code[0],code[1]))
        #   child.doubleClicked.connect(self.code_write(code[0]))
        #self.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.code_write(code[0])) 
            

        zsparent_sz = QTreeWidgetItem(self.ui.treeWidget)    
        zsparent_sz.setText(0,"深圳")
        zsparent_sz.setIcon(0, QtGui.QIcon('scr/ico/greenman.png'))
        
        shanghai=ma.list_input('sz')
        list_name=list(shanghai.values)
        i=0
        for code in list_name:
            i+=1
            child = QTreeWidgetItem(zsparent_sz)
            child.setText(0, '%s %s'%(code[0],code[1]))
            child.setText(1,code[0])
            
        '''
        连接 edit line 和searchButton
        '''
        self.ui.searchButton.clicked.connect(self.run_drawing)
            
        #print(shanghai)
      
        self.ui.treeWidget.itemDoubleClicked.connect(self.DoubleClicked_code_edit)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.openMenu)
   
        '''
        导入graph
        '''
        #引用 T2
        self.K_graph=t2.My_plot()
        #加入列表
        self.ui.verticalLayout.addWidget(self.K_graph.win,0,0,10,10)
        self.K_graph.setCodeDate(code='sh',start='2016-11-01',end='2018-01-08')
        self.K_graph.Kline_plotting()
        self.K_graph.update_plotting()
        self.K_graph.macd_plotting()
        self.K_graph.RSI_plotting()
        '''
        no useful
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "render.html")) #path to read html file
        local_url = QUrl.fromLocalFile(file_path)
        self.ui.widget.load(local_url)
        #self.ui.commandLinkButton.clicked.connect(self.classify)  #when the arrow button is clicked, trigger events
        '''
        self.ui.commandLinkButton.setFixedSize(50, 50)



        #self.ui.commandLinkButton.clicked.connect(lambda action: self.classify(action, self.ui.treewidget))
        #  QSizePolicy
        try:
            retain_size = self.ui.dateEdit_2.sizePolicy()
            retain_size.setRetainSizeWhenHidden(True)
            self.ui.dateEdit_2.setSizePolicy(retain_size)
            retain_size = self.ui.comboBox.sizePolicy()
            retain_size.setRetainSizeWhenHidden(True)
            self.ui.comboBox.setSizePolicy(retain_size)
            retain_size = self.ui.label_2.sizePolicy()
            retain_size.setRetainSizeWhenHidden(True)
            self.ui.label_2.setSizePolicy(retain_size)
        except AttributeError:
            print("No PYQT5 Binding! Widgets might be deformed")



        self.ui.dateEdit.setDate(QPast)
        self.ui.dateEdit_2.setDate(Qcurdate)#populate widgets
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit_2.setCalendarPopup(True)
        self.ui.comboBox.addItems(["D", "W", "M", "5", "15", "30", "60"])
        self.ui.treeWidget_2.setDragDropMode(self.ui.treeWidget_2.InternalMove)
        self.ui.treeWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget_2.customContextMenuRequested.connect(self.openWidgetMenu)
        #self.ui.toolbutton.clicked.connect(lambda action: self.graphmerge(action, CombineKeyword))
        self.ui.combobox.currentIndexChanged.connect(self.modifycombo)
        self.initUI()
    #@LOG.debug_fun
    def run_drawing(self):
        LOG.logger.info('drawing_window for stock')
        code_input=Action_main.check_code(self.ui.code_edit.text())
        
        #code_input=self.ui.code_edit.text()
        print(code_input)
      
        if code_input == False:
            print(code_input)
            self.ui.code_edit.clear()
            self.ui.code_edit.setPlaceholderText('请重新输入code')
        else:

            
            self.K_graph.remove_plot()
            try:
                self.K_graph.setCodeDate(code=code_input,start='2016-11-01',end='2018-01-04')
            except ValueError:
                    print('Input code is wrong/输入代码错误.')
            else:
                self.K_graph.Kline_plotting()
                self.K_graph.update_plotting()
                self.K_graph.macd_plotting()
                self.K_graph.RSI_plotting()
    '''
    动作：双击列表
    reload
    '''    
    def DoubleClicked_code_edit(self):#点击TreeWidget inportCODE bar
        getSelected = self.ui.treeWidget.currentItem().text(0)
        code_select=getSelected[0:6]
        name=getSelected[7:11]# unused
        self.ui.code_edit.setText('%s'%code_select)
      
    
    '''
    输入完成后重新加载图片
    '''
    def reload_graph(self,code_load,start_load,end_load):
        self.K_graph.remove_plot()
        self.K_graph.setCodeDate(code=code_load,start=start_load,end=end_load)
        self.K_graph.Kline_plotting()
        self.K_graph.update_plotting()
        self.K_graph.macd_plotting()
        
    def initUI(self):
        LOG.logger.info('show the UI')
        self.show()
    def modifycombo(self):
        if self.ui.combobox.currentText()==u"复权": #if 复权 is selected, clear all existing queries to avoid value conflict
            self.ui.label_2.show()
            self.ui.dateEdit_2.show()
            self.ui.comboBox.show()
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["hfq", "qfq"])
            self.ui.treeWidget_2.clear()
        if self.ui.combobox.currentText()==u"K线":
            self.ui.label_2.show()
            self.ui.dateEdit_2.show()
            self.ui.comboBox.show()
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["D", "W", "M", "5", "15", "30", "60"])#same as above
            self.ui.treeWidget_2.clear()
        if self.ui.combobox.currentText()==u"分笔数据":
            self.ui.comboBox.hide()
            self.ui.label_2.hide()
            self.ui.dateEdit_2.hide()
            self.ui.treeWidget_2.clear()
        if self.ui.combobox.currentText()==u"历史分钟":
            self.ui.comboBox.show()
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["1min","5min","15min","30min","60min"])
            self.ui.label_2.hide()
            self.ui.dateEdit_2.hide()
            self.ui.treeWidget_2.clear()

        if self.ui.combobox.currentText()==u"十大股东":
            self.ui.comboBox.hide()
            self.ui.label_2.hide()
            self.ui.dateEdit_2.hide()
            self.ui.treeWidget_2.clear()

    def graphmerge(self, combineKeyword):
        sth = ""
        for i in combineKeyword:
            if sth == "":
                sth = sth + i
            else :
                sth = sth + "\n" + "&"+ "-"+i
        list1 = sth
        return sth
        global CombineKeyword
        CombineKeyword = []
        self.ui.listwidget.clear()  #combine stuff so that different graphs can be drawn together

    def kstuff(self):
        return 0


    def openWidgetMenu(self,position):
        indexes = self.ui.treeWidget_2.selectedIndexes()
        item = self.ui.treeWidget_2.itemAt(position)
        if item == None:
            return
        #item = self.ui.listWidget.itemAt(position)
        if len(indexes) > 0:
            menu = QMenu()
            menu.addAction(QAction("Delete", menu,checkable = True))#This function is perhaps useless
            #menu.triggered.connect(self.eraseItem)
            item = self.ui.treeWidget_2.itemAt(position)
            #collec = str(item.text())
            menu.triggered.connect(lambda action: self.ListMethodSelected(action, item))
        menu.exec_(self.ui.treeWidget_2.viewport().mapToGlobal(position))


    def ListMethodSelected(self, action, item):
        if action.text() == "Delete":
            self.eraseItem()
        if action.text() == "Combine":
            global CombineKeyword
            collec = str(item.text())
            CombineKeyword.append(collec)#Useless function(maybe?)
            list1 = [self.tr(collec)]
            self.ui.listwidget.addItems(list1)
            self.eraseItem()


    def methodSelected(self, action, collec):
        #print(action.text()) #Choice
        #if (self.ui.treewidget.count() == 5):
         #   self.ui.label.setText("Maximum number of queries")
         #   return
        #self.ui.label.setText("")
        Choice = action.text()
        Stock = collec
        #print(collec)  #Stock Name
        #print(db_origin)  #DataBase name
        #list1 = [self.tr(Stock+"-"+Choice+"-"+db_origin)]
        #self.ui.treewidget.addItems(list1)
        parent = QTreeWidgetItem(self.ui.treeWidget_2)
        parent.setText(0, Stock.decode("utf-8")+"-"+Choice)
        font = QtGui.QFont("Times", 12, QtGui.QFont.Bold)
        self.ui.treeWidget_2.setFont(font)

    def eraseItem(self):
        for x in self.ui.treeWidget_2.selectedItems():#delete with write click menu
            #item = self.ui.treewidget.takeItem(self.ui.treewidget.currentRow())
            sip.delete(x)
            #item.delete'

            
            
    def classify(self, folder):
        
        items = []
        startdate = self.ui.dateEdit.date()
        startdate = startdate.toPyDate()
        startdate = startdate.strftime("%Y/%m/%d")#converts date from dateedit to tushare readable date
        enddate = self.ui.dateEdit_2.date()
        enddate = enddate.toPyDate()
        enddate = enddate.strftime("%Y/%m/%d")
        option = self.ui.comboBox.currentText()
        print(startdate,enddate,option)
        option = str(option)
        #if (self.ui.treewidget) == 0:
            #self.ui.label.setText("Need to select at least one query")
            #return
        root = self.ui.treeWidget_2.invisibleRootItem()# This is for iterating child items
        child_count = root.childCount()
        if child_count==0:
            return
        for i in range(child_count):
            if root.child(i).child(0):
                array = []
                temp = root.child(i)
                #mergelist = self.recurse(temp,array)
                #print(mergelist)
                parent = root.child(i).text(0)
                mergelist = []
                for j in range(temp.childCount()):
                    while temp.child(j).childCount()!=0:
                        #self.ui.label.setText("Error: Invalid Tree!")
                        return
                    txt = temp.child(j).text(0)
                    mergelist.append(txt)
                mergelist.insert(0,parent)
                url = self.graphmerge(mergelist)
                items.append(url)
            else:
                item = root.child(i)
                url = item.text(0)
                items.append(url)
        labels = [k for k in items]
        items = ([x.encode("utf-8") for x in labels])
        width = self.ui.widget.width()#give width and height of user's screen so that graphs can be generated with dynamic size
        height = self.ui.widget.height()
#        graphpage(labels, startdate,enddate,option,width, height)#labels:复权ork线or分笔 option:hfq, qfq or 15, 30, D, etc
        self.ui.widget.reload()#refreshes webengine
        self.ui.widget.repaint()
        self.ui.widget.update()

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

def main():

    app = QtWidgets.QApplication(sys.argv)
    widows =mywindow()
    label= QtWidgets.QLabel(widows)
    label.setText("挖矿")
      

    widows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    LOG.logger.info('===============  start  ============')
    main()

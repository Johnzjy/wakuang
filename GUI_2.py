#-*- coding:utf-8 -*-
from __future__ import print_function

import json
import os
import pickle
import sys
import time
from datetime import datetime, timedelta

import pandas as pd
import tushare as ts
from pandas import DataFrame as df
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import QDate, Qt, QUrl
from qtpy.QtWidgets import (QAction, QApplication, QMainWindow, QMenu,
                            QTreeWidgetItem)

import MACD_RUNNING_ALL as ma
import sip
import technical_indicators2 as t2
from src import Action_main, Graph, Top10shareholder, layout, logd
#from s.Graph import graphpage
from src.layout import Ui_MainWindow

list1 = []
LOG = logd.Logger('./src/GUI.log')


class mywindow(QMainWindow):
    """Set docstring here.

    Parameters
    ----------
    QMainWindow: 

    Returns
    -------

    """

    def __init__(self):
        super(mywindow, self).__init__()
        self.GraphEnable = True  # 绘图开关
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        curdate = time.strftime(
            "%Y-%m-%d")  #gets current time to put into dateedit
        dateobj = datetime.strptime(curdate,
                                    "%Y-%m-%d")  #converts to datetime object
        past = dateobj - timedelta(days=365)  #minus a week to start date
        pasttime = datetime.strftime(past, "%Y-%m-%d")

        self.QPast = QDate.fromString(
            pasttime,
            "yyyy-MM-dd")  #convert to qtime so that widget accepts the values
        self.Qcurdate = QDate.fromString(curdate, "yyyy-MM-dd")
        self.startdate = pasttime
        self.enddate = curdate

        zsparent = QTreeWidgetItem(self.ui.treeWidget)
        zsparent.setText(0, "index")
        zsparent.setIcon(0, QtGui.QIcon('src/ico/internet.png'))
        zsnames = [
            "上证指数-sh", "深圳成指-sz", "沪深300指数-hs300", "上证50-sz50", "中小板-zxb",
            "创业板-cyb"
        ]
        #股票列表
        for k in zsnames:
            child = QTreeWidgetItem(zsparent)
            child.setText(0, k)
        zsparent2 = QTreeWidgetItem(self.ui.treeWidget)
        zsparent2.setText(0, "SH")
        zsparent2.setIcon(0, QtGui.QIcon('src/ico/batman.png'))

        self.shanghai = ma.list_input('sh')
        #print (self.shanghai)

        list_name = list(self.shanghai.values)
        for code in list_name:
            child = QTreeWidgetItem(zsparent2)
            child.setText(0, '%s %s' % (code[0], code[1]))
        #   child.doubleClicked.connect(self.code_write(code[0]))
        #self.connect(self, QtCore.SIGNAL('itemClicked(QTreeWidgetItem*, int)'), self.code_write(code[0]))

        zsparent_sz = QTreeWidgetItem(self.ui.treeWidget)
        zsparent_sz.setText(0, "SZ")
        zsparent_sz.setIcon(0, QtGui.QIcon('src/ico/greenman.png'))

        self.shenzhen = ma.list_input('sz')
        list_name = list(self.shenzhen.values)
        i = 0
        for code in list_name:
            i += 1
            child = QTreeWidgetItem(zsparent_sz)
            child.setText(0, '%s %s' % (code[0], code[1]))
            child.setText(1, code[0])
        '''
        连接 edit line 和searchButton
        '''
        self.ui.searchButton.clicked.connect(self.ClickedSearchButton)
        self.ui.searchButton.pressed.connect(self.PressSearchButton)
        self.ui.searchButton.released.connect(self.ReleasedSearchButton)

        #print(shanghai)

        self.ui.treeWidget.itemDoubleClicked.connect(
            self.DoubleClicked_code_edit)
        self.ui.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.openMenu)
        '''
        导入graph
        '''
        #引用 T2
        self.GraphInit()
        '''
        self.ui.DateLinkButton 日期设置 
        '''
        self.ui.DateLinkButton.setFixedSize(50, 50)
        self.ui.DateLinkButton.clicked.connect(self.ClickedDateButton)
        self.ui.DateLinkButton.pressed.connect(self.PressDateButton)
        self.ui.DateLinkButton.released.connect(self.ReleasedDateButton)
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

        self.ui.dateEdit.setDate(self.QPast)
        self.ui.dateEdit_2.setDate(self.Qcurdate)  #populate widgets
        self.ui.dateEdit.setCalendarPopup(True)
        self.ui.dateEdit_2.setCalendarPopup(True)
        self.ui.comboBox.addItems(["D", "W", "M", "5", "15", "30", "60"])

        #self.ui.toolbutton.clicked.connect(lambda action: self.graphmerge(action, CombineKeyword))
        self.ui.combobox.currentIndexChanged.connect(self.modifycombo)
        self.initUI()

    #@LOG.debug_fun

    def GraphInit(self):
        self.K_graph = t2.My_plot()
        #加入列表
        self.K_lineTab = self.ui.GraphTab.insertTab(0, self.K_graph.win,
                                                    'graph')
        if self.GraphEnable == True:
            self.ui.pbar.setRange(0, 5)
            self.K_graph.setCodeDate(
                code='sh',
                start='%s' % self.startdate,
                end='%s' % self.enddate)
            self.ui.pbar.setValue(1)
            self.K_graph.Kline_plotting()
            self.ui.pbar.setValue(2)
            self.K_graph.update_plotting()
            self.ui.pbar.setValue(3)
            self.K_graph.macd_plotting()
            self.ui.pbar.setValue(4)
            self.K_graph.RSI_plotting()
            self.ui.pbar.setValue(5)

        else:
            pass
        #self.Top10H=Top10shareholder.Top10Holder
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "src\\Wakuang.html"))

        local_url = QUrl.fromLocalFile(file_path)
        self.ui.webView.load(local_url)

    def ClickedSearchButton(self):
        LOG.logger.info('drawing_window for stock')
        self.ui.pbar.reset()
        code_input = Action_main.check_code(self.ui.code_edit.text())
        #print (code_input)
        self.SetLable(code_input)
        #code_input=self.ui.code_edit.text()

        if code_input == False:
            #print(code_input)
            self.ui.code_edit.clear()
            self.ui.code_edit.setPlaceholderText('请重新输入code')
            pass
        else:

            self.K_graph.remove_plot()
            try:
                self.K_graph.setCodeDate(
                    code=code_input,
                    start='%s' % self.startdate,
                    end='%s' % self.enddate)
            except ValueError:
                print('Input code is wrong/输入代码错误.')
                top10flag = False

            else:
                self.ui.pbar.setRange(0, 5)
                self.K_graph.Kline_plotting()
                self.ui.pbar.setValue(1)
                self.K_graph.update_plotting()
                self.ui.pbar.setValue(2)
                self.K_graph.macd_plotting()
                self.ui.pbar.setValue(3)
                self.K_graph.RSI_plotting()
                self.ui.pbar.setValue(4)
                self.reload_chart()
                self.ui.pbar.setValue(5)
                top10 = Top10shareholder.Top10Holder(code_input,
                                                     self.startdate)
                file_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "src\\top10.html"))
                top10.render(path=file_path)
                top10flag = True

            if top10flag == True:
                file_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "src\\top10.html"))
                local_url = QUrl.fromLocalFile(file_path)
                self.ui.webView.load(local_url)
            else:
                file_path = os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__), "src\\Wakuang.html"))
                local_url = QUrl.fromLocalFile(file_path)
                self.ui.webView.load(local_url)

    def PressSearchButton(self):

        self.ui.searchButton.setIcon(
            QtGui.QIcon(QtGui.QPixmap('src/ico/search_r.ico')))

    def ReleasedSearchButton(self):
        self.ui.searchButton.setIcon(
            QtGui.QIcon(QtGui.QPixmap('src/ico/search_p.ico')))

    '''
    动作：双击列表
    reload
    '''

    def DoubleClicked_code_edit(self):  #点击TreeWidget inportCODE bar
        getSelected = self.ui.treeWidget.currentItem().text(0)
        code_select = getSelected[0:6]
        name = getSelected[7:11]  # unused
        self.ui.code_edit.setText('%s' % code_select)

    ''' 
    输入完成后重新加载图片
    '''

    def reload_chart(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "src\\render.html"))
        print(file_path)
        local_url = QUrl.fromLocalFile(file_path)
        self.ui.webView.load(local_url)
        return

    '''
    没用
    '''

    def reload_graph(self, code_load, start_load, end_load):
        self.K_graph.remove_plot()
        self.K_graph.setCodeDate(
            code=code_load, start=start_load, end=end_load)
        self.K_graph.Kline_plotting()
        self.K_graph.update_plotting()
        self.K_graph.macd_plotting()

    def initUI(self):
        LOG.logger.info('show the UI')
        self.show()

    def modifycombo(self):
        if self.ui.combobox.currentText(
        ) == u"复权":  #if 复权 is selected, clear all existing queries to avoid value conflict
            self.ui.label_2.show()
            self.ui.dateEdit_2.show()
            self.ui.comboBox.show()
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["hfq", "qfq"])

        if self.ui.combobox.currentText() == u"K线":
            self.ui.label_2.show()
            self.ui.dateEdit_2.show()
            self.ui.comboBox.show()
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(["D", "W", "M", "5", "15", "30",
                                       "60"])  #same as above

        if self.ui.combobox.currentText() == u"分笔数据":
            self.ui.comboBox.hide()
            self.ui.label_2.hide()
            self.ui.dateEdit_2.hide()

        if self.ui.combobox.currentText() == u"历史分钟":
            self.ui.comboBox.show()
            self.ui.comboBox.clear()
            self.ui.comboBox.addItems(
                ["1min", "5min", "15min", "30min", "60min"])
            self.ui.label_2.hide()
            self.ui.dateEdit_2.hide()

        if self.ui.combobox.currentText() == u"十大股东":
            self.ui.comboBox.hide()
            self.ui.label_2.hide()
            self.ui.dateEdit_2.hide()

    def graphmerge(self, combineKeyword):
        sth = ""
        for i in combineKeyword:
            if sth == "":
                sth = sth + i
            else:
                sth = sth + "\n" + "&" + "-" + i
        list1 = sth
        return sth
        global CombineKeyword
        CombineKeyword = []
        self.ui.listwidget.clear(
        )  #combine stuff so that different graphs can be drawn together

    def kstuff(self):
        return 0

    def ListMethodSelected(self, action, item):
        if action.text() == "Delete":
            self.eraseItem()
        if action.text() == "Combine":
            global CombineKeyword
            collec = str(item.text())
            CombineKeyword.append(collec)  #Useless function(maybe?)
            list1 = [self.tr(collec)]
            self.ui.listwidget.addItems(list1)
            self.eraseItem()

    def SetLable(self, code_in):

        list_name = list(self.shanghai.values)
        for code in list_name:
            if code_in == code[0]:
                self.ui.codelabel.setText('上海 %s %s' % (code[0], code[1]))
                return
            else:
                pass
        list_name = list(self.shenzhen.values)
        for code in list_name:
            if code_in == code[0]:
                self.ui.codelabel.setText('深圳 %s %s' % (code[0], code[1]))
                return
            else:
                pass
        self.ui.codelabel.setText(code_in)

    def ClickedDateButton(self):  #设置日期
        self.startdate = self.ui.dateEdit.date()
        self.startdate = self.startdate.toPyDate()
        self.startdate = self.startdate.strftime(
            "%Y-%m-%d")  #converts date from dateedit to tushare readable date
        self.enddate = self.ui.dateEdit_2.date()
        self.enddate = self.enddate.toPyDate()
        self.enddate = self.enddate.strftime("%Y-%m-%d")

    def PressDateButton(self):
        self.ui.DateLinkButton.setIcon(
            QtGui.QIcon(QtGui.QPixmap('src/ico/date_p.ico')))

    def ReleasedDateButton(self):
        self.ui.DateLinkButton.setIcon(
            QtGui.QIcon(QtGui.QPixmap('src/ico/date_r.ico')))

    def openMenu(self, position):
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
            if level == 0:
                pass
            else:
                #keyarray = GetKeys(collec, db_origin)
                #if "Open" in keyarray:
                if self.ui.combobox.currentText() == u"K线":
                    menu.addAction(QAction("Kline", menu, checkable=True))
                    menu.addAction(QAction("Open", menu, checkable=True))
                    menu.addAction(
                        QAction("Close", menu, checkable=True)
                    )  #open up different menu with different kind of graphs
                    menu.addAction(QAction("High", menu, checkable=True))
                    menu.addAction(QAction("Low", menu, checkable=True))
                    menu.addAction(QAction("Volume", menu, checkable=True))
                    #menu.addAction(QAction("P_change", menu, checkable=True))
                    #menu.addAction(QAction("Turnover",menu,checkable=True))
                if self.ui.combobox.currentText() == u"复权":
                    menu.addAction(QAction("Kline", menu, checkable=True))
                    menu.addAction(QAction("Open", menu, checkable=True))
                    menu.addAction(QAction("Close", menu, checkable=True))
                    menu.addAction(QAction("High", menu, checkable=True))
                    menu.addAction(QAction("Low", menu, checkable=True))
                    menu.addAction(QAction("Volume", menu, checkable=True))
                    menu.addAction(QAction("Amount", menu, checkable=True))
                if self.ui.combobox.currentText() == u"分笔数据":
                    menu.addAction(QAction("分笔", menu, checkable=True))
                if self.ui.combobox.currentText() == u"历史分钟":
                    menu.addAction(QAction("Kline", menu, checkable=True))
                    menu.addAction(QAction("Open", menu, checkable=True))
                    menu.addAction(QAction("Close", menu, checkable=True))
                    menu.addAction(QAction("High", menu, checkable=True))
                    menu.addAction(QAction("Low", menu, checkable=True))
                    menu.addAction(QAction("Volume", menu, checkable=True))
                    menu.addAction(QAction("Amount", menu, checkable=True))
                if self.ui.combobox.currentText() == u"十大股东":
                    menu.addAction(QAction("季度饼图", menu, checkable=True))
                    #menu.addAction(QAction("持股比例", menu, checkable=True))
                #for g in keyarray:
                #menu.addAction(QAction(g, menu, checkable=True))
        menu.triggered.connect(
            lambda action: self.methodSelected(action, collec))
        menu.exec_(self.ui.treeWidget.viewport().mapToGlobal(position))


def main():

    app = QtWidgets.QApplication(sys.argv)
    widows = mywindow()
    label = QtWidgets.QLabel(widows)
    label.setText("挖矿")

    widows.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    LOG.logger.info('===============  start  ============')
    main()

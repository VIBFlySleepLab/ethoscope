# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created: Thu Jul 24 10:14:55 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(523, 417)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtGui.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(240, 20, 121, 41))
        self.loadButton.setObjectName("loadButton")
        self.ipEdit = QtGui.QLineEdit(self.centralwidget)
        self.ipEdit.setGeometry(QtCore.QRect(10, 30, 61, 31))
        self.ipEdit.setPlaceholderText("")
        self.ipEdit.setObjectName("ipEdit")
        self.ipEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.ipEdit_2.setGeometry(QtCore.QRect(80, 30, 61, 31))
        self.ipEdit_2.setObjectName("ipEdit_2")
        self.ipEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.ipEdit_3.setGeometry(QtCore.QRect(150, 30, 61, 31))
        self.ipEdit_3.setObjectName("ipEdit_3")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 30, 31, 41))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 30, 21, 41))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 131, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(220, 36, 55, 21))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(210, 30, 21, 41))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(18)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 110, 491, 261))
        self.listWidget.setObjectName("listWidget")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(370, 30, 111, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.downloadcheckBox = QtGui.QCheckBox(self.centralwidget)
        self.downloadcheckBox.setGeometry(QtCore.QRect(20, 70, 271, 21))
        self.downloadcheckBox.setObjectName("downloadcheckBox")
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(380, 30, 81, 19))
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(99)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(380, 10, 91, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(470, 30, 16, 17))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(370, 30, 16, 20))
        font = QtGui.QFont()
        font.setFamily("Sans")
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 523, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.loadButton.setText(QtGui.QApplication.translate("MainWindow", "Discover Sleeps", None, QtGui.QApplication.UnicodeUTF8))
        self.ipEdit.setText(QtGui.QApplication.translate("MainWindow", "192", None, QtGui.QApplication.UnicodeUTF8))
        self.ipEdit_2.setText(QtGui.QApplication.translate("MainWindow", "168", None, QtGui.QApplication.UnicodeUTF8))
        self.ipEdit_3.setText(QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Direccion Red local ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadcheckBox.setText(QtGui.QApplication.translate("MainWindow", "Save data in this computer automatically ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Scanner Speed", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "-", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\count_parts.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(237, 106)
        self.countParts = QtWidgets.QSpinBox(Dialog)
        self.countParts.setGeometry(QtCore.QRect(110, 20, 111, 22))
        self.countParts.setMinimum(1)
        self.countParts.setMaximum(100000)
        self.countParts.setProperty("value", 1)
        self.countParts.setDisplayIntegerBase(10)
        self.countParts.setObjectName("countParts")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(70, 60, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_2.setText(_translate("Dialog", "Взять"))
        self.pushButton.setText(_translate("Dialog", "Oк"))

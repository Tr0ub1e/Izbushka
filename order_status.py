# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\order_status.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1120, 336)
        self.label_13 = QtWidgets.QLabel(Dialog)
        self.label_13.setGeometry(QtCore.QRect(20, 80, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.milliageEdit = QtWidgets.QLineEdit(Dialog)
        self.milliageEdit.setGeometry(QtCore.QRect(20, 100, 191, 22))
        self.milliageEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.milliageEdit.setMaxLength(1000000)
        self.milliageEdit.setReadOnly(True)
        self.milliageEdit.setObjectName("milliageEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 55, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_14 = QtWidgets.QLabel(Dialog)
        self.label_14.setGeometry(QtCore.QRect(20, 190, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(200, 20, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(250, 80, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.vincodeEdit = QtWidgets.QLineEdit(Dialog)
        self.vincodeEdit.setGeometry(QtCore.QRect(20, 160, 331, 22))
        self.vincodeEdit.setReadOnly(True)
        self.vincodeEdit.setObjectName("vincodeEdit")
        self.numberEdit = QtWidgets.QLineEdit(Dialog)
        self.numberEdit.setGeometry(QtCore.QRect(250, 100, 101, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.numberEdit.setFont(font)
        self.numberEdit.setMaxLength(8)
        self.numberEdit.setReadOnly(True)
        self.numberEdit.setObjectName("numberEdit")
        self.engineEdit = QtWidgets.QLineEdit(Dialog)
        self.engineEdit.setGeometry(QtCore.QRect(20, 220, 331, 22))
        self.engineEdit.setReadOnly(True)
        self.engineEdit.setObjectName("engineEdit")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(20, 130, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.markEdit = QtWidgets.QLineEdit(Dialog)
        self.markEdit.setGeometry(QtCore.QRect(20, 50, 151, 22))
        self.markEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.markEdit.setMaxLength(1000000)
        self.markEdit.setReadOnly(True)
        self.markEdit.setObjectName("markEdit")
        self.modelEdit = QtWidgets.QLineEdit(Dialog)
        self.modelEdit.setGeometry(QtCore.QRect(200, 50, 151, 22))
        self.modelEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.modelEdit.setMaxLength(1000000)
        self.modelEdit.setReadOnly(True)
        self.modelEdit.setObjectName("modelEdit")
        self.chosedUsluga = QtWidgets.QTableWidget(Dialog)
        self.chosedUsluga.setGeometry(QtCore.QRect(370, 10, 741, 311))
        self.chosedUsluga.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.chosedUsluga.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.chosedUsluga.setObjectName("chosedUsluga")
        self.chosedUsluga.setColumnCount(3)
        self.chosedUsluga.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.chosedUsluga.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.chosedUsluga.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.chosedUsluga.setHorizontalHeaderItem(2, item)
        self.chosedUsluga.horizontalHeader().setDefaultSectionSize(280)
        self.chosedUsluga.horizontalHeader().setStretchLastSection(False)
        self.chosedUsluga.verticalHeader().setStretchLastSection(False)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 260, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit.setGeometry(QtCore.QRect(160, 260, 194, 22))
        self.dateTimeEdit.setReadOnly(True)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.delZakaz = QtWidgets.QPushButton(Dialog)
        self.delZakaz.setGeometry(QtCore.QRect(220, 300, 93, 28))
        self.delZakaz.setCheckable(False)
        self.delZakaz.setDefault(False)
        self.delZakaz.setFlat(False)
        self.delZakaz.setObjectName("delZakaz")
        self.finishZak = QtWidgets.QPushButton(Dialog)
        self.finishZak.setGeometry(QtCore.QRect(50, 300, 93, 28))
        self.finishZak.setObjectName("finishZak")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Статус заказа"))
        self.label_13.setText(_translate("Dialog", "Пробег"))
        self.label.setText(_translate("Dialog", "Марка"))
        self.label_14.setText(_translate("Dialog", "Номер двигателя"))
        self.label_2.setText(_translate("Dialog", "Модель"))
        self.label_6.setText(_translate("Dialog", "Гос номер"))
        self.numberEdit.setPlaceholderText(_translate("Dialog", "AA####AA"))
        self.label_12.setText(_translate("Dialog", "VIN код"))
        item = self.chosedUsluga.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Услуга"))
        item = self.chosedUsluga.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Деталь"))
        item = self.chosedUsluga.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Статус"))
        self.label_3.setText(_translate("Dialog", "Дата окончания"))
        self.delZakaz.setText(_translate("Dialog", "Удалить заказ"))
        self.finishZak.setText(_translate("Dialog", "Закончить"))

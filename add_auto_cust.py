# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\add_auto_cust.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(882, 394)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 55, 16))
        self.label_2.setObjectName("label_2")
        self.markAuto = QtWidgets.QComboBox(Dialog)
        self.markAuto.setGeometry(QtCore.QRect(20, 40, 131, 22))
        self.markAuto.setObjectName("markAuto")
        self.modelAuto = QtWidgets.QComboBox(Dialog)
        self.modelAuto.setGeometry(QtCore.QRect(170, 40, 131, 22))
        self.modelAuto.setObjectName("modelAuto")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 100, 131, 22))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(20, 280, 55, 22))
        self.label_5.setObjectName("label_5")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(120, 350, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.numberEdit = QtWidgets.QLineEdit(Dialog)
        self.numberEdit.setGeometry(QtCore.QRect(170, 100, 131, 22))
        self.numberEdit.setObjectName("numberEdit")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(170, 80, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(20, 160, 131, 22))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(20, 220, 131, 22))
        self.label_8.setObjectName("label_8")
        self.famEdit = QtWidgets.QLineEdit(Dialog)
        self.famEdit.setGeometry(QtCore.QRect(20, 130, 291, 22))
        self.famEdit.setReadOnly(True)
        self.famEdit.setObjectName("famEdit")
        self.nameEdit = QtWidgets.QLineEdit(Dialog)
        self.nameEdit.setGeometry(QtCore.QRect(20, 190, 291, 22))
        self.nameEdit.setReadOnly(True)
        self.nameEdit.setObjectName("nameEdit")
        self.fathEdit = QtWidgets.QLineEdit(Dialog)
        self.fathEdit.setGeometry(QtCore.QRect(20, 250, 291, 22))
        self.fathEdit.setReadOnly(True)
        self.fathEdit.setObjectName("fathEdit")
        self.phoneEdit = QtWidgets.QLineEdit(Dialog)
        self.phoneEdit.setGeometry(QtCore.QRect(20, 310, 291, 22))
        self.phoneEdit.setReadOnly(True)
        self.phoneEdit.setObjectName("phoneEdit")
        self.ableUsluga = QtWidgets.QTableWidget(Dialog)
        self.ableUsluga.setGeometry(QtCore.QRect(320, 20, 256, 351))
        self.ableUsluga.setObjectName("ableUsluga")
        self.ableUsluga.setColumnCount(1)
        self.ableUsluga.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ableUsluga.setHorizontalHeaderItem(0, item)
        self.ableUsluga.horizontalHeader().setStretchLastSection(True)
        self.ableUsluga.verticalHeader().setStretchLastSection(False)
        self.addUsluga = QtWidgets.QPushButton(Dialog)
        self.addUsluga.setGeometry(QtCore.QRect(580, 110, 31, 28))
        self.addUsluga.setObjectName("addUsluga")
        self.delUsluga = QtWidgets.QPushButton(Dialog)
        self.delUsluga.setGeometry(QtCore.QRect(580, 170, 31, 28))
        self.delUsluga.setObjectName("delUsluga")
        self.chosedUsluga = QtWidgets.QTableWidget(Dialog)
        self.chosedUsluga.setGeometry(QtCore.QRect(620, 20, 256, 351))
        self.chosedUsluga.setObjectName("chosedUsluga")
        self.chosedUsluga.setColumnCount(1)
        self.chosedUsluga.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.chosedUsluga.setHorizontalHeaderItem(0, item)
        self.chosedUsluga.horizontalHeader().setStretchLastSection(True)
        self.chosedUsluga.verticalHeader().setStretchLastSection(False)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Марка"))
        self.label_2.setText(_translate("Dialog", "Модель"))
        self.label_4.setText(_translate("Dialog", "Фамилия клиента"))
        self.label_5.setText(_translate("Dialog", "Телефон"))
        self.pushButton.setText(_translate("Dialog", "Добавить"))
        self.numberEdit.setPlaceholderText(_translate("Dialog", "AA####AA"))
        self.label_6.setText(_translate("Dialog", "Гос номер"))
        self.label_7.setText(_translate("Dialog", "Имя клиента"))
        self.label_8.setText(_translate("Dialog", "Отчество клиента"))
        item = self.ableUsluga.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Доступные услуги"))
        self.addUsluga.setText(_translate("Dialog", ">>"))
        self.delUsluga.setText(_translate("Dialog", "<<"))
        item = self.chosedUsluga.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Выбранные услуги"))

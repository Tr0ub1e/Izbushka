# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\add_employee.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(311, 371)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(100, 330, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 261, 16))
        self.label.setObjectName("label")
        self.dateEdit = QtWidgets.QDateEdit(Dialog)
        self.dateEdit.setGeometry(QtCore.QRect(190, 250, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 250, 161, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 180, 55, 21))
        self.label_3.setObjectName("label_3")
        self.moneyEdit = QtWidgets.QLineEdit(Dialog)
        self.moneyEdit.setGeometry(QtCore.QRect(70, 180, 231, 22))
        self.moneyEdit.setInputMask("")
        self.moneyEdit.setText("")
        self.moneyEdit.setMaxLength(32767)
        self.moneyEdit.setObjectName("moneyEdit")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 290, 101, 21))
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(170, 290, 131, 22))
        self.comboBox.setObjectName("comboBox")
        self.famEdit = QtWidgets.QLineEdit(Dialog)
        self.famEdit.setGeometry(QtCore.QRect(10, 40, 291, 22))
        self.famEdit.setObjectName("famEdit")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 261, 16))
        self.label_5.setObjectName("label_5")
        self.nameEdit = QtWidgets.QLineEdit(Dialog)
        self.nameEdit.setGeometry(QtCore.QRect(10, 90, 291, 22))
        self.nameEdit.setObjectName("nameEdit")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 120, 261, 16))
        self.label_6.setObjectName("label_6")
        self.fathEdit = QtWidgets.QLineEdit(Dialog)
        self.fathEdit.setGeometry(QtCore.QRect(10, 140, 291, 22))
        self.fathEdit.setObjectName("fathEdit")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 210, 61, 21))
        self.label_7.setObjectName("label_7")
        self.phoneEdit = QtWidgets.QLineEdit(Dialog)
        self.phoneEdit.setGeometry(QtCore.QRect(70, 210, 231, 22))
        self.phoneEdit.setInputMask("")
        self.phoneEdit.setText("")
        self.phoneEdit.setMaxLength(32767)
        self.phoneEdit.setObjectName("phoneEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Добавить"))
        self.label.setText(_translate("Dialog", "Фамилия"))
        self.label_2.setText(_translate("Dialog", "Дата приема"))
        self.label_3.setText(_translate("Dialog", "Ставка"))
        self.label_4.setText(_translate("Dialog", "Специализация"))
        self.label_5.setText(_translate("Dialog", "Имя"))
        self.label_6.setText(_translate("Dialog", "Отчество"))
        self.label_7.setText(_translate("Dialog", "Телефон"))

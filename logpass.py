# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\logpass.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(218, 158)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\\favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.login = QtWidgets.QLineEdit(Dialog)
        self.login.setObjectName("login")
        self.verticalLayout.addWidget(self.login)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pwd = QtWidgets.QLineEdit(Dialog)
        self.pwd.setObjectName("pwd")
        self.verticalLayout.addWidget(self.pwd)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Соединение"))
        self.label_2.setText(_translate("Dialog", "Логин"))
        self.label.setText(_translate("Dialog", "Пароль"))
        self.pushButton.setText(_translate("Dialog", "Подключиться"))

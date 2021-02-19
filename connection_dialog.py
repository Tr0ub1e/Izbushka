from PyQt5 import QtWidgets, QtGui
from logpass import Ui_Dialog
from db_tools import autowork_db

class ConDial(QtWidgets.QDialog):

    def __init__(self):
        super(ConDial, self).__init__()

        self.db = autowork_db()
        self.con, self.cursor = None, None

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.dial_ui.pushButton.clicked.connect(self.mainDial)

        self.dial.exec_()

    def access_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Вход выполнен успешно!")
        msg.setWindowTitle("Вход")
        msg.exec_()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка входа")
        msg.setInformativeText('Неправильный логин/пароль')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

    def mainDial(self):

        user = self.dial_ui.login.text()
        pwd = self.dial_ui.pwd.text()

        try:
            return self.db.make_con(user, pwd)

        finally:
            self.dial.close()

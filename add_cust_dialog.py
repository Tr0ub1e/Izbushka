from add_cust import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from db_tools import autowork_db


class CustDial(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(CustDial, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)
        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def insert_data(self):

        try:
            fio = self.dial_ui.fioEdit.text()
            phone = self.dial_ui.phoneEdit.text()

            self.db.insert_customers(fio, phone)

        except Exception as e:
            print(e)

        finally:
            self.dial.close()

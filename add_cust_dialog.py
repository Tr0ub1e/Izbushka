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
            fam = self.dial_ui.famEdit.text()
            name = self.dial_ui.nameEdit.text()
            fath = self.dial_ui.fathEdit.text()
            phone = self.dial_ui.phoneEdit.text()

            try:
                phone = int(phone)
            except:
                raise

            _ = fam + " " +name+ " " + fath

            self.db.insert_customers(_, phone)

        except:
            self.error_msg()

        finally:
            self.dial.close()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

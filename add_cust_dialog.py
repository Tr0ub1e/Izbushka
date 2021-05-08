from add_cust import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from db_tools import autowork_db


class CustDial(QtWidgets.QDialog):

    def __init__(self, con, cur, type_, up_st=()):
        super(CustDial, self).__init__()

        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        if type_ == "insert":
            self.dial_ui.pushButton.clicked.connect(self.insert_data)

        if type_ == "update":
            self.fill_data(up_st)

            self.fio, self.phone = self.get_form_data()

            self.dial_ui.pushButton.clicked.connect(self.update_data)

        self.exec_()

    def insert_data(self):

        try:
            fio, phone = self.get_form_data()
            self.db.insert_customers(fio, phone)

        except:
            self.error_msg()

        finally:
            self.close()

    def get_form_data(self):

        fam = self.dial_ui.famEdit.text()
        name = self.dial_ui.nameEdit.text()
        fath = self.dial_ui.fathEdit.text()
        phone = self.dial_ui.phoneEdit.text()

        _ = fam + " " +name+ " " + fath

        try:
            phone = int(phone)
        except:
            raise

        return _, phone

    def fill_data(self, up_st):

        self.id_cust = up_st[0]

        fam, name, fath = up_st[1].split(' ')

        self.dial_ui.famEdit.setText(fam)
        self.dial_ui.nameEdit.setText(name)
        self.dial_ui.fathEdit.setText(fath)
        self.dial_ui.phoneEdit.setText(up_st[2])

    def update_data(self):

        fam = self.dial_ui.famEdit.text()
        name = self.dial_ui.nameEdit.text()
        fath = self.dial_ui.fathEdit.text()
        phone = self.dial_ui.phoneEdit.text()

        _ = fam + " " +name+ " " + fath

        data = {}

        if self.fio != _:
            data['fio'] = _

        if self.phone != phone:
            data['phone'] = phone

        self.db.update_customers(self.id_cust, data)

        self.close()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

from add_employee import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from db_tools import autowork_db

class EmpDial(QtWidgets.QDialog):

    def __init__(self, specs, con, cur):
        super(EmpDial, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_box(specs)

        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def fill_box(self, items):

        for id_spec, name_spec in items:
            self.dial_ui.comboBox.addItem(str(name_spec))

    def insert_data(self):

        try:
            fio = self.dial_ui.lineEdit.text()
            rental_date = self.dial_ui.dateEdit.date()
            rate = self.dial_ui.lineEdit_2.text()
            spec = self.dial_ui.comboBox.currentText()

            self.db.insert_employees(fio, rental_date, rate, spec)

        except Exception as e:
            print(self.__class__.__name__, e)

        finally:
            self.dial.close()

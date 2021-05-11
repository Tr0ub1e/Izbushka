from PyQt5 import QtWidgets
from usluga_table import Ui_Dialog
from db_tools import autowork_db

class Usluga(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(Usluga, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.fill_data()

        self.exec_()

    def fill_data(self):

        self.dial_ui.tableWidget.setRowCount(len(self.db.get_uslugi()))

        for i, items in enumerate(self.db.get_uslugi()):


            name_serv = QtWidgets.QTableWidgetItem(items[1])
            price = QtWidgets.QTableWidgetItem(str(items[2]))
            duration = QtWidgets.QTableWidgetItem(str(items[3]))

            self.dial_ui.tableWidget.setItem(i, 0, name_serv)
            self.dial_ui.tableWidget.setItem(i, 1, price)
            self.dial_ui.tableWidget.setItem(i, 2, duration)

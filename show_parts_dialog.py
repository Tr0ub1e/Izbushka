from PyQt5 import QtWidgets
from usluga_table import Ui_Dialog
from db_tools import autowork_db

class Parts(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(Parts, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        headers = ('Марка', 'Модель', 'Название', 'Цена', 'Кол-во')
        self.setWindowTitle('Доступные запчасти')

        self.dial_ui.tableWidget.setColumnCount(5)

        for i, head in enumerate(headers):
            item = QtWidgets.QTableWidgetItem(head)
            self.dial_ui.tableWidget.setHorizontalHeaderItem(i, item)

        self.fill_data()

        self.exec_()

    def fill_data(self):

        self.dial_ui.tableWidget.setRowCount(len(self.db.get_zapchasti()))

        for i, items in enumerate(self.db.get_zapchasti()):

            mark = QtWidgets.QTableWidgetItem(items[-2])
            model = QtWidgets.QTableWidgetItem(items[-1])
            kol_vo = QtWidgets.QTableWidgetItem(str(items[2]))
            name_zap = QtWidgets.QTableWidgetItem(items[3])
            cost = QtWidgets.QTableWidgetItem(str(items[4]))

            self.dial_ui.tableWidget.setItem(i, 0, mark)
            self.dial_ui.tableWidget.setItem(i, 1, model)
            self.dial_ui.tableWidget.setItem(i, 2, name_zap)
            self.dial_ui.tableWidget.setItem(i, 3, cost)
            self.dial_ui.tableWidget.setItem(i, 4, kol_vo)

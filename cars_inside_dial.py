from PyQt5 import QtWidgets
from usluga_table import Ui_Dialog
from db_tools import autowork_db

class Cars(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(Cars, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        headers = ('Марка', 'Модель', 'Гос номер')
        self.setWindowTitle('Автомобили в сервисе')

        for i, head in enumerate(headers):
            self.dial_ui.tableWidget.horizontalHeaderItem(i).setText(head)

        self.fill_data()

        self.exec_()

    def fill_data(self):

        self.dial_ui.tableWidget.setRowCount(len(self.db.get_cars()))

        for i, items in enumerate(self.db.get_cars()):

            mark = QtWidgets.QTableWidgetItem(items[0])
            model = QtWidgets.QTableWidgetItem(str(items[1]))
            gov_number = QtWidgets.QTableWidgetItem(str(items[2]))

            self.dial_ui.tableWidget.setItem(i, 0, mark)
            self.dial_ui.tableWidget.setItem(i, 1, model)
            self.dial_ui.tableWidget.setItem(i, 2, gov_number)

from PyQt5 import QtWidgets
from empl_history import Ui_Dialog
from db_tools import autowork_db

class ArchCust(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(ArchCust, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        headers = ('Код', "ФИО", "Телефон", "Кол-во заказов", "Статус",
                                "Дата записи")

        self.dial_ui.tableWidget.setColumnCount(len(headers))

        for i, head in enumerate(headers):
            item = QtWidgets.QTableWidgetItem(head)
            self.dial_ui.tableWidget.setHorizontalHeaderItem(i, item)

        self.fill_data()

        self.dial_ui.pushButton.clicked.connect(self.upd_data)
        self.exec_()

    def fill_data(self):

        self.dial_ui.tableWidget.setRowCount(len(self.db.show_cust_arch()))

        for i, items in enumerate(self.db.show_cust_arch()):

            id_cust = QtWidgets.QTableWidgetItem(str(items[0]))
            phone = QtWidgets.QTableWidgetItem(str(items[1]))
            fio = QtWidgets.QTableWidgetItem(str(items[2]))
            order_count = QtWidgets.QTableWidgetItem(str(items[3]))
            arch_date = QtWidgets.QTableWidgetItem(str(items[5]))
            arch_status = QtWidgets.QTableWidgetItem(str(items[6]))

            self.dial_ui.tableWidget.setItem(i, 0, id_cust)
            self.dial_ui.tableWidget.setItem(i, 1, fio)
            self.dial_ui.tableWidget.setItem(i, 2, phone)
            self.dial_ui.tableWidget.setItem(i, 3, order_count)
            self.dial_ui.tableWidget.setItem(i, 4, arch_date)
            self.dial_ui.tableWidget.setItem(i, 5, arch_status)

    def upd_data(self):
        start = self.dial_ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        stop = self.dial_ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")

        self.dial_ui.tableWidget.setRowCount(len(self.db.show_cust_arch(start, stop)))

        for i, items in enumerate(self.db.show_cust_arch(start, stop)):

            id_cust = QtWidgets.QTableWidgetItem(str(items[0]))
            phone = QtWidgets.QTableWidgetItem(str(items[1]))
            fio = QtWidgets.QTableWidgetItem(str(items[2]))
            order_count = QtWidgets.QTableWidgetItem(str(items[3]))
            arch_date = QtWidgets.QTableWidgetItem(str(items[5]))
            arch_status = QtWidgets.QTableWidgetItem(str(items[6]))

            self.dial_ui.tableWidget.setItem(i, 0, id_cust)
            self.dial_ui.tableWidget.setItem(i, 1, fio)
            self.dial_ui.tableWidget.setItem(i, 2, phone)
            self.dial_ui.tableWidget.setItem(i, 3, order_count)
            self.dial_ui.tableWidget.setItem(i, 4, arch_date)
            self.dial_ui.tableWidget.setItem(i, 5, arch_status)

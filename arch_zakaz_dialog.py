from PyQt5 import QtWidgets
from arch_zakaz import Ui_Dialog
from db_tools import autowork_db

class ArchZakaz(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(ArchZakaz, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        headers = ('Код заказа', "Гос номер", "Статус", "Дата записи")
        headers_2 = ('Услуга', "Запчасть", "Статус", "Дата записи")

        self.dial_ui.zakazTable.setColumnCount(len(headers))

        for i, head in enumerate(headers):
            item = QtWidgets.QTableWidgetItem(head)
            self.dial_ui.zakazTable.setHorizontalHeaderItem(i, item)

        self.dial_ui.uslugaTable.setColumnCount(len(headers_2))

        for i, head in enumerate(headers_2):
            item = QtWidgets.QTableWidgetItem(head)
            self.dial_ui.uslugaTable.setHorizontalHeaderItem(i, item)

        self.fill_data()

        self.dial_ui.pushButton.clicked.connect(self.upd_data)
        self.dial_ui.zakazTable.cellClicked.connect(self.foo)

        self.exec_()

    def foo(self):
        id_z = int(self.dial_ui.zakazTable.item(self.dial_ui.zakazTable.currentRow(), 0).text())

        self.info_(id_z)
        self.arch_serv(id_z)

    def arch_serv(self, id_z):

        len_data = self.db.get_arch_serv_info(id_z)
        if not isinstance(len_data, list): return

        self.dial_ui.uslugaTable.setRowCount(len(len_data))

        for i, items in enumerate(len_data):

            name_serv = QtWidgets.QTableWidgetItem(items[0])
            name_zap = QtWidgets.QTableWidgetItem(items[1])
            status_serv = QtWidgets.QTableWidgetItem(items[2])
            arch_date = QtWidgets.QTableWidgetItem(str(items[3]))

            self.dial_ui.uslugaTable.setItem(i, 0, name_serv)
            self.dial_ui.uslugaTable.setItem(i, 1, name_zap)
            self.dial_ui.uslugaTable.setItem(i, 2, status_serv)
            self.dial_ui.uslugaTable.setItem(i, 3, arch_date)

    def info_(self, id_z):

        company, mark, vincode, enginecode, milleage, prod_year = self.db.get_arch_zakaz_info(id_z)

        self.dial_ui.model_.setText(company)
        self.dial_ui.mark_.setText(mark)
        self.dial_ui.engine.setText(enginecode)
        self.dial_ui.vin.setText(vincode)
        self.dial_ui.milliage.setText(str(milleage))
        self.dial_ui.year_.setText(str(prod_year))

    def fill_data(self):

        self.dial_ui.zakazTable.setRowCount(len(self.db.get_arch_zakaz()))

        for i, items in enumerate(self.db.get_arch_zakaz()):

            id_z = QtWidgets.QTableWidgetItem(str(items[0]))
            gov_number = QtWidgets.QTableWidgetItem(str(items[1]))
            status = QtWidgets.QTableWidgetItem(str(items[2]))
            arch_date = QtWidgets.QTableWidgetItem(str(items[3]))

            self.dial_ui.zakazTable.setItem(i, 0, id_z)
            self.dial_ui.zakazTable.setItem(i, 1, gov_number)
            self.dial_ui.zakazTable.setItem(i, 2, status)
            self.dial_ui.zakazTable.setItem(i, 3, arch_date)

    def upd_data(self):

        gov_number_ = self.dial_ui.lineEdit.text()

        self.dial_ui.zakazTable.setRowCount(len(self.db.get_arch_zakaz(gov_number_)))

        for i, items in enumerate(self.db.get_arch_zakaz(gov_number_)):

            id_z = QtWidgets.QTableWidgetItem(str(items[0]))
            gov_number = QtWidgets.QTableWidgetItem(str(items[1]))
            status = QtWidgets.QTableWidgetItem(str(items[2]))
            arch_date = QtWidgets.QTableWidgetItem(str(items[3]))

            self.dial_ui.zakazTable.setItem(i, 0, id_z)
            self.dial_ui.zakazTable.setItem(i, 1, gov_number)
            self.dial_ui.zakazTable.setItem(i, 2, status)
            self.dial_ui.zakazTable.setItem(i, 3, arch_date)

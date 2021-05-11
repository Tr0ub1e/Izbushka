import subprocess
from PyQt5 import QtWidgets
from printer_m import Make_html
from order_status import Ui_Dialog
from db_tools import autowork_db

class Order_status(QtWidgets.QDialog):

    def __init__(self, con, cur, id_cust, id_z):
        super(Order_status, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.id_z = id_z
        self.id_cust = id_cust

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.dial_ui.delZakaz.clicked.connect(self.delete_zakaz_action)
        self.dial_ui.finishZak.clicked.connect(self.finish_zakaz_action)
        self.dial_ui.printButton.clicked.connect(self.print_)

        self.fill_data(id_cust, id_z)
        self.exec_()

    def print_(self):

        usl_data = self.db.get_usl_print(self.id_z)
        zap_data = self.db.get_zap_print(self.id_z)
        car_data = (self.company + " " + self.model, self.enginecode,
                    self.prod_year, self.gov_number, self.milleage, self.vincode)

        work = tuple(map(int, self.db.get_work_print(self.id_z)))
        parts = self.db.get_part_print(self.id_z)
        other = 0

        if parts[0] == None:
            parts = (0,)
        else:
            parts = tuple(map(int, self.db.get_part_print(self.id_z)))

        money_data = (*work, other, *parts)

        Make_html(self.date_z.strftime("%d-%m-%Y"), self.finish_date_z.strftime("%d-%m-%Y"),
                    car_data, usl_data, zap_data,
                    money_data).save_file()

        subprocess.Popen('python printer_handler.py')

    def delete_zakaz_action(self):

        msg = QtWidgets.QMessageBox()
        resp = msg.question(self, "Удаление заказа", \
                        "Вы уверены что хотите удалить заказ? ", msg.Yes|msg.No)

        if resp == msg.Yes:
            self.db.delete_zakaz(self.id_z)
            self.close()
        else:
            return

    def finish_zakaz_action(self):

        msg = QtWidgets.QMessageBox()
        resp = msg.question(self, "Завершение заказа", \
                        "Вы уверены что хотите завершенить заказ? ", msg.Yes|msg.No)

        if resp == msg.Yes:
            for i in range(self.dial_ui.chosedUsluga.rowCount()):
                if self.dial_ui.chosedUsluga.item(i, 2).text() != "готово":
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setWindowTitle('Ошибка')
                    msg.setText('Есть незавершенные задания')
                    msg.exec_()
                    return

            self.db.finish_zakaz(self.id_cust, self.id_z)
            self.close()
        else:
            return

    def fill_data(self, id_cust, id_z):

        self.company, self.model, self.gov_number, \
        self.enginecode, self.vincode, self.milleage, self.prod_year, \
        self.date_z, self.finish_date_z = self.db.get_more_serv_stat(id_cust, id_z)[0]

        sum_z = self.db.get_sum_z(id_z)

        self.dial_ui.milliageEdit.setText(str(self.milleage))
        self.dial_ui.vincodeEdit.setText(self.vincode)
        self.dial_ui.markEdit.setText(self.company)
        self.dial_ui.modelEdit.setText(self.model)
        self.dial_ui.engineEdit.setText(self.enginecode)
        self.dial_ui.numberEdit.setText(self.gov_number)
        self.dial_ui.yearEdit.setText(str(self.prod_year))
        self.dial_ui.startTime.setDateTime(self.date_z)
        self.dial_ui.dateTimeEdit.setDateTime(self.finish_date_z)
        self.dial_ui.sumZEdit.setText(str(*sum_z))

        self.dial_ui.chosedUsluga.setRowCount(len(self.db.get_serv_stat(id_cust, id_z)))

        for i, items in enumerate(self.db.get_serv_stat(id_cust, id_z)):

            name_serv = QtWidgets.QTableWidgetItem(items[0])
            name_zap = QtWidgets.QTableWidgetItem(items[1])
            status_serv = QtWidgets.QTableWidgetItem(items[2])

            self.dial_ui.chosedUsluga.setItem(i, 0, name_serv)
            self.dial_ui.chosedUsluga.setItem(i, 1, name_zap)
            self.dial_ui.chosedUsluga.setItem(i, 2, status_serv)

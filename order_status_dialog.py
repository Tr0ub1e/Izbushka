from PyQt5 import QtWidgets
from order_status import Ui_Dialog
from db_tools import autowork_db

class Order_status(QtWidgets.QDialog):

    def __init__(self, con, cur, id_cust, id_z):
        super(Order_status, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.id_z = id_z
        self.id_cust = id_cust

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.dial_ui.delZakaz.clicked.connect(self.delete_zakaz_action)
        self.dial_ui.finishZak.clicked.connect(self.finish_zakaz_action)

        self.fill_data(id_cust, id_z)
        self.dial.exec_()

    def delete_zakaz_action(self):

        msg = QtWidgets.QMessageBox()
        resp = msg.question(self.dial, "Удаление заказа", \
                        "Вы уверены что хотите удалить заказ? ", msg.Yes|msg.No)

        if resp == msg.Yes:
            self.db.delete_zakaz(self.id_z)
            self.dial.close()
        else:
            return

    def finish_zakaz_action(self):

        msg = QtWidgets.QMessageBox()
        resp = msg.question(self.dial, "Завершение заказа", \
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
            self.dial.close()
        else:
            return

    def fill_data(self, id_cust, id_z):

        company, model, gov_number, \
        enginecode, vincode, milleage, \
        finish_date_z, sum_z = self.db.get_more_serv_stat(id_cust, id_z)[0]

        self.dial_ui.milliageEdit.setText(str(milleage))
        self.dial_ui.vincodeEdit.setText(vincode)
        self.dial_ui.markEdit.setText(company)
        self.dial_ui.modelEdit.setText(model)
        self.dial_ui.engineEdit.setText(enginecode)
        self.dial_ui.numberEdit.setText(gov_number)
        self.dial_ui.dateTimeEdit.setDateTime(finish_date_z)
        self.dial_ui.sumZEdit.setText(str(sum_z))

        self.dial_ui.chosedUsluga.setRowCount(len(self.db.get_serv_stat(id_cust, id_z)))

        for i, items in enumerate(self.db.get_serv_stat(id_cust, id_z)):

            name_serv = QtWidgets.QTableWidgetItem(items[0])
            name_zap = QtWidgets.QTableWidgetItem(items[1])
            status_serv = QtWidgets.QTableWidgetItem(items[2])

            self.dial_ui.chosedUsluga.setItem(i, 0, name_serv)
            self.dial_ui.chosedUsluga.setItem(i, 1, name_zap)
            self.dial_ui.chosedUsluga.setItem(i, 2, status_serv)

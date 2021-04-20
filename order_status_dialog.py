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

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_data(id_cust, id_z)
        self.dial.exec_()

    def fill_data(self, id_cust, id_z):

        company, model, gov_number, enginecode, vincode, milleage, finish_date_z = self.db.get_more_serv_stat(id_cust, id_z)[0]

        self.dial_ui.milliageEdit.setText(str(milleage))
        self.dial_ui.vincodeEdit.setText(vincode)
        self.dial_ui.markEdit.setText(company)
        self.dial_ui.modelEdit.setText(model)
        self.dial_ui.engineEdit.setText(enginecode)
        self.dial_ui.numberEdit.setText(gov_number)
        self.dial_ui.dateTimeEdit.setDateTime(finish_date_z)

        self.dial_ui.chosedUsluga.setRowCount(len(self.db.get_serv_stat(id_cust, id_z)))

        for i, items in enumerate(self.db.get_serv_stat(id_cust, id_z)):

            name_serv = QtWidgets.QTableWidgetItem(items[0])
            name_zap = QtWidgets.QTableWidgetItem(items[1])
            status_serv = QtWidgets.QTableWidgetItem(items[2])

            self.dial_ui.chosedUsluga.setItem(i, 0, name_serv)
            self.dial_ui.chosedUsluga.setItem(i, 1, name_zap)
            self.dial_ui.chosedUsluga.setItem(i, 2, status_serv)
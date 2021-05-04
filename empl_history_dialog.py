from PyQt5 import QtWidgets
from empl_history import Ui_Dialog
from db_tools import autowork_db

class History(QtWidgets.QDialog):

    def __init__(self, con, cur, id_empl):
        super(History, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur
        self.id_empl = id_empl

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_data()

        self.dial_ui.pushButton.clicked.connect(self.upd_data)
        self.dial.exec_()

    def fill_data(self):

        self.dial_ui.tableWidget.setRowCount(len(self.db.show_history(self.id_empl)))

        for i, items in enumerate(self.db.show_history(self.id_empl)):

            id_serv = QtWidgets.QTableWidgetItem(str(items[2]))
            status_serv = QtWidgets.QTableWidgetItem(str(items[3]))
            timestamp = QtWidgets.QTableWidgetItem(str(items[4]))

            self.dial_ui.tableWidget.setItem(i, 0, id_serv)
            self.dial_ui.tableWidget.setItem(i, 1, status_serv)
            self.dial_ui.tableWidget.setItem(i, 2, timestamp)

    def upd_data(self):
        start = self.dial_ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        stop = self.dial_ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")

        self.dial_ui.tableWidget.setRowCount(len(self.db.show_history(self.id_empl, start, stop)))

        for i, items in enumerate(self.db.show_history(self.id_empl, start, stop)):

            id_serv = QtWidgets.QTableWidgetItem(str(items[2]))
            status_serv = QtWidgets.QTableWidgetItem(str(items[3]))
            timestamp = QtWidgets.QTableWidgetItem(str(items[4]))

            self.dial_ui.tableWidget.setItem(i, 0, id_serv)
            self.dial_ui.tableWidget.setItem(i, 1, status_serv)
            self.dial_ui.tableWidget.setItem(i, 2, timestamp)

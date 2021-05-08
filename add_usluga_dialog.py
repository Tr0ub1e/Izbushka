from PyQt5 import QtWidgets
from add_usluga import Ui_Dialog
from db_tools import autowork_db
from datetime import datetime, time

class Add_usluga(QtWidgets.QDialog):

    def __init__(self, con, cur, type_, id_serv=int):
        super(Add_usluga, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.id_serv = id_serv

        self.up_st = []

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        if type_ == 'insert':
            self.dial_ui.pushButton.clicked.connect(self.insert_usluga_action)

        if type_ == 'update':
            self.fill_data()
            self.dial_ui.pushButton.clicked.connect(self.update_usluga_action)

        self.exec_()

    def fill_data(self):

        for id_serv, name_serv, price, duration in self.db.get_uslugi():
            if id_serv == self.id_serv:
                self.dial_ui.nameEdit.setText(name_serv)
                self.dial_ui.costEdit.setText(str(price))
                self.dial_ui.timeEdit.setTime((datetime(1, 1, 1)+duration).time())

                self.up_st.append(name_serv)
                self.up_st.append(str(price))
                self.up_st.append(duration)
                break

    def update_usluga_action(self):

        d = {}

        if self.dial_ui.nameEdit.text() != self.up_st[0]:
            d['name_serv'] = self.dial_ui.nameEdit.text()

        if self.dial_ui.costEdit.text() != str(self.up_st[1]):
            d['price'] = int(self.dial_ui.costEdit.text())

        if self.dial_ui.timeEdit.text() != self.up_st[2]:
            d['duration'] = self.dial_ui.timeEdit.text()

        self.db.update_usluga(self.id_serv, d)

        self.close()

    def insert_usluga_action(self):

        name_serv = self.dial_ui.nameEdit.text()
        cost = int(self.dial_ui.costEdit.text())
        duration = self.dial_ui.timeEdit.text()

        try:
            self.db.insert_usluga(name_serv, cost, duration)
        except Exception as e:
            print(e)
        finally:
            self.close()

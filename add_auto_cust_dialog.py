from PyQt5 import QtWidgets
from add_auto_cust import Ui_Dialog
from db_tools import autowork_db
from datetime import time, timedelta

class AddAutoCust(QtWidgets.QDialog):
    """docstring for AddAutoCust."""

    def __init__(self, connection, cursor, *args, **kwargs):
        super(AddAutoCust, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = connection
        self.db.cursor = cursor

        self.id_client, self.fio = args

        self.cost = 0
        self.duration = time(0,0,0)
        self.duration.strftime("%H:%M:%S")

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_data()
        self.fill_comp()
        self.fill_usluga()

        self.dial_ui.markAuto.currentTextChanged.connect(self.fill_mark)

        self.dial_ui.addUsluga.clicked.connect(self.add_uslugi)
        self.dial_ui.delUsluga.clicked.connect(self.del_uslugi)
        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def fill_usluga(self):

        self.dial_ui.ableUsluga.setRowCount(len(self.db.get_uslugi()))

        self.id_usluga = []
        self.chosed_usluga = []

        for i, items in enumerate(self.db.get_uslugi()):

            self.id_usluga.append(items[0])

            self.dial_ui.ableUsluga.setItem(i, 0, \
                            QtWidgets.QTableWidgetItem(items[1]))
            self.dial_ui.ableUsluga.setItem(i, 1, \
                            QtWidgets.QTableWidgetItem(str(items[2])))
            self.dial_ui.ableUsluga.setItem(i, 2, \
                            QtWidgets.QTableWidgetItem(str(items[3])))

    def add_uslugi(self):

        self.dial_ui.chosedUsluga.setRowCount(self.dial_ui.ableUsluga.rowCount())

        try:
            row = self.dial_ui.ableUsluga.currentRow()
            self.chosed_usluga.append(self.id_usluga[row])

            for i in range(3):
                item = self.dial_ui.ableUsluga.takeItem(row, i)
                self.dial_ui.chosedUsluga.setItem(row, i, item)

            self.count_cost_and_time(row)

        except Exception as e:
            print(e)

    def del_uslugi(self):

        try:
            row = self.dial_ui.chosedUsluga.currentRow()
            self.chosed_usluga.remove(self.id_usluga[row])

            for i in range(3):
                item = self.dial_ui.chosedUsluga.takeItem(row, i)
                self.dial_ui.ableUsluga.setItem(row, i, item)

            self.count_cost_and_time(row, False)
        except Exception as e:
            print(e)

    def count_cost_and_time(self, row, add=True):

        try:
            if add:
                self.cost += int(self.dial_ui.chosedUsluga.item(row, 1).text())

                time_ = tuple(map(int, self.dial_ui.chosedUsluga.item(row, 2).text().split(":")))

                timeEdit = [self.duration.hour, self.duration.minute, self.duration.second]

                for i in range(3):
                    timeEdit[i] += time_[i]

                self.duration = time(*timeEdit)

            if not add:
                self.cost -= int(self.dial_ui.ableUsluga.item(row, 1).text())

                time_ = tuple(map(int, self.dial_ui.ableUsluga.item(row, 2).text().split(":")))

                timeEdit = [self.duration.hour, self.duration.minute, self.duration.second]

                for i in range(3):
                    timeEdit[i] -= time_[i]

                self.duration = time(*timeEdit)

        except Exception as e:
            print(e)

        self.dial_ui.costEdit.setText(str(self.cost))
        self.dial_ui.durationEdit.setText(str(self.duration))

    def insert_data(self):

        try:
            car_number = self.dial_ui.numberEdit.text()

            mark = self.dial_ui.markAuto.currentText()
            model = self.dial_ui.modelAuto.currentText()

            id_auto = self.db.get_car(mark, model)

            self.db.insert_auto(self.id_client, *id_auto, car_number)

        except Exception as e:
            print(e)

        finally:
            self.dial.close()

    def fill_data(self):

        fio = self.fio.split(' ')
        self.dial_ui.famEdit.setText(fio[0])
        self.dial_ui.nameEdit.setText(fio[1])
        self.dial_ui.fathEdit.setText(fio[2])
        self.dial_ui.phoneEdit.setText(str(self.db.get_phone(self.id_client)[0]))

    def fill_comp(self):

        for mark in self.db.get_companies():
            self.dial_ui.markAuto.addItem(str(*mark))

    def fill_mark(self, value):

        self.dial_ui.modelAuto.clear()

        for model in self.db.get_models(value):
            self.dial_ui.modelAuto.addItem(str(*model))

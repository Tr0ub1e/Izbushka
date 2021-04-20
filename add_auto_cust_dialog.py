import traceback
from PyQt5 import QtWidgets
from add_auto_cust import Ui_Dialog
from db_tools import autowork_db
from datetime import time, timedelta
from count_parts_dialog import Count_Parts
from count_orders_dialog import Count_Orders
from extended_qtablewidgetitem import Ext_TableItem

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
        self.part_cost = 0

        self.duration = time(0,0,0)
        self.duration.strftime("%H:%M:%S")

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_data()
        self.fill_comp()
        self.fill_mark()
        self.fill_usluga()

        self.dial_ui.markAuto.currentTextChanged.connect(self.fill_mark)

        self.dial_ui.addUsluga.clicked.connect(self.add_uslugi)
        self.dial_ui.delUsluga.clicked.connect(self.del_uslugi)

        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def fill_usluga(self):

        self.dial_ui.ableUsluga.setRowCount(len(self.db.get_uslugi()))

        for i, items in enumerate(self.db.get_uslugi()):

            self.dial_ui.ableUsluga.setItem(i, 0, \
                            Ext_TableItem(items[1], items[0]))
            self.dial_ui.ableUsluga.setItem(i, 1, \
                            QtWidgets.QTableWidgetItem(str(items[2])))
            self.dial_ui.ableUsluga.setItem(i, 2, \
                            QtWidgets.QTableWidgetItem(str(items[3])))


    def add_uslugi(self):

        self.dial_ui.chosedUsluga.setRowCount(self.dial_ui.ableUsluga.rowCount())

        try:
            row = self.dial_ui.ableUsluga.currentRow()

            mark = self.dial_ui.markAuto.currentText()
            model = self.dial_ui.modelAuto.currentText()
            id_serv = self.dial_ui.ableUsluga.item(row, 0).id_item
            serv_cost = int(self.dial_ui.ableUsluga.item(row, 1).text())

            dialog = Count_Orders(self.db.connection, self.db.cursor, mark, model, id_serv)
            data, kol_vo, part_cost = dialog.data, dialog.value, dialog.part_cost

            for i in range(3):
                item = self.dial_ui.ableUsluga.takeItem(row, i)
                self.dial_ui.chosedUsluga.setItem(row, i, item)

            self.dial_ui.chosedUsluga.setItem(row, 3, QtWidgets.QTableWidgetItem(str(kol_vo)))
            self.dial_ui.chosedUsluga.setItem(row, 4, Ext_TableItem(str(part_cost), data))
            self.count_cost_and_time(row)

        except Exception as e:
            print(traceback.format_exc())

    def del_uslugi(self):

        try:
            row = self.dial_ui.chosedUsluga.currentRow()

            for i in range(3):
                item = self.dial_ui.chosedUsluga.takeItem(row, i)
                self.dial_ui.ableUsluga.setItem(row, i, item)

            self.count_cost_and_time(row, False)
            self.dial_ui.chosedUsluga.setItem(row, 3, QtWidgets.QTableWidgetItem(" "))

        except Exception as e:
            print(e)


    def count_cost_and_time(self, row, add=True):

        try:
            if add:
                self.cost += int(self.dial_ui.chosedUsluga.item(row, 1).text())*int(self.dial_ui.chosedUsluga.item(row, 3).text())
                self.part_cost += int(self.dial_ui.chosedUsluga.item(row, 4).text())

                time_ = tuple(map(int, self.dial_ui.chosedUsluga.item(row, 2).text().split(":")))

                timeEdit = [self.duration.hour, self.duration.minute, self.duration.second]

                for x in range(int(self.dial_ui.chosedUsluga.item(row, 3).text())):
                    for i in range(3):
                        timeEdit[i] += time_[i]

                while timeEdit[1] >= 60:
                    timeEdit[0] += 1
                    timeEdit[1] -= 60

                    if timeEdit[2] >= 60: timeEdit[1] += 1; timeEdit[2] -= 60

                self.duration = time(*timeEdit)

            if not add:
                self.cost -= int(self.dial_ui.ableUsluga.item(row, 1).text())*int(self.dial_ui.chosedUsluga.item(row, 3).text())
                self.part_cost -= int(self.dial_ui.chosedUsluga.item(row, 4).text())

                time_ = tuple(map(int, self.dial_ui.ableUsluga.item(row, 2).text().split(":")))

                timeEdit = [self.duration.hour, self.duration.minute, self.duration.second]

                try:
                    for x in range(int(self.dial_ui.chosedUsluga.item(row, 3).text())):
                        for i in range(3):
                            timeEdit[i] -= time_[i]

                except:
                    for i in range(3):
                        timeEdit[i] -= time_[i]


                while timeEdit[1] < 0:
                    timeEdit[0] -= 1
                    timeEdit[1] += 60

                    if timeEdit[2] < 0: timeEdit[1] -= 1; timeEdit[2] += 60

                self.duration = time(*timeEdit)

            self.dial_ui.costEdit.setText(str(self.cost))
            self.dial_ui.durationEdit.setText(str(self.duration))
            self.dial_ui.costPartEdit.setText(str(self.part_cost))
            self.dial_ui.resultEdit.setText(str(self.part_cost+self.cost))

        except Exception as e:
            print(e)

    def insert_data(self):
        id_usluga = []

        try:
            car_number = self.dial_ui.numberEdit.text()
            mark = self.dial_ui.markAuto.currentText()
            model = self.dial_ui.modelAuto.currentText()
            id_auto = self.db.get_car(mark, model)
            vincode = self.dial_ui.vincodeEdit.text()
            enginecode = self.dial_ui.engineEdit.text()
            milleage = self.dial_ui.milliageEdit.text()

            for i in range(self.dial_ui.chosedUsluga.rowCount()):
                try:
                    id_usluga.append((self.dial_ui.chosedUsluga.item(i, 0).id_item,
                         self.dial_ui.chosedUsluga.item(i, 4).id_item,    #id_z, count
                         int(self.dial_ui.chosedUsluga.item(i, 1).text())))

                except Exception as e:
                    continue


            id_z = self.db.insert_zakaz(self.id_client, *id_auto, car_number,
                self.duration, vincode, enginecode, milleage)

            for id_serv, items, cost in id_usluga:

                if isinstance(items[0], int):
                    for i in range(items[0]):
                        self.db.insert_uslugi_zakaz(*id_z, id_serv, cost)

                else:
                    for id_part, count_p in items:
                        for j in range(count_p):
                            self.db.insert_uslugi_zakaz(*id_z, id_serv, cost, id_part)

        #    for id_zap, kol_vo in id_zapch:
        #        self.db.insert_zap_zakaz(*id_z, id_zap, kol_vo)

        except Exception as e:
            print(traceback.format_exc())

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

    def fill_mark(self):

        self.dial_ui.modelAuto.clear()

        value = self.dial_ui.markAuto.currentText()

        for model in self.db.get_models(value):
            self.dial_ui.modelAuto.addItem(str(*model))

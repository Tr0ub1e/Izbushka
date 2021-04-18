import traceback
from PyQt5 import QtWidgets
from add_auto_cust import Ui_Dialog
from db_tools import autowork_db
from datetime import time, timedelta
from count_parts_dialog import Count_Parts
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
        self.fill_zapch()

        self.dial_ui.markAuto.currentTextChanged.connect(self.fill_mark)
        self.dial_ui.modelAuto.currentTextChanged.connect(self.fill_zapch)

        self.dial_ui.addUsluga.clicked.connect(self.add_uslugi)
        self.dial_ui.delUsluga.clicked.connect(self.del_uslugi)

        self.dial_ui.addZapch.clicked.connect(self.add_parts)
        self.dial_ui.delZapch.clicked.connect(self.del_parts)

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

    def fill_zapch(self):

        self.dial_ui.chosedParts.setRowCount(0)

        mark = self.dial_ui.markAuto.currentText()
        model = self.dial_ui.modelAuto.currentText()

        if isinstance(mark, str) and isinstance(model, str):
            id_auto = self.db.get_car(mark, model)


        if id_auto:
            self.dial_ui.ableParts.setRowCount(len(self.db.get_zapchasti_car(*id_auto)))

            for row, i in enumerate(self.db.get_zapchasti_car(*id_auto)):

                id_zap, kol_vo, _, name_z, cost = i

                self.dial_ui.ableParts.setItem(row, 0, Ext_TableItem(name_z, id_zap))
                self.dial_ui.ableParts.setItem(row, 1, QtWidgets.QTableWidgetItem(str(kol_vo)))
                self.dial_ui.ableParts.setItem(row, 2, QtWidgets.QTableWidgetItem(str(cost)))

    def add_uslugi(self):

        self.dial_ui.chosedUsluga.setRowCount(self.dial_ui.ableUsluga.rowCount())

        try:
            row = self.dial_ui.ableUsluga.currentRow()

            dialog = Count_Parts(self.dial_ui.ableUsluga.item(row, 1).text())
            kol_vo = dialog.value

            for i in range(3):
                item = self.dial_ui.ableUsluga.takeItem(row, i)
                self.dial_ui.chosedUsluga.setItem(row, i, item)

            self.dial_ui.chosedUsluga.setItem(row, 3, QtWidgets.QTableWidgetItem(str(kol_vo)))
            self.count_cost_and_time(row)

        except Exception as e:
            print(e)

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

    def add_parts(self):

        self.dial_ui.chosedParts.setRowCount(self.dial_ui.ableParts.rowCount())

        row = self.dial_ui.ableParts.currentRow()
        dialog = Count_Parts(self.dial_ui.ableParts.item(row, 1).text())
        kol_vo = dialog.value

        try:
            if kol_vo == 0: return

            cost = int(self.dial_ui.ableParts.item(row, 2).text())
            item = self.dial_ui.ableParts.item(row, 0)

            self.dial_ui.chosedParts.setItem(row, 0, Ext_TableItem(item.text(), item.id_item))
            self.dial_ui.chosedParts.setItem(row, 1, QtWidgets.QTableWidgetItem(str(kol_vo)))
            self.dial_ui.chosedParts.setItem(row, 2, QtWidgets.QTableWidgetItem(str(cost*kol_vo)))

            self.count_part_cost(row)

        except Exception as e:
            print(e)

    def del_parts(self):

        try:

            row = self.dial_ui.ableParts.currentRow()
            self.count_part_cost(row, False)

            for i in range(3):
                self.dial_ui.chosedParts.setItem(row, i, QtWidgets.QTableWidgetItem(" "))

        except Exception as e:
            print(e)

    def count_cost_and_time(self, row, add=True):

        try:
            if add:
                self.cost += int(self.dial_ui.chosedUsluga.item(row, 1).text())*int(self.dial_ui.chosedUsluga.item(row, 3).text())

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
            self.dial_ui.resultEdit.setText(str(self.part_cost+self.cost))

        except Exception as e:
            print(e)

    def count_part_cost(self, row, add=True):

        try:
            if add:
                self.part_cost += int(self.dial_ui.chosedParts.item(row, 2).text())

            else:
                self.part_cost -= int(self.dial_ui.chosedParts.item(row, 2).text())

        except Exception as e:
            print(e)

        self.dial_ui.costZapchEdit.setText(str(self.part_cost))
        self.dial_ui.resultEdit.setText(str(self.part_cost+self.cost))

    def insert_data(self):
        id_usluga = []
        id_zapch = []

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
                    id_usluga.append(
                        (self.dial_ui.chosedUsluga.item(i, 0).id_item,
                        int(self.dial_ui.chosedUsluga.item(i, 1).text()),
                        int(self.dial_ui.chosedUsluga.item(i, 3).text()))
                        )
                except:
                    continue

            for i in range(self.dial_ui.chosedParts.rowCount()):
                try:
                    id_zapch.append(
                                (self.dial_ui.chosedParts.item(i, 0).id_item,
                                int(self.dial_ui.chosedParts.item(i, 1).text()))
                                )
                except:
                    continue

            id_z = self.db.insert_zakaz(self.id_client, *id_auto, car_number,
                self.duration, vincode, enginecode, milleage)

            for id_serv, cost_serv, count_serv in id_usluga:
                self.db.insert_uslugi_zakaz(*id_z, id_serv, cost_serv, count_serv)

            for id_zap, kol_vo in id_zapch:
                self.db.insert_zap_zakaz(*id_z, id_zap, kol_vo)

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

    def fill_mark(self):

        self.dial_ui.modelAuto.clear()

        value = self.dial_ui.markAuto.currentText()

        for model in self.db.get_models(value):
            self.dial_ui.modelAuto.addItem(str(*model))

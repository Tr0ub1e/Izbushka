from PyQt5 import QtWidgets
from extended_qtablewidgetitem import Ext_TableItem
from count_parts_dialog import Count_Parts
from count_orders import Ui_Dialog
from db_tools import autowork_db


class Count_Orders(QtWidgets.QDialog):

    def __init__(self, con, cursor, mark, model, id_serv):
        super(Count_Orders, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.db = autowork_db()
        self.db.connection, self.db.cursor = con, cursor

        self.fill_zapch(mark, model)

        self.value = 0
        self.part_value = 0
        self.part_cost = 0

        self.id_serv = id_serv

        self.dial_ui.pushButton.clicked.connect(self.get_number)
        self.dial_ui.addZapch.clicked.connect(self.add_parts)
        self.dial_ui.delZapch.clicked.connect(self.del_parts)

        self.exec_()

    def fill_zapch(self, mark, model):

        self.dial_ui.chosedParts.setRowCount(0)

        if isinstance(mark, str) and isinstance(model, str):
            id_auto = self.db.get_car(mark, model)

        if id_auto:
            self.dial_ui.ableParts.setRowCount(len(self.db.get_zapchasti_car(*id_auto)))

            for row, i in enumerate(self.db.get_zapchasti_car(*id_auto)):

                id_zap, kol_vo, _, name_z, cost = i

                self.dial_ui.ableParts.setItem(row, 0, Ext_TableItem(name_z, id_zap))
                self.dial_ui.ableParts.setItem(row, 1, QtWidgets.QTableWidgetItem(str(kol_vo)))
                self.dial_ui.ableParts.setItem(row, 2, QtWidgets.QTableWidgetItem(str(cost)))

    def get_number(self):

        self.value = self.dial_ui.countParts.value()
        self.data = []

        if self.value < self.part_value:

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка ввода")
            msg.setInformativeText('Кол-во деталей не соответсвует услугам')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

            return

        if self.dial_ui.checkBox.isChecked():
            self.data.append(self.value)
            self.close()

        for i in range(self.dial_ui.chosedParts.rowCount()):

            try:
                id_z = self.dial_ui.ableParts.item(i, 0).id_item
                count = int(self.dial_ui.chosedParts.item(i, 1).text())
                self.data.append((id_z, count))

            except:
                continue

        self.close()

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

            self.part_value += kol_vo
            self.count_part_cost(row)

        except Exception as e:
            print(e)

    def del_parts(self):

        try:
            row = self.dial_ui.ableParts.currentRow()
            kol_vo = int(self.dial_ui.chosedParts.item(row, 1).text())
            self.part_value -= kol_vo
            self.count_part_cost(row, False)

            for i in range(3):
                self.dial_ui.chosedParts.setItem(row, i, QtWidgets.QTableWidgetItem(" "))

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

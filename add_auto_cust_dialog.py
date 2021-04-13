from PyQt5 import QtWidgets
from add_auto_cust import Ui_Dialog
from db_tools import autowork_db


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

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_data()
        self.fill_comp()

        self.dial_ui.markAuto.currentTextChanged.connect(self.fill_mark)

        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def fill_usluga(self):
        pass

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

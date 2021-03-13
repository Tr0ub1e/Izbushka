from PyQt5 import QtWidgets
from add_auto_cust import Ui_Dialog
from db_tools import autowork_db


class AddAutoCust(QtWidgets.QDialog):
    """docstring for AddAutoCust."""

    def __init__(self, connection, cursor):
        super(AddAutoCust, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = connection
        self.db.cursor = cursor

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_comp()
        self.dial_ui.markAuto.currentTextChanged.connect(self.fill_mark)

        self.fill_fam()
        self.dial_ui.famList.currentTextChanged.connect(self.fill_name)
        self.dial_ui.nameList.currentTextChanged.connect(self.fill_fath)
        self.dial_ui.fathList.currentTextChanged.connect(self.fill_phone)

#        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def fill_comp(self):

        for mark in self.db.get_companies():
            self.dial_ui.markAuto.addItem(str(*mark))

    def fill_mark(self, value):

        self.dial_ui.modelAuto.clear()

        for model in self.db.get_models(value):
            self.dial_ui.modelAuto.addItem(str(*model))

    def fill_fam(self):

        for i in self.db.get_fam():
            self.dial_ui.famList.addItem(str(*i))

    def fill_name(self, fam):

        self.dial_ui.nameList.clear()

        for i in self.db.get_name(fam):
            self.dial_ui.nameList.addItem(str(*i))

    def fill_fath(self, name):

        self.dial_ui.fathList.clear()

        fam = self.dial_ui.famList.currentText()

        for i in self.db.get_fath(fam, name):
            self.dial_ui.fathList.addItem(str(*i))

    def fill_phone(self, fath):

        self.dial_ui.phoneList.clear()

        fam = self.dial_ui.famList.currentText()
        name = self.dial_ui.nameList.currentText()

        for i in self.db.get_phone(fam, name, fath):
            self.dial_ui.phoneList.addItem(str(*i))

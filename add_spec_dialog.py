from PyQt5 import QtWidgets
from add_spec import Ui_Dialog
from db_tools import autowork_db


class Add_specialization(QtWidgets.QDialog):

    def __init__(self, con, cursor, type_, data=str):
        super(Add_specialization, self).__init__()

        self.db = autowork_db()
        self.db.connection, self.db.cursor = con, cursor

        self.dial_ui = Ui_Dialog()

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        if type_ == 'insert':
            self.dial_ui.pushButton.clicked.connect(self.insert_spec)

        if type_ == 'update':
            self.old_name = data
            self.dial_ui.lineEdit.setText(data)
            self.dial_ui.pushButton.clicked.connect(self.change_spec)

        self.exec_()

    def insert_spec(self):

        name_spec = self.dial_ui.lineEdit.text()

        for i in name_spec:
            if i in '1234567890!@#$%^&*(_+)':
                self.error_msg()
                return

        self.db.add_spec(name_spec)
        self.close()

    def change_spec(self):

        new_name = self.dial_ui.lineEdit.text()

        if new_name != self.old_name:

            for i in new_name:
                if i in '1234567890!@#$%^&*(_+)':
                    self.error_msg()
                    return

            self.db.update_spec(self.old_name, new_name)

        self.close()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

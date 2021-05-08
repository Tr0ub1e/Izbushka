from add_car import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from db_tools import autowork_db


class CarDial(QtWidgets.QDialog):

    def __init__(self, con, cur):
        super(CarDial, self).__init__()

        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.exec_()

    def insert_data(self):

        mark = self.dial_ui.mark.text()
        model = self.dial_ui.model.text()

        try:
            self.db.insert_car(mark, model)
        except Exception as e:
            print(e)
            self.error_msg()
        finally:
            self.close()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

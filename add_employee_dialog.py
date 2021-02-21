from add_employee import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from db_tools import autowork_db

class EmpDial(QtWidgets.QDialog):

    def __init__(self, specs, con, cur):
        super(EmpDial, self).__init__()

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.fill_box(specs)

        self.dial_ui.pushButton.clicked.connect(self.insert_data)

        self.dial.exec_()

    def fill_box(self, items):

        for id_spec, name_spec in items:
            self.dial_ui.comboBox.addItem(str(name_spec))

    def insert_data(self):

        try:
            fam = self.dial_ui.famEdit.text()
            name = self.dial_ui.nameEdit.text()
            fath = self.dial_ui.fathEdit.text()

            rental_date = self.dial_ui.dateEdit.date()
            rate = self.dial_ui.moneyEdit.text()
            spec = self.dial_ui.comboBox.currentText()

            try:
                rate = int(rate)
            except:
                raise

            _ = fam + " " +name+ " " + fath

            self.db.insert_employees(_, rental_date, rate, spec)

        except Exception as e:
            #print(e)
            self.error_msg()

        finally:
            self.dial.close()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

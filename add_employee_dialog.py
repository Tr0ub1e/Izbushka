from datetime import datetime
from add_employee import Ui_Dialog
from PyQt5 import QtWidgets, QtGui
from db_tools import autowork_db

class EmpDial(QtWidgets.QDialog):

    def __init__(self, specs, con, cur, type_, up_st=()):
        super(EmpDial, self).__init__()

        self.dial_ui = Ui_Dialog()
        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.fill_box(specs)

        if type_ == 'insert':
            self.dial_ui.pushButton.clicked.connect(self.insert_data)

        if type_ == 'update':
            self.fill_data(*up_st)

            self.fio, self.rate, self.spec, self.phone = self.get_data()

            self.dial_ui.pushButton.clicked.connect(self.update_data)


        self.exec_()

    def fill_box(self, items):

        for id_spec, name_spec in items:
            self.dial_ui.comboBox.addItem(str(name_spec))

    def get_data(self):

        try:
            fam = self.dial_ui.famEdit.text()
            name = self.dial_ui.nameEdit.text()
            fath = self.dial_ui.fathEdit.text()

            rate = self.dial_ui.moneyEdit.text()
            spec = self.dial_ui.comboBox.currentText()
            phone = self.dial_ui.phoneEdit.text()

            try:
                rate = int(rate)
                if len(phone) > 12: raise
            except Exception as e:
                print(e)

            _ = fam + " " +name+ " " + fath

            return _, rate, spec, phone

        except Exception as e:
            print(e)
            self.error_msg()

        finally:
            self.close()

    def insert_data(self):

        _ = self.get_data()
        date = datetime.now().strftime('%Y-%m-%d')
        self.db.insert_employees(*_, date)

    def fill_data(self, id_empl, fam, name, fath, rate, phone, spec):

        try:
            self.id_empl = id_empl
            self.dial_ui.famEdit.setText(fam)
            self.dial_ui.nameEdit.setText(name)
            self.dial_ui.fathEdit.setText(fath)
            self.dial_ui.moneyEdit.setText(rate)
            self.dial_ui.comboBox.setCurrentIndex(self.dial_ui. \
                                            comboBox.findText(spec))
            self.dial_ui.phoneEdit.setText(phone)

        except Exception as e:
            print(e)
            self.error_msg()

        finally:
            self.close()

    def update_data(self):

        fio, rate, spec, phone = self.get_data()
        id_pos = self.db.get_id_spec(spec)

        data = {}

        if self.fio != fio:
            data['fio'] = fio

        if self.rate != rate:
            data['rate'] = rate

        if self.phone != phone:
            data['phone'] = phone

        self.db.update_empl(self.id_empl, *id_pos, d=data)

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

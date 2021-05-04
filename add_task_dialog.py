import traceback
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from add_task import Ui_Dialog
from db_tools import autowork_db


class Add_Task(QtWidgets.QDialog):

    def __init__(self, con, cursor):
        super(Add_Task, self).__init__()

        self.db = autowork_db()
        self.db.connection, self.db.cursor = con, cursor

        self.id_serv = []
        self.id_spec = []
        self.id_empl = []
        self.id_zakaz = []
        self.id_time = []

        self.dial = QtWidgets.QDialog()
        self.dial_ui = Ui_Dialog()

        self.dial_ui.setupUi(self.dial)
        self.dial_ui.retranslateUi(self.dial)

        self.dial_ui.dateEdit.setDate(datetime.now().date())

        self.fill_serv()
        self.fill_spec()
        self.fill_empl()
        self.fill_tasks()
        self.fill_info()

        self.dial_ui.specBox.currentIndexChanged.connect(self.fill_empl)
        self.dial_ui.uslugaBox.currentTextChanged.connect(self.foo)
        self.dial_ui.taskBox.currentIndexChanged.connect(self.fill_info)
        self.dial_ui.taskBox.currentTextChanged.connect(self.fill_info)

        self.dial_ui.pushButton.clicked.connect(self.insert_task)

        self.dial.exec_()

    def fill_serv(self):

        for id_serv_, name_serv, duration, _ in self.db.get_uslugi():
            self.id_serv.append(id_serv_)
            self.dial_ui.uslugaBox.addItem(name_serv)

        for id_time_, time_ in self.db.get_working_ours():
            self.id_time.append(id_time_)
            self.dial_ui.timeEdit.addItem(str(time_))

    def foo(self):
        self.fill_tasks()
        self.fill_info()

    def fill_tasks(self):
        self.dial_ui.taskBox.clear()
        self.id_zakaz.clear()

        id_serv = self.dial_ui.uslugaBox.currentIndex()

        for id_serv_z, name_zap, finish_date, duration, id_zap in self.db.get_pending_uslugi(self.id_serv[id_serv]):
            self.dial_ui.taskBox.addItem("Задание №%s" % id_serv_z)
            self.id_zakaz.append((id_serv_z, (name_zap, id_zap), finish_date, duration))

    def fill_info(self):

        self.dial_ui.lineEdit_3.setText('')
        self.dial_ui.partEdit.setText('')

        try:
            id_serv_z = self.dial_ui.taskBox.currentIndex()

            id_serv_z, name_zap_id_zap, finish_date, duration = self.id_zakaz[id_serv_z]

            self.dial_ui.lineEdit_3.setText(str(finish_date))
            self.dial_ui.durationEdit.setText(str(duration))
            self.dial_ui.partEdit.setText(name_zap_id_zap[0])

        except Exception as e:
            pass

    def fill_spec(self):

        for id_spec_, name_spec in self.db.show_spec():
            self.id_spec.append(id_spec_)
            self.dial_ui.specBox.addItem(name_spec)

    def fill_empl(self):

        self.dial_ui.emplBox.clear()
        self.id_empl.clear()

        name_spec = self.dial_ui.specBox.currentText()

        for fio, id_empl_ in self.db.emp_pos(name_spec):
            self.id_empl.append(id_empl_)
            self.dial_ui.emplBox.addItem(fio)

    def insert_task(self):

        try:
            date_ = self.dial_ui.dateEdit.date().toString(Qt.ISODate)

            id_time = self.id_time[self.dial_ui.timeEdit.currentIndex()]
            id_date = self.db.insert_timetable(date_)

            id_serv_z = self.dial_ui.taskBox.currentIndex()
            id_serv_z, _, _, _ = self.id_zakaz[id_serv_z]
            #id_zap = id_zap[1]
            id_empl = self.id_empl[self.dial_ui.emplBox.currentIndex()]

            id_serv = self.id_serv[self.dial_ui.uslugaBox.currentIndex()]

            self.db.insert_shedule(*id_date, id_time, id_serv_z, id_empl)

        except Exception as e:
            print(traceback.format_exc())
            self.error_msg()

        self.dial.close()

    def error_msg(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Ошибка добавления")
        msg.setInformativeText('Проверьте правильность данных')
        msg.setWindowTitle("Ошибка")
        msg.exec_()

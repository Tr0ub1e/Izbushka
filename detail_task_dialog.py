from PyQt5 import QtWidgets
from detail_task import Ui_Dialog
from db_tools import autowork_db

class TaskInfo(QtWidgets.QDialog):

    def __init__(self, con, cur, id_shedule):
        super(TaskInfo, self).__init__()

        self.dial_ui = Ui_Dialog()

        self.db = autowork_db()

        self.db.connection = con
        self.db.cursor = cur

        self.dial_ui.setupUi(self)
        self.dial_ui.retranslateUi(self)

        self.fill_data(id_shedule)

        self.exec_()

    def fill_data(self, id_shedule):

        name_serv, name_zap, finish_date_z, \
                name_spec, fio = self.db.get_task_info(id_shedule)

        self.dial_ui.uslugaEdit.setText(name_serv)
        self.dial_ui.partEdit.setText(name_zap)
        self.dial_ui.endTime.setText(str(finish_date_z))
        self.dial_ui.emplSpec.setText(name_spec)
        self.dial_ui.emplEdit.setText(fio)

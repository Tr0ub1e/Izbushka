from PyQt5 import QtWidgets, QtGui
from functools import wraps

def update_windows(func):

    @wraps(func)
    def inner(self, *args, **kwargs):

        res = func(self)
        self.clear_table()
        self.clients_table()
        self.ui.emplTree.clear()
        self.ui.clientTree.clear()
        self.clear_table()
        self.clear_labels()

        self.zakaz_tree()
        self.employees()
        self.clients()
        self.uslugi()

        return res

    return inner

def disconnect_(func):

    @wraps(func)
    def inner(self):

        self.ui.emplTree.clear()
        self.ui.specTable.clear()
        self.ui.uslugiTree.clear()
        self.ui.clientTree.clear()
        self.clear_table()
        self.clear_labels()

        self.ui.addEmpl.disconnect()
        self.ui.changeEmpl.disconnect()
        self.ui.delEmpl.disconnect()

        self.ui.addCust.disconnect()
        self.ui.changeCust.disconnect()
        self.ui.delCust.disconnect()

        self.ui.addSpec.disconnect()
        self.ui.changeSpec.disconnect()
        self.ui.delSpec.disconnect()

        self.ui.addZakaz.disconnect()

        return func(self)

    return inner

def connect_(func):

    @wraps(func)
    def inner(self):

        self.ui.addEmpl.clicked.connect(self.raise_add_emp)
        self.ui.changeEmpl.clicked.connect(self.raise_change_empl)
        self.ui.delEmpl.clicked.connect(self.delete_empl)

        self.ui.addSpec.clicked.connect(self.raise_add_spec)
        self.ui.changeSpec.clicked.connect(self.raise_change_spec)
        self.ui.delSpec.clicked.connect(self.delete_spec)

        self.ui.addCust.clicked.connect(self.raise_add_cust)
        self.ui.delCust.clicked.connect(self.delete_cust)
        self.ui.changeCust.clicked.connect(self.raise_change_cust)

        self.ui.addZakaz.clicked.connect(self.raise_add_auto)

        self.ui.addTimetable.clicked.connect(self.make_task)
        self.ui.delTimetable.clicked.connect(self.delete_task_)

        self.ui.clientTable.cellDoubleClicked.connect(self.get_status_z)
        self.ui.tasksTable.cellDoubleClicked.connect(self.done_task_empl)

        return func(self)
    return inner

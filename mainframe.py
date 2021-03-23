from PyQt5 import QtWidgets, QtGui
from myform import Ui_MainWindow
from db_tools import autowork_db
from connection_dialog import ConDial
from add_employee_dialog import EmpDial
from add_cust_dialog import CustDial
from add_auto_cust_dialog import AddAutoCust


class MainFrame(QtWidgets.QMainWindow, autowork_db):

    def __init__(self):
        """
        Главное окно
        Инициализация, подключение кнопок, вывод окна
        """
        super(MainFrame, self).__init__()

        self.win = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.win)
        self.ui.retranslateUi(self.win)

        self.ui.make_con.triggered.connect(self.raise_con_dialog)
        self.ui.discon.triggered.connect(self.raise_discon_dialog)

        self.win.show()

    def raise_discon_dialog(self):
        """
        Отключение от БД
        Выводит сообщение
        """

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Выход выполнен успешно")
        msg.setWindowTitle("Выход")

        try:
            self.close_db()

            self.ui.add_emp.disconnect()
            self.ui.add_client.disconnect()
            self.ui.add_auto.disconnect()

            msg.exec_()

        except Exception as e:
            print(e)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Выход выполнен не успешно")
            msg.setInformativeText("Возможно вы были неподключены к БД")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def raise_con_dialog(self):
        """
        Выводит диалог подключения к БД
        возвращает Подлючение и Курсор
        """
        try:
            my_dial = ConDial()
            self.connection, self.cursor = my_dial.mainDial()
            my_dial.access_msg()

            self.ui.add_emp.triggered.connect(self.raise_add_emp)
            self.ui.add_client.triggered.connect(self.raise_add_cust)
            self.ui.add_auto.triggered.connect(self.raise_add_auto)

            self.employees()
            self.clients()
            #self.debug_tree()

        except Exception as e:
            print(e)
            my_dial.error_msg()

    def raise_add_auto(self):
        """
        """
        my_dial = AddAutoCust(self.connection, self.cursor)

    def raise_add_emp(self):
        """
        Выводит диалог добавления нового работника в БД
        """
        my_dial = EmpDial(self.show_spec(), self.connection, self.cursor)
        self.ui.emplTree.clear()
        self.employees()

    def raise_add_cust(self):
        """
        Выводит диалог добавления нового клиента
        """
        my_dial = CustDial(self.connection, self.cursor)
        self.ui.clientTree.clear()
        self.clients()

    def clients(self):
        """
        Вывод отсорт. дерева клиентов по фамилиям
        """
        list_of_fam = [j for i in self.get_fam() for j in i]


        for fam in sorted(list_of_fam):
            parent = QtWidgets.QTreeWidgetItem(self.ui.clientTree)
            parent.setFlags(parent.flags())
            parent.setText(0, fam)

            for fio in self.get_fio(fam):
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, *fio)

    def employees(self):
        """
        Вывод дерева специальностей и работников
        """
        for name in self.show_spec():
            parent = QtWidgets.QTreeWidgetItem(self.ui.emplTree)
            parent.setFlags(parent.flags())
            parent.setText(0, name[1])

            for fio, id_empl in self.emp_pos(name[1]):
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setText(0, "{}: {}".format(fio, id_empl))

        self.ui.emplTree.itemSelectionChanged.connect(self.empl_tree_items)

    def clear_table(self):
        """
        Очистка таблицы, удаление стобцов и колонок
        """
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)

    def empl_tree_items(self):

        if not self.ui.emplTree.currentItem().text(0) in \
                                        [x for _, x in self.show_spec()]:

            fio, id_empl = self.ui.emplTree.currentItem().text(0).split(':')

            self.ui.fioLab.setText(fio)

            self.ui.specLab.setText(self.ui.emplTree. \
                            currentItem().parent().text(0))

            _, _, rental_date, rate, phone = tuple(self.get_empl(id_empl)[0])

            self.ui.dateLab.setText(str(rental_date))
            self.ui.rateLab.setText(str(rate))
            self.ui.phoneLab.setText(phone)

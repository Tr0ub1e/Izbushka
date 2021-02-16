from PyQt5 import QtWidgets, QtGui
from myform import Ui_MainWindow
from db_tools import autowork_db
from connection_dialog import ConDial
from add_employee_dialog import EmpDial
from add_cust_dialog import CustDial


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
        self.ui.discon.triggered.connect(self.close_db)

        self.ui.employees.triggered.connect(self.employees)
        self.ui.customer.triggered.connect(self.clients)
        self.ui.spec.triggered.connect(self.special)

        self.ui.add_emp.triggered.connect(self.raise_add_emp)
        self.ui.add_client.triggered.connect(self.raise_add_cust)

        self.transl = {'car':'Авто', 'customer':'Клиенты',
                        'employees':'Сотрудники', 'services':'Услуги',
                        'spec':'Специализации'}

        self.win.show()

    def raise_con_dialog(self):
        """
        Выводит диалог подключения к БД
        возвращает Подлючение и Курсор
        """
        try:
            my_dial = ConDial()
            self.connection, self.cursor = my_dial.mainDial()
        except:
            pass

    def raise_add_emp(self):
        """
        Выводит диалог добавления нового работника в БД
        """
        my_dial = EmpDial(self.show_spec(), self.connection, self.cursor)

    def raise_add_cust(self):
        """
        Выводит диалог добавления нового клиента
        """
        try:
            my_dial = CustDial(self.connection, self.cursor)
        except Exception as e:
            print(e)

    def employees(self):
        """
        Вывод в таблицу работников по типу

        перв ключ\фио\дата приема на работу\зарплата
        """
        self.clear_table()
        self.ui.tableWidget.setColumnCount(5)

        for i in self.show_employees():

            ind, fio, date, rate, spec = i
            rows = self.ui.tableWidget.rowCount()

            self.ui.tableWidget.insertRow(rows)
            self.ui.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(ind)))
            self.ui.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(fio))
            self.ui.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(str(date)))
            self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(rate)))
            self.ui.tableWidget.setItem(rows, 4, QtWidgets.QTableWidgetItem(spec))

        self.ui.tableWidget.setHorizontalHeaderLabels(['id', 'Фио', 'Дата приема', 'Ставка', 'Специализация'])
        self.ui.tableWidget.resizeColumnsToContents()

    def clients(self):
        """
        Вывод в таблицу клиентов по типу

        перв кл\фио\телефон\кол-во заказов
        """
        self.clear_table()
        self.ui.tableWidget.setColumnCount(4)

        for i in self.show_customers():
            ind, fio, phone, orders = i
            rows = self.ui.tableWidget.rowCount()

            self.ui.tableWidget.insertRow(rows)
            self.ui.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(ind)))
            self.ui.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(fio))
            self.ui.tableWidget.setItem(rows, 2, QtWidgets.QTableWidgetItem(phone))
            self.ui.tableWidget.setItem(rows, 3, QtWidgets.QTableWidgetItem(str(orders)))

        self.ui.tableWidget.setHorizontalHeaderLabels(['id', 'Фио', 'Телефон', 'Кол-во обращений'])
        self.ui.tableWidget.resizeColumnsToContents()


    def special(self):
        """
        Вывод в таблицу специальностей
        перв кл\имя
        """
        self.clear_table()
        self.ui.tableWidget.setColumnCount(2)

        for i in self.show_spec():

            id_sp, name = i
            rows = self.ui.tableWidget.rowCount()

            self.ui.tableWidget.insertRow(rows)
            self.ui.tableWidget.setItem(rows, 0, QtWidgets.QTableWidgetItem(str(id_sp)))
            self.ui.tableWidget.setItem(rows, 1, QtWidgets.QTableWidgetItem(name))

        self.ui.tableWidget.setHorizontalHeaderLabels(['id_spec', 'Специальность'])
        self.ui.tableWidget.resizeColumnsToContents()


    def clear_table(self):
        """
        Очистка таблицы, удаление стобцов и колонок
        """
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)

import traceback
from datetime import datetime
from PyQt5 import QtWidgets, QtGui
from myform import Ui_MainWindow
from db_tools import autowork_db
from add_spec_dialog import Add_specialization
from add_task_dialog import Add_Task
from connection_dialog import ConDial
from add_employee_dialog import EmpDial
from add_cust_dialog import CustDial
from add_auto_cust_dialog import AddAutoCust
from order_status_dialog import Order_status
from extended_QTreeItem import Ext_Item
from extended_qtablewidgetitem import Ext_TableItem

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
            self.auxiliary()

            self.close_db()
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

            self.employees()
            self.clients()
            self.uslugi()
            self.zakaz_tree()

        except Exception as e:
            print(traceback.format_exc())
            my_dial.error_msg()

    def raise_add_spec(self):
        Add_specialization(self.connection, self.cursor, 'insert')
        self.ui.emplTree.clear()
        self.employees()

    def raise_change_spec(self):

        try:
            old_name = self.ui.emplTree.currentItem().text(0)

            if old_name in [name_spec for _, name_spec in self.show_spec()]:
                self.ui.emplTree.clear()

                Add_specialization(self.connection, self.cursor, 'update', old_name)
                self.employees()
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка изменения")
            msg.setInformativeText('Произошел сбой в изменении данных')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def delete_spec(self):

        try:
            name = self.ui.emplTree.currentItem().text(0)

            if self.ui.emplTree.currentItem().childCount() == 0:
                self.ui.emplTree.clear()
                self.del_spec(name)

                self.employees()
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Нельзя удалять занятые специальности')
                msg.setWindowTitle("Ошибка")
                msg.exec_()

        except:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Произошел сбой в удалении данных')
                msg.setWindowTitle("Ошибка")
                msg.exec_()

    def raise_add_auto(self):
        """
        """
        try:
            fio = self.ui.clientTree.currentItem().text(0)
            id_client = self.ui.clientTree.currentItem().id_item

            my_dial = AddAutoCust(self.connection, self.cursor, id_client, fio)

            self.ui.clientTable.setRowCount(0)
            self.clients_table()
            self.uslugi()

        except:
            print(traceback.format_exc())
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка добавления")
            msg.setInformativeText('Вы не выбрали клиента')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def raise_add_emp(self):
        """
        Выводит диалог добавления нового работника в БД
        """
        my_dial = EmpDial(self.show_spec(), self.connection, \
                                                    self.cursor, 'insert')
        self.ui.emplTree.clear()
        self.clear_labels()
        self.employees()

    def raise_change_empl(self):

        try:

            if self.ui.emplTree.currentItem().text(0) \
                    in [name_spec for _, name_spec in self.show_spec()]:

                id_empl = self.ui.emplTree.currentItem().id_item
                fio = self.ui.fioLab.text().split(' ')
                spec = self.ui.specLab.text()
                date_ = datetime.strptime(self.ui.dateLab.text(), '%Y-%m-%d').date()
                phone = self.ui.phoneLab.text()
                rate = self.ui.rateLab.text()

                _ = (id_empl, *fio, date_, rate, phone, spec)

                my_dial = EmpDial(self.show_spec(), self.connection, self.cursor,
                        "update", _)

                self.ui.emplTree.clear()
                self.clear_labels()
                self.employees()

        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка изменения")
            msg.setInformativeText('Произошел сбой в изменении данных')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def raise_add_cust(self):
        """
        Выводит диалог добавления нового клиента
        """
        my_dial = CustDial(self.connection, self.cursor, "insert")
        self.ui.clientTree.clear()
        self.clients()

    def raise_change_cust(self):

        try:
            fio = self.ui.fioCli.text()
            phone = self.ui.phoneCli.text()
            id_cust = self.ui.clientTree.currentItem().id_item

            up_st = (id_cust, fio, phone)

            my_dial = CustDial(self.connection, self.cursor, "update", up_st)
            self.ui.clientTree.clear()
            self.clients()
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка изменения")
            msg.setInformativeText('Произошел сбой в изменении данных')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    def delete_empl(self):

        msg = QtWidgets.QMessageBox()

        try:
            id_empl = self.ui.emplTree.currentItem().id_item
            self.delete_empl_by_id(id_empl)

            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText("Удаление выполнено успешно!")
            msg.setWindowTitle("Удаление")

            self.ui.emplTree.clear()
            self.employees()

        except:
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка удаления")
            msg.setInformativeText('Произошел сбой в удалении данных')
            msg.setWindowTitle("Ошибка")

        finally:
            msg.exec_()

    def delete_cust(self):

        if not self.ui.clientTree.currentItem().text(0) in \
                                    [j for i in self.get_fam() for j in i]:

            if self.ui.clientTable.rowCount() != 0:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Нельзя удалять клиента с активными заказами')
                msg.setWindowTitle("Ошибка")
                msg.exec_()

                return

            id_cust = self.ui.clientTree.currentItem().id_item
            self.delete_customer(id_cust)

            self.ui.clientTree.clear()
            self.clear_table()
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

            for _id, fio in self.get_fio(fam):
                child = Ext_Item(parent, _id)
                child.setText(0, fio)

        self.ui.clientTree.itemSelectionChanged.connect(self.clients_table)

    def employees(self):
        """
        Вывод дерева специальностей и работников
        """
        for name in self.show_spec():
            parent = QtWidgets.QTreeWidgetItem(self.ui.emplTree)
            parent.setFlags(parent.flags())
            parent.setText(0, name[1])

            for fio, id_empl in self.emp_pos(name[1]):
                child = Ext_Item(parent, id_empl)
                child.setText(0, "{}".format(fio))

        self.ui.emplTree.itemSelectionChanged.connect(self.empl_tree_items)

    def uslugi(self):
        self.ui.uslugiTree.clear()

        for id_serv, name_serv, _, _ in self.get_uslugi():

            parent = QtWidgets.QTreeWidgetItem(self.ui.uslugiTree)
            parent.setFlags(parent.flags())
            parent.setText(0, name_serv)

            for id_serv_z, _, _, _, status in self.get_pending_zakaz(id_serv):

                child = Ext_Item(parent, (id_serv_z))
                child.setText(0, "Задание №{} \n({})".format(id_serv_z, status))

    def clear_table(self):
        """
        Очистка таблицы, удаление стобцов и колонок
        """
        self.ui.clientTable.setRowCount(0)

    def clear_labels(self):

        text = "NULL"

        self.ui.fioLab.setText(text)
        self.ui.dateLab.setText(text)
        self.ui.phoneLab.setText(text)
        self.ui.specLab.setText(text)
        self.ui.rateLab.setText(text)

    def empl_tree_items(self):

        try:
            if not self.ui.emplTree.currentItem().text(0) in \
                                        [x for _, x in self.show_spec()]:

                fio = self.ui.emplTree.currentItem().text(0)
                id_empl = self.ui.emplTree.currentItem().id_item

                self.ui.fioLab.setText(fio)

                self.ui.specLab.setText(self.ui.emplTree. \
                            currentItem().parent().text(0))

                if self.get_empl(id_empl) == []: return
                _, _, rental_date, rate, phone = tuple(self.get_empl(id_empl)[0])

                self.ui.dateLab.setText(str(rental_date))
                self.ui.rateLab.setText(str(rate))
                self.ui.phoneLab.setText(phone)
        except:
            pass

    def zakaz_tree(self):
        self.ui.specTable.clear()
        self.clean_timetable()

        for id_date, date_ in self.get_timetable():
            parent = QtWidgets.QTreeWidgetItem(self.ui.specTable)
            parent.setFlags(parent.flags())
            parent.setText(0, date_.strftime("%d.%m.%Y"))

            for id_time, time_ in self.get_working_ours():
                child = QtWidgets.QTreeWidgetItem(parent)
                child.setFlags(child.flags())
                child.setText(1, str(time_))

                for i in self.get_timetable_data(id_date, id_time):

                    if isinstance(i, tuple):
                        id_shedule, mark, model, gov_number, fio, name_zap = i
                        new_child = QtWidgets.QTreeWidgetItem(child)
                        new_child.setFlags(new_child.flags())

                        new_child.setText(2, gov_number)
                        new_child.setText(3, mark + ' ' + model)
                        new_child.setText(4, str(fio))
                        new_child.setText(5, str(id_shedule))

    def empl_tasks(self):
        pass

    def make_task(self):


        dialog = Add_Task(self.connection, self.cursor)
        self.uslugi()
        self.zakaz_tree()

    def delete_task_(self):

        msg = QtWidgets.QMessageBox()

        resp = msg.question(self.win, "Удаление задания", \
                        "Вы уверены что хотите удалить задание? ", msg.Yes|msg.No)

        if resp == msg.Yes:

            try:
                id_shedule = int(self.ui.specTable.currentItem().text(5))
                self.delete_task(id_shedule)

                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Удаление выполнено успешно!")
                msg.setWindowTitle("Удаление")

                self.zakaz_tree()

            except:
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Произошел сбой в удалении данных')
                msg.setWindowTitle("Ошибка")

            finally:
                msg.exec_()

    def clients_table(self):

        if not self.ui.clientTree.currentItem().text(0) in \
                                    [j for i in self.get_fam() for j in i]:

            id_cust = self.ui.clientTree.currentItem().id_item

            if self.get_cust(id_cust) == None: return
            fio, phone, orders = self.get_cust(id_cust)

            self.ui.fioCli.setText(fio)
            self.ui.phoneCli.setText(phone)
            self.ui.ordersCli.setText(orders)

            self.ui.clientTable.setRowCount(len(self.get_client_cars(id_cust)))

            for _id, item in enumerate(self.get_client_cars(id_cust)):

                self.ui.clientTable.setItem(_id, 0, \
                                        Ext_TableItem(item[0], item[3]))
                self.ui.clientTable.setItem(_id, 1, \
                                        QtWidgets.QTableWidgetItem(item[1]))
                self.ui.clientTable.setItem(_id, 2, \
                                        QtWidgets.QTableWidgetItem(item[2]))

    def get_status_z(self):

        try:
            id_cust = self.ui.clientTree.currentItem().id_item
            id_z = self.ui.clientTable.item(self.ui.clientTable.currentRow(), 0).id_item

            Order_status(self.connection, self.cursor, id_cust, id_z)
            self.clear_table()
            self.clients_table()
        except:
            pass

    def auxiliary(self):

        self.ui.emplTree.clear()
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

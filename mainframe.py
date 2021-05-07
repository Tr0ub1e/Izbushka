import traceback
from datetime import datetime
from PyQt5 import QtWidgets, QtGui
import decorators as ds
from myform import Ui_MainWindow
from db_tools import autowork_db
from add_usluga_dialog import Add_usluga
from add_spec_dialog import Add_specialization
from add_task_dialog import Add_Task
from connection_dialog import ConDial
from add_employee_dialog import EmpDial
from add_cust_dialog import CustDial
from add_auto_cust_dialog import AddAutoCust
from order_status_dialog import Order_status
from empl_history_dialog import History
from cars_inside_dial import Cars
from usluga_table_dialog import Usluga
from show_parts_dialog import Parts
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

    @ds.disconnect_
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
            msg.exec_()

        except Exception as e:
            print(e)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Выход выполнен не успешно")
            msg.setInformativeText("Возможно вы были неподключены к БД")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    @ds.connect_
    def raise_con_dialog(self):
        """
        Выводит диалог подключения к БД
        возвращает Подлючение и Курсор
        """
        try:
            if self.connection != None: return

            my_dial = ConDial()
            self.connection, self.cursor = my_dial.mainDial()
            my_dial.access_msg()

            self.employees()
            self.clients()
            self.uslugi()
            self.zakaz_tree()

        except Exception as e:
            print(traceback.format_exc())
            my_dial.error_msg()

    @ds.update_windows
    def raise_add_usluga(self):
        Add_usluga(self.connection, self.cursor, 'insert')

    @ds.update_windows
    def raise_change_usluga(self):

        msg = QtWidgets.QMessageBox()

        try:
            if self.ui.uslugiTree.currentItem().childCount() == 0:
                id_serv = self.ui.uslugiTree.currentItem().id_item
                Add_usluga(self.connection, self.cursor, 'update', id_serv)

            else:
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Нельзя изменять услуги с заказами")
                msg.setWindowTitle("Ошибка")
                msg.exec_()

        except Exception as e:
            print(e)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Вы не выбрали услугу")
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    @ds.update_windows
    def delete_usluga_(self):
        msg = QtWidgets.QMessageBox()

        resp = msg.question(self.win, "Удаление услуги", \
                        "Вы уверены что хотите удалить услугу? ", msg.Yes|msg.No)

        if resp == msg.Yes:

            try:
                if self.ui.uslugiTree.currentItem().childCount() == 0:
                    id_serv = self.ui.uslugiTree.currentItem().id_item
                    self.delete_usluga(id_serv)
                else:
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText("Нельзя удалять услуги с заказами")
                    msg.setWindowTitle("Ошибка")
                    msg.exec_()
            except Exception as e:
                raise
            else:
                pass

    def raise_show_parts(self):
        Parts(self.connection, self.cursor)

    def raise_show_cars(self):
        Cars(self.connection, self.cursor)

    def raise_show_usluga(self):
        Usluga(self.connection, self.cursor)

    def raise_show_empl_history(self):

        try:
            if not self.ui.emplTree.currentItem().text(0) \
                        in [name_spec for _, name_spec in self.show_spec()]:

                id_empl = self.ui.emplTree.currentItem().id_item
                History(self.connection, self.cursor, id_empl)
        except:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка")
            msg.setInformativeText('Вы не выбрали работника')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    @ds.update_windows
    def raise_add_spec(self):
        Add_specialization(self.connection, self.cursor, 'insert')

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

    @ds.update_windows
    def delete_spec(self):

        msg = QtWidgets.QMessageBox()

        resp = msg.question(self.win, "Удаление специальности", \
                        "Вы уверены что хотите удалить специальность? ", msg.Yes|msg.No)

        if resp == msg.Yes:

            try:
                id_spec = self.ui.emplTree.currentItem().id_item

                if self.ui.emplTree.currentItem().childCount() == 0:
                    self.del_spec(id_spec)

                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText("Удаление выполнено успешно!")
                    msg.setWindowTitle("Удаление")

                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText("Ошибка удаления")
                    msg.setInformativeText('Нельзя удалять занятые специальности')
                    msg.setWindowTitle("Ошибка")

            except:
                print(traceback.format_exc())
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Произошел сбой в удалении данных')
                msg.setWindowTitle("Ошибка")

            finally:
                msg.exec_()

    @ds.update_windows
    def raise_add_auto(self):
        try:
            fio = self.ui.clientTree.currentItem().text(0)
            id_client = self.ui.clientTree.currentItem().id_item

            my_dial = AddAutoCust(self.connection, self.cursor, id_client, fio)

        except:
            print(traceback.format_exc())
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Ошибка добавления")
            msg.setInformativeText('Вы не выбрали клиента')
            msg.setWindowTitle("Ошибка")
            msg.exec_()

    @ds.update_windows
    def raise_add_emp(self):
        """
        Выводит диалог добавления нового работника в БД
        """
        my_dial = EmpDial(self.show_spec(), self.connection, \
                                                    self.cursor, 'insert')

    def raise_change_empl(self):

        try:

            if not self.ui.emplTree.currentItem().text(0) \
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

    @ds.update_windows
    def raise_add_cust(self):
        """
        Выводит диалог добавления нового клиента
        """
        my_dial = CustDial(self.connection, self.cursor, "insert")

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

    @ds.update_windows
    def delete_empl(self):

        msg = QtWidgets.QMessageBox()

        resp = msg.question(self.win, "Удаление сотрудника", \
                        "Вы уверены что хотите удалить сотрудника? ", msg.Yes|msg.No)

        if resp == msg.Yes:

            try:
                id_empl = self.ui.emplTree.currentItem().id_item

                if self.ui.tasksTable.rowCount() != 0:
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText("Ошибка удаления")
                    msg.setInformativeText('Нельзя удалять работников с заданиями')
                    msg.setWindowTitle("Ошибка")

                    return

                self.delete_empl_by_id(id_empl)

                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Удаление выполнено успешно!")
                msg.setWindowTitle("Удаление")

            except:
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Произошел сбой в удалении данных')
                msg.setWindowTitle("Ошибка")

            finally:
                msg.exec_()

    @ds.update_windows
    def delete_cust(self):

        msg = QtWidgets.QMessageBox()

        resp = msg.question(self.win, "Удаление клиента", \
                        "Вы уверены что хотите удалить клиента? ", msg.Yes|msg.No)

        if resp == msg.Yes:

            try:
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

                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText("Удаление выполнено успешно!")
                    msg.setWindowTitle("Удаление")

            except:
                pass

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
        for id_, name in self.show_spec():
            parent = Ext_Item(self.ui.emplTree, id_)
            parent.setFlags(parent.flags())
            parent.setText(0, name)

            for fio, id_empl in self.emp_pos(name):
                child = Ext_Item(parent, id_empl)
                child.setText(0, "{}".format(fio))

        self.ui.emplTree.itemSelectionChanged.connect(self.empl_tree_items)

    def uslugi(self):
        self.ui.uslugiTree.clear()

        for id_serv, name_serv, _, _ in self.get_uslugi():

            parent = Ext_Item(self.ui.uslugiTree, id_serv)
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
        self.ui.tasksTable.setRowCount(0)

    def clear_labels(self):

        text = "NULL"

        self.ui.fioLab.setText(text)
        self.ui.dateLab.setText(text)
        self.ui.phoneLab.setText(text)
        self.ui.specLab.setText(text)
        self.ui.rateLab.setText(text)

        self.ui.phoneCli.setText(text)
        self.ui.ordersCli.setText(text)
        self.ui.fioCli.setText(text)

    def empl_tree_items(self):
        """
        Выводит данные о работнике
        """
        try:
            if not self.ui.emplTree.currentItem().text(0) in \
                                        [x for _, x in self.show_spec()]:

                self.empl_tasks()

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

        try:
            id_empl = self.ui.emplTree.currentItem().id_item
            self.ui.tasksTable.setRowCount(len(self.get_empl_tasks(id_empl)))

            for i, items in enumerate(self.get_empl_tasks(id_empl)):

                id_serv_z, *car, status_serv = items

                self.ui.tasksTable.setItem(i, 0, QtWidgets.QTableWidgetItem("Задание №{}".format(id_serv_z)))
                self.ui.tasksTable.setItem(i, 1, QtWidgets.QTableWidgetItem(' '.join(car)))
                self.ui.tasksTable.setItem(i, 2, QtWidgets.QTableWidgetItem(status_serv))

        except:
            print(traceback.format_exc())

    @ds.update_windows
    def make_task(self):
        Add_Task(self.connection, self.cursor)

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

        try:

            if not self.ui.clientTree.currentItem().text(0) in \
                                        [j for i in self.get_fam() for j in i]:

                id_cust = self.ui.clientTree.currentItem().id_item

                if self.get_cust(id_cust) == None: return
                fio, phone, orders = self.get_cust(id_cust)

                self.ui.fioCli.setText(fio)
                self.ui.phoneCli.setText(phone)
                self.ui.ordersCli.setText(str(orders))

                self.ui.clientTable.setRowCount(len(self.get_client_cars(id_cust)))

                for _id, item in enumerate(self.get_client_cars(id_cust)):

                    self.ui.clientTable.setItem(_id, 0, \
                                            Ext_TableItem(item[0], item[3]))
                    self.ui.clientTable.setItem(_id, 1, \
                                            QtWidgets.QTableWidgetItem(item[1]))
                    self.ui.clientTable.setItem(_id, 2, \
                                            QtWidgets.QTableWidgetItem(item[2]))
        except:
            pass

    @ds.update_windows
    def done_task_empl(self):

        msg = QtWidgets.QMessageBox()

        resp = msg.question(self.win, "Завершение задания", \
                        "Вы уверены что хотите завершить задание? ", msg.Yes|msg.No)

        if resp == msg.Yes:

            try:
                id_serv_z = self.ui.tasksTable.\
                    item(self.ui.tasksTable.currentRow(), 0).text()[len('Задание №'):]

                id_empl = self.ui.emplTree.currentItem().id_item

                self.finish_task(int(id_serv_z), id_empl)

                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Завершение выполнено успешно!")
                msg.setWindowTitle("Завершение")

                self.zakaz_tree()

            except:
                print(traceback.format_exc())
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Ошибка удаления")
                msg.setInformativeText('Произошел сбой в удалении данных')
                msg.setWindowTitle("Ошибка")

            finally:
                msg.exec_()

    @ds.update_windows
    def get_status_z(self):

        try:
            id_cust = self.ui.clientTree.currentItem().id_item
            id_z = self.ui.clientTable.item(self.ui.clientTable.currentRow(), 0).id_item

            Order_status(self.connection, self.cursor, id_cust, id_z)

        except:
            print(traceback.format_exc())

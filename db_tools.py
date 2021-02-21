from mysql.connector import connect, Error
from datetime import date
from PyQt5.QtCore import QDate, Qt

class autowork_db():

    host = 'localhost'
    __database = 'autowork'

    connection = None
    cursor = None

    def make_con(self, user, password):
        try:
            self.connection = connect(host=self.host, user=user,
                            password=password,
                            database=self.__database)

            self.cursor = self.connection.cursor()

            return self.connection, self.cursor

        except Error as e:
            print(e)

    def close_db(self):
        self.connection.close()

    def show_spec(self):

        querry = 'select * from specialization'
        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def show_employees(self):

        querry = 'select id_worker, fio, rental_date, rate, name_spec \
                  from employees, emp_pos, specialization \
                  where id_worker = id_empl and id_pos = id_spec'

        self.cursor.execute(querry)
        return self.cursor.fetchall()

    def insert_employees(self, fio, rental_date, rate, spec):

        querry = """
                    insert into autowork.employees
                    (fio, rental_date, rate)
                    values(%s, %s, %s)
                 """

        id_spec_q = """
                    select id_spec from autowork.specialization
                    where name_spec = %s
                    """

        id_empl_q = """
                    select id_empl from autowork.employees
                    where fio = %s and rental_date = %s and rate = %s
                    """

        emp_pos = """
                    insert into autowork.emp_pos(id_worker, id_pos)
                    values (%s, %s)
                  """
        #добавление нового человека
        self.cursor.execute(querry, (fio, rental_date.toString(Qt.ISODate), rate))
        self.connection.commit()

        #получение его ключа
        self.cursor.execute(id_empl_q, (fio, rental_date.toString(Qt.ISODate), rate))
        id_empl = self.cursor.fetchone()

        #получить ключ специальности
        self.cursor.execute(id_spec_q, (spec,))
        id_spec = self.cursor.fetchone()

        #связать со специальностями
        self.cursor.execute(emp_pos, (*id_empl, *id_spec))


    def show_customers(self):

        querry = 'select * from customer'
        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def insert_customers(self, fio, phone):

        querry = """
                    insert into customer(fio, phone)
                    values(%s, %s)
                 """

        self.cursor.execute(querry, (fio, phone))
        self.connection.commit()

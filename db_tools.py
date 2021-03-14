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

    def get_car(self, mark, model):

        querry = """
                select id_car from autowork.car
                where company = %s and model = %s
                """

        self.cursor.execute(querry, (mark, model))

        return self.cursor.fetchall()

    def get_fio(self, fam):

        querry = """
                select fio FROM autowork.customer
                where substring_index(fio, ' ', 1) = %s;
                """
                
        self.cursor.execute(querry, (fam,))

        return self.cursor.fetchall()

    def get_fam(self):
        querry = """
                select distinct substring_index(fio, ' ', 1)
                FROM autowork.customer
                 """

        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def get_name(self, fam):
        querry = """

        select distinct substring_index(substring_index(fio, ' ', 2), ' ', -1)
        FROM autowork.customer
        where substring_index(fio, ' ', 1) = %s

        """

        self.cursor.execute(querry, (fam,))

        return self.cursor.fetchall()

    def get_fath(self, fam, name):
        querry = """
        select distinct substring_index(fio, ' ', -1) FROM autowork.customer
        where
        substring_index(fio, ' ', 1) = %s and
	    substring_index(substring_index(fio, ' ', 2), ' ', -1) = %s
        """
        self.cursor.execute(querry, (fam, name))

        return self.cursor.fetchall()

    def get_phone(self, fam, name, fath):

        querry = """
                select phone from autowork.customer
                where fio = %s
                """

        fio = fam + ' ' + name + ' ' + fath

        self.cursor.execute(querry, (fio,))
        return self.cursor.fetchall()

    def insert_auto(self, id_client, id_auto, car_number):

        car_pos = """
                    insert into autowork.client_pos
                    (id_client, id_car, gov_number)
                    values (%s, %s, %s)
                  """

        self.cursor.execute(car_pos, (id_client, id_auto, car_number))
        self.connection.commit()

    def get_companies(self):

        querry = """
                 select company from autowork.car group by 1;
                 """
        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def get_models(self, company):

        querry = """
                 select model from autowork.car where company = %s
                 """
        self.cursor.execute(querry, (company,))

        return self.cursor.fetchall()

    def show_spec(self):

        querry = 'select * from specialization'
        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def emp_pos(self, name_spec):

        query = """
                select fio FROM autowork.employees join emp_pos
                on id_empl = id_worker
                join specialization
                on id_pos = id_spec
                where name_spec = %s
                """

        self.cursor.execute(query, (name_spec,))

        return self.cursor.fetchall()

    def show_employees(self):

        querry = """
                select fio, rental_date, rate, name_spec
                from employees join emp_pos on id_worker = id_empl
                join specialization on id_pos = id_spec
                """

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
        self.connection.commit()

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

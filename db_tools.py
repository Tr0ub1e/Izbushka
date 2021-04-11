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

    def get_client_cars(self, id_cust):

        query = """
            select
                    company, model, gov_number
            from
                autowork.client_pos
                join car using(id_car)
                join customer using(id_cust)
            where
                id_cust = %s
                """

        self.cursor.execute(query, (id_cust,))
        
        return self.cursor.fetchall()

    def get_car(self, mark, model):

        querry = """
                select id_car from autowork.car
                where company = %s and model = %s
                """

        self.cursor.execute(querry, (mark, model))

        return self.cursor.fetchone()

    def get_fio(self, fam):

        querry = """
                select id_cust, fio FROM autowork.customer
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

    def get_phone(self, id_cust):

        querry = """
                select phone from autowork.customer
                where id_cust = %s
                """
        self.cursor.execute(querry, (id_cust,))
        return self.cursor.fetchall()

    def insert_auto(self, id_cust, id_auto, car_number):

        car_pos = """
                    insert into autowork.client_pos
                    (id_cust, id_car, gov_number)
                    values (%s, %s, %s)
                  """

        self.cursor.execute(car_pos, (id_cust, id_auto, car_number))
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

    def get_id_spec(self, spec):

        querry = "select id_spec from specialization where name_spec = %s"

        self.cursor.execute(querry, (spec,))
        return self.cursor.fetchone()

    def emp_pos(self, name_spec):

        query = """
                select fio, id_empl FROM autowork.employees join emp_pos
                on id_empl = id_worker
                join specialization
                on id_pos = id_spec
                where name_spec = %s
                """

        self.cursor.execute(query, (name_spec,))

        return self.cursor.fetchall()

    def show_employees(self):

        querry = """
                select fio, rental_date, rate, name_spec, phone
                from employees join emp_pos on id_worker = id_empl
                join specialization on id_pos = id_spec
                """

        self.cursor.execute(querry)
        return self.cursor.fetchall()

    def get_empl(self, id_empl):

        querry = """
                select * from autowork.employees
                where id_empl = %s
                """

        self.cursor.execute(querry, (id_empl,))
        return self.cursor.fetchall()

    def get_id_empl(self, *args):

        querry = """
                select id_empl from employees join emp_pos on id_worker = id_empl
                join specialization on id_pos = id_spec
                where
                fio = %s and rental_date = %s and rate = %s and name_spec = %s
                and phone = %s
                """

        self.cursor.execute(querry, args)
        return self.cursor.fetchone()

    def update_empl(self, id_empl=None, id_pos=None, d={}):

        querry = ("update autowork.employees set ", " where id_empl = %s")
        pos = ("update autowork.emp_pos set id_pos = %s where id_worker = %s")

        #change spec
        if id_empl != None and id_pos != None:

            if not isinstance(id_empl, int) or not isinstance(id_pos, int):
                raise TypeError

            self.cursor.execute(pos, (id_pos, id_empl))
            self.connection.commit()

        if d != {}:

            for i in d.items():

            #change credintals
                _ = querry[0] + "{} = '{}'".format(*i)+querry[1]
                print(_)
                self.cursor.execute(_, (id_empl,))
                self.connection.commit()

    def delete_empl_by_id(self, id_empl):

        employees = "delete from employees where id_empl = %s"
        emp_pos = "delete from emp_pos where id_worker = %s"

        self.cursor.execute(employees, (id_empl,))
        self.cursor.execute(emp_pos, (id_empl,))
        self.connection.commit()

    def insert_employees(self, fio, rental_date, rate, spec, phone):

        querry = """
                    insert into autowork.employees
                    (fio, rental_date, rate, phone)
                    values(%s, %s, %s, %s)
                 """

        id_spec_q = """
                    select id_spec from autowork.specialization
                    where name_spec = %s
                    """

        id_empl_q = """
                    select id_empl from autowork.employees
                    where fio = %s and rental_date = %s and rate = %s
                    and phone = %s
                    """

        emp_pos = """
                    insert into autowork.emp_pos(id_worker, id_pos)
                    values (%s, %s)
                  """
        #добавление нового человека
        try:
            self.cursor.execute(querry, \
                          (fio, rental_date.toString(Qt.ISODate), rate, phone))
            self.connection.commit()

        except Exception as e:
            print(querry)
            print(e)

        #получение его ключа
        try:
            self.cursor.execute(id_empl_q, \
                          (fio, rental_date.toString(Qt.ISODate), rate, phone))
            id_empl = self.cursor.fetchone()

        except Exception as e:
            print(id_empl_q)
            print(e)

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

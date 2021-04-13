from mysql.connector import connect, Error
from datetime import date
from PyQt5.QtCore import QDate, Qt
from db_tools_empl import Employee_db
from db_tools_cust import Customer_db

class autowork_db(Employee_db, Customer_db):

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
                autowork.zakaz
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

    def insert_auto(self, id_cust, id_auto, car_number, date_z):

        car_pos = """
                    insert into autowork.zakaz
                    (id_cust, id_car, gov_number, date_z)
                    values (%s, %s, %s, %s)
                  """

        self.cursor.execute(car_pos, (id_cust, id_auto, car_number, date_z))
        self.connection.commit()

    def delete_auto(self, id_cust, car_number, date_z):

        querry = """
                delete from autowork.zakaz
                where
                    id_cust = %s and
                    gov_number = %s and
                    date_z = %s
                """

        self.cursor.execute(querry, (id_cust, car_number, date_z))
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

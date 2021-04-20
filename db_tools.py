from mysql.connector import connect, Error
from PyQt5.QtCore import QDate, Qt
import datetime
from db_tools_empl import Employee_db
from db_tools_cust import Customer_db
from db_tools_spec import Spec_db

class autowork_db(Employee_db, Customer_db, Spec_db):

    host = 'localhost'
    __database = 'autowork'

    connection = None
    cursor = None

    def make_con(self, user, password):
        try:
            self.connection = connect(host=self.host, user=user,
                            password=password,
                            database=self.__database)
                            #buffered=True)

            self.cursor = self.connection.cursor()

            return self.connection, self.cursor

        except Error as e:
            print(e)

    def close_db(self):
        self.connection.close()

    def insert_timetable(self, work_date):

        q = "insert into timetable_date(work_date) values(%s)"

        try:
            self.cursor.execute(q, (work_date,))
            self.connection.commit()
        except:
            return "date already exists"

    def insert_time(self, id_date, work_time, id_z):

        q = "insert into timetable_date_datetime(id_date, )"

    def get_timetable(self):

        q = "select * from timetable_date"

        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_working_ours(self):

        q = "select * from timetable_time"

        self.cursor.execute(q)
        return self.cursor.fetchall()

    def get_timetable_data(self, id_date, id_time):

        q = """select company, model, gov_number, fio, name_zap from timetable_date
                    join shedule_ using(id_date)
                    join timetable_time using(id_time)
                    join zakaz using(id_z)
                    join car using(id_car)
                    join employees using(id_empl)
                    join zapchasti_sklad using(id_zap)
            where
                id_time = %s and
                id_date = %s
            """
        self.cursor.execute(q, (id_time, id_date))
        return self.cursor.fetchall()

    def get_zapchasti_car(self, id_car):

        q = "select * from zapchasti_sklad where id_car = %s"

        self.cursor.execute(q, (id_car,))

        return self.cursor.fetchall()

    def get_uslugi(self):

        quarry = "select * from autowork.services"

        self.cursor.execute(quarry)

        return self.cursor.fetchall()

    def get_pending_uslugi(self, id_serv):

        q = "select * from services_z where id_serv = %s"

        self.cursor.execute(q, (id_serv,))
        return self.cursor.fetchall()

    def insert_uslugi_zakaz(self, id_z, id_serv, cost_serv, id_zap=None):

        q = """
            insert into services_z(id_z, id_serv, cost_serv, id_zap)
            values (%s, %s, %s, %s)
            """

        self.cursor.execute(q, (id_z, id_serv, cost_serv, id_zap))
        self.connection.commit()

    def insert_zap_zakaz(self, id_z, id_zap, kol_vo):

        q = """
            insert into zap_z(id_z, id_zap, kol_vo)
            values (%s, %s, %s)
            """

        self.cursor.execute(q, (id_z, id_zap, kol_vo))
        self.connection.commit()

    def get_client_cars(self, id_cust):

        query = """
                select
                    company, model, gov_number, id_z
                FROM autowork.zakaz
                    join services_z using(id_z)
                    join car using(id_car)
                where
                    id_cust = %s
                group by 3
                """
        self.cursor.execute(query, (id_cust,))
        return self.cursor.fetchall()

    def get_serv_stat(self, id_cust, id_z):

        query = """
            select
                name_serv, name_zap, status_serv
            FROM autowork.zakaz
                join services_z using(id_z)
                join services using(id_serv)
                left join zapchasti_sklad using(id_zap)
            where
                id_cust = %s and
                id_z = %s
                """
        self.cursor.execute(query, (id_cust, id_z))

        return self.cursor.fetchall()

    def get_more_serv_stat(self, id_cust, id_z):

        query = """
            select
                company, model, gov_number, enginecode,
                vincode, milleage, finish_date_z
            FROM autowork.zakaz
                join services_z using(id_z)
                join services using(id_serv)
                join car using(id_car)
                left join zapchasti_sklad using(id_zap)
            where
                id_cust = %s and
                id_z = %s
                """
        self.cursor.execute(query, (id_cust, id_z))

        return self.cursor.fetchall()

    def get_car(self, mark, model):

        querry = """
                select id_car from autowork.car
                where company = %s and model = %s
                """

        self.cursor.execute(querry, (mark, model))

        return self.cursor.fetchone()

    def insert_zakaz(self, id_cust, id_auto, car_number, duration,
                        vincode, enginecode, milleage):

        time = datetime.datetime.now()

        duration = list(map(int, duration.strftime("%H:%M:%S").split(':')))
        finish_date = time + datetime.timedelta(
                                    hours=duration[0], minutes=duration[1],
                                    seconds=duration[2]
                                    )

        car_pos = """
                    insert into autowork.zakaz
                    (id_cust, id_car, gov_number, date_z, finish_date_z,
                    vincode, enginecode, milleage)
                    values (%s, %s, %s, %s, %s, %s, %s, %s);
                  """

        self.cursor.execute(car_pos, (id_cust, id_auto, car_number,
                            time.strftime("%Y-%m-%d %H:%M:%S"),
                            finish_date.strftime("%Y-%m-%d %H:%M:%S"),
                            vincode, enginecode, milleage))
        self.connection.commit()

        return self.get_id_zakaz(id_cust, id_auto, car_number,
                                time.strftime("%Y-%m-%d %H:%M:%S"),
                                finish_date.strftime("%Y-%m-%d %H:%M:%S"),
                                vincode, milleage, enginecode)

    def get_id_zakaz(self, *args):

        get_id = """
                select id_z from autowork.zakaz as z
                where
                    z.id_cust = %s and
                    z.id_car = %s and
                    z.gov_number = %s and
                    z.date_z = %s and
                    z.finish_date_z = %s and
                    z.vincode = %s and
                    z.milleage = %s and
                    z.enginecode = %s;
                 """
        self.cursor.execute(get_id, args)
        return self.cursor.fetchone()

    def delete_auto(self, id_cust, id_auto, car_number, duration,
                        vincode, enginecode, milleage):

        querry = """
                delete from autowork.zakaz
                where
                    id_cust = %s and
                    id_car = %s and
                    gov_number = %s and
                    date_z = %s and
                    finish_date_z = %s and
                    vincode = %s and
                    milleage = %s and
                    enginecode = %s
                """

        self.cursor.execute(querry, (id_cust, id_auto, car_number, duration,
                            vincode, enginecode, milleage))
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

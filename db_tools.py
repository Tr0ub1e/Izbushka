from mysql.connector import connect, Error
from PyQt5.QtCore import QDate, Qt
import datetime
from db_tools_empl import Employee_db
from db_tools_cust import Customer_db
from db_tools_spec import Spec_db
from db_tools_timetable import Time_db

class autowork_db(Employee_db, Customer_db, Spec_db, Time_db):

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

    def insert_usluga(self, name_usluga, cost, duration):

        q = """
            insert into services(name_serv, price, duration)
            values(%s, %s, %s)
            """

        self.cursor.execute(q, (name_usluga, cost, duration))
        self.connection.commit()

    def update_usluga(self, id_serv, d={}):

        q = ("update(services) set ", "where id_serv = %s")

        for i in d.items():

            _ = q[0] + "{} = '{}'".format(*i)+q[1]

            self.cursor.execute(_, (id_serv,))
            self.connection.commit()

    def delete_usluga(self, id_serv):

        q = 'delete from services where id_serv = %s'

        self.cursor.execute(q, (id_serv,))
        self.connection.commit()

    def get_sum_z(self, id_z):
        q = """
            Select sum(price+ifnull(cost_zap, 0))
            from zakaz
	               join services_z using(id_z)
                   join services using(id_serv)
                   left join zapchasti_sklad using(id_zap)
                   where id_z = %s
            """
        self.cursor.execute(q, (id_z,))

        return self.cursor.fetchone()

    def get_zapchasti_car(self, id_car):

        q = "select * from zapchasti_sklad where id_car = %s"

        self.cursor.execute(q, (id_car,))

        return self.cursor.fetchall()

    def get_uslugi(self):

        quarry = "select * from autowork.services"

        self.cursor.execute(quarry)

        return self.cursor.fetchall()

    def get_zapchasti(self):
        q = 'select * FROM autowork.zapchasti_sklad join car using(id_car)'
        self.cursor.execute(q)

        return self.cursor.fetchall()

    def get_pending_uslugi(self, id_serv):
        q = """
               select
	               id_services_z, name_zap, finish_date_z, duration, id_zap
               from
	              services
                    join services_z using(id_serv)
                    join zakaz using(id_z)
                    left join zapchasti_sklad using(id_zap)
                where
                    status_serv = 'ожидание' and id_serv = %s
            """
        self.cursor.execute(q, (id_serv,))
        return self.cursor.fetchall()

    def get_pending_zakaz(self, id_serv):

        q = "select * from services_z where id_serv = %s"

        self.cursor.execute(q, (id_serv,))
        return self.cursor.fetchall()

    def insert_uslugi_zakaz(self, id_z, id_serv, id_zap=None):

        q = """
            insert into services_z(id_z, id_serv, id_zap)
            values (%s, %s, %s)
            """

        if id_zap != None:
            q2 = "update(zapchasti_sklad) \
                    set kol_vo_zap = kol_vo_zap - 1 \
                    where id_zap = %s"
            self.cursor.execute(q2, (id_zap,))
            self.connection.commit()

        self.cursor.execute(q, (id_z, id_serv, id_zap))
        self.connection.commit()

    def delete_task(self, id_shedule):

        q = "select id_empl, id_serv_z FROM shedule_ where id_shedule = %s"
        self.cursor.execute(q, (id_shedule,))

        id_empl, id_serv_z = self.cursor.fetchone()

        q = """insert into empl_tasks(id_empl, id_serv_z, status_serv, et_datetime)
            values(%s, %s, 'отменено', now())
            """
        self.cursor.execute(q, (id_empl, id_serv_z))
        self.connection.commit()

        q = "select s.id_serv_z from shedule_ as s where s.id_shedule = %s"
        self.cursor.execute(q, (id_shedule,))
        res = self.cursor.fetchone()

        q = "delete from shedule_ where id_shedule = %s"
        self.cursor.execute(q, (id_shedule,))
        self.connection.commit()

        q = "update(services_z) set status_serv = 'ожидание' \
                where id_services_z = %s"
        self.cursor.execute(q, res)
        self.connection.commit()

    def finish_zakaz(self, id_cust, id_z):

        q = 'call add_orders_c(%s)'
        self.cursor.execute(q, (id_cust,))
        self.delete_zakaz(id_z, True)

    def delete_zakaz(self, id_z, finish=False):

        q = [
            "insert into arch_zakaz select *, now(), 'завершен' from zakaz where id_z = %s",
            "insert into arch_services_z select *, now() from services_z where id_z = %s",
            "delete from zakaz where id_z = %s"
            ]

        if not finish:
            q[0] = "insert into arch_zakaz select *, now(), 'отменен' from zakaz where id_z = %s"

        for i in q:
            self.cursor.execute(i, (id_z,))
        self.connection.commit()

    def insert_shedule(self, id_date, id_time, id_serv_z, id_empl):

        q = """
            insert into
                shedule_(id_date, id_time, id_serv_z, id_empl)
            values(
                %s, %s, %s, %s
            )
            """
        self.cursor.execute(q, (id_date, id_time, id_serv_z, id_empl))
        self.connection.commit()

        q = """
            update(services_z)
            set status_serv = 'выполняется'
            where id_services_z = %s
            """

        self.cursor.execute(q, (id_serv_z,))
        self.connection.commit()


        q = """
            insert into empl_tasks(id_empl, id_serv_z, status_serv, et_datetime)
            values (%s, %s, %s, %s)
            """
        time_ = datetime.datetime.now()
        time_.strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(q, (id_empl, id_serv_z, 'выполняется', time_.strftime('%Y-%m-%d %H:%M:%S')))
        self.connection.commit()

    def get_id_shedule(self, id_date, id_time, id_serv_z, id_empl):

        id_shedule = """
            select id_shedule from shedule_
            where
                id_date = %s and id_time = %s
                and id_serv_z = %s and id_empl = %s
            """

        self.cursor.execute(q, (id_date, id_time, id_serv_z, id_empl))

        return self.cursor.fetchall()

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
                vincode, milleage, prod_year, date_z, finish_date_z
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
                        vincode, enginecode, milleage, prod_year):

        time = datetime.datetime.now()

        duration = list(map(int, duration.strftime("%H:%M:%S").split(':')))
        finish_date = time + datetime.timedelta(
                                    hours=duration[0], minutes=duration[1],
                                    seconds=duration[2]
                                    )

        car_pos = """
                    insert into autowork.zakaz
                    (id_cust, id_car, gov_number, date_z, finish_date_z,
                    vincode, enginecode, milleage, prod_year)
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                  """

        self.cursor.execute(car_pos, (id_cust, id_auto, car_number,
                            time.strftime("%Y-%m-%d %H:%M:%S"),
                            finish_date.strftime("%Y-%m-%d %H:%M:%S"),
                            vincode, enginecode, milleage, prod_year))
        self.connection.commit()

        return self.get_id_zakaz(id_cust, id_auto, car_number,
                                time.strftime("%Y-%m-%d %H:%M:%S"),
                                finish_date.strftime("%Y-%m-%d %H:%M:%S"),
                                vincode, milleage, enginecode, prod_year)

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
                    z.enginecode = %s and
                    z.prod_year = %s
                 """
        self.cursor.execute(get_id, args)
        return self.cursor.fetchone()

    def insert_car(self, mark, model):

        q = 'insert into autowork.car(company, model) values (%s, %s)'

        self.cursor.execute(q, (mark, model))

    def get_cars(self):

        q = 'select company, model, gov_number \
                    FROM autowork.zakaz join car using(id_car)'

        self.cursor.execute(q)

        return self.cursor.fetchall()

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

    def get_usl_print(self, id_z):

        q = """
            select id_serv, name_serv, count(name_serv) as kol_vo, duration, price, price*count(name_serv) as sum_
            FROM autowork.zakaz join services_z using(id_z) join services using(id_serv)
            where id_z = %s
            group by id_serv;
            """

        self.cursor.execute(q, (id_z,))

        return self.cursor.fetchall()

    def get_zap_print(self, id_z):

        q = """
            select id_zap, name_zap, count(*), cost_zap, cost_zap*count(*)
            from zakaz join services_z using(id_z) join zapchasti_sklad using(id_zap)
            where id_z = %s
            group by id_zap
            """

        self.cursor.execute(q, (id_z,))

        return self.cursor.fetchall()

    def get_work_print(self, id_z):

        q = """
            select sum(price) FROM autowork.services_z join services using(id_serv)
            where id_z = %s
            """
        self.cursor.execute(q, (id_z,))

        return self.cursor.fetchone()

    def get_part_print(self, id_z):

        q = """
            select sum(cost_zap) FROM autowork.services_z join zapchasti_sklad using(id_zap)
            where id_z = %s
            """
        self.cursor.execute(q, (id_z,))

        return self.cursor.fetchone()

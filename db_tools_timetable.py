from mysql.connector import connect, Error

class Time_db():

    connection = None
    cursor = None

    def insert_timetable(self, work_date):

        q = "insert into timetable_date(work_date) values(%s)"

        try:
            self.cursor.execute(q, (work_date,))
            self.connection.commit()

        except:
            pass

        finally:
            q = "select id_date from timetable_date where work_date = %s"
            self.cursor.execute(q, (work_date,))
            return self.cursor.fetchone()

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

        q = """select id_shedule, company, model, gov_number, fio, name_zap from timetable_date
                    join shedule_ using(id_date)
                    join services_z on id_services_z = id_serv_z
                    join timetable_time using(id_time)
                    join zakaz using(id_z)
                    join car using(id_car)
                    join employees using(id_empl)
                    left join zapchasti_sklad using(id_zap)
            where
                id_time = %s and
                id_date = %s
            """
        self.cursor.execute(q, (id_time, id_date))
        return self.cursor.fetchall()

    def clean_timetable(self):
        q = 'delete from timetable_date \
                where id_date not in (select id_date from shedule_)'

        self.cursor.execute(q)
        self.connection.commit()

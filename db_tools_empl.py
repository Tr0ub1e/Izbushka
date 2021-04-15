from mysql.connector import connect, Error

class Employee_db():

    connection = None
    cursor = None

    def show_employees(self):

        querry = """
                select fio, rental_date, rate, name_spec, phone
                from employees join emp_pos on id_worker = id_empl
                join specialization on id_pos = id_spec
                """

        self.cursor.execute(querry)
        return self.cursor.fetchall()

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

                self.cursor.execute(_, (id_empl,))
                self.connection.commit()

    def delete_empl_by_id(self, id_empl):

        employees = "delete from employees where id_empl = %s"
        emp_pos = "delete from emp_pos where id_worker = %s"

        self.cursor.execute(employees, (id_empl,))
        self.cursor.execute(emp_pos, (id_empl,))
        self.connection.commit()

    def get_empl(self, id_empl):

        querry = """
                select * from autowork.employees
                where id_empl = %s
                """

        self.cursor.execute(querry, (id_empl,))
        return self.cursor.fetchall()

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
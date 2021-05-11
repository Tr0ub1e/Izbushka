from mysql.connector import connect, Error

class Spec_db():

    connection = None
    cursor = None

    def show_spec(self):

        querry = 'select * from specialization'
        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def get_id_spec(self, spec):

        querry = "select id_spec from specialization where name_spec = %s"

        self.cursor.execute(querry, (spec,))
        return self.cursor.fetchone()

    def add_spec(self, name_spec):

        q = "insert into autowork.specialization(name_spec) values(%s)"

        self.cursor.execute(q, (name_spec,))
        self.connection.commit()

    def update_spec(self, old_name, new_name):

        q = 'update(specialization) set name_spec = %s where name_spec = %s'
        self.cursor.execute(q, (new_name, old_name))
        self.connection.commit()

    def del_spec(self, id_spec):

        q = "delete from specialization where id_spec = %s"

        self.cursor.execute(q, (id_spec,))
        self.connection.commit()

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

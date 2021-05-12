from mysql.connector import connect, Error

class Customer_db():

    connection = None
    cursor = None

    def show_customers(self):

        querry = 'select * from customer'
        self.cursor.execute(querry)

        return self.cursor.fetchall()

    def show_cust_arch(self, *args):

        if len(args) == 0:
            q = 'select * from arch_cust'
            self.cursor.execute(q)
        else:
            q = "select * from arch_cust \
                    where arch_date between %s and %s"

            start, stop = args
            self.cursor.execute(q, (start, stop))

        return self.cursor.fetchall()

    def delete_customer(self, id_cust):

        querry = """
                delete from autowork.customer
                where id_cust = %s
                """
        self.cursor.execute(querry, (id_cust,))
        self.connection.commit()

    def insert_customers(self, fio, phone):

        querry = """
                    insert into customer(fio, phone)
                    values(%s, %s)
                 """

        self.cursor.execute(querry, (fio, phone))
        self.connection.commit()

    def update_customers(self, id_cust, d={}):

        querry = ("update autowork.customer set ", " where id_cust = %s")

        if d != {}:

            for i in d.items():

                _ = querry[0] + "{} = '{}'".format(*i)+querry[1]

                self.cursor.execute(_, (id_cust,))
                self.connection.commit()

    def get_cust(self, id_cust):

        q = "select fio, phone, order_count from customer where id_cust = %s"

        self.cursor.execute(q, (id_cust,))

        return self.cursor.fetchone()

    def get_cust_id(self, fio, phone):

        querry = "select id_cust from autowork.customers \
                  where fio = %s and phone = %s"

        self.cursor.execute(querry, (fio, phone))

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

    def get_phone(self, id_cust):

        querry = """
                select phone from autowork.customer
                where id_cust = %s
                """
        self.cursor.execute(querry, (id_cust,))
        return self.cursor.fetchone()

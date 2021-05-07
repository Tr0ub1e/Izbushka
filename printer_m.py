from bs4 import BeautifulSoup

class Make_html():

    def __init__(self, start_date, end_date, car_data, usl_data, zap_data, money_data):

        self.car_data = car_data
        self.zap_data = zap_data
        self.money_data = money_data
        self.usl_data = usl_data
        self.start_date, self.end_date = start_date, end_date

        with open('testt2.html','r', encoding='utf-8') as file:
            page = file.read()

        self.soup = BeautifulSoup(page, 'html.parser')

    def save_file(self):

        self.insert_money_data(self.money_data)
        self.insert_car_data(self.start_date, self.end_date, self.car_data)
        self.insert_data(self.usl_data, self.zap_data)

        with open('res.html', 'w', encoding='utf-8') as file:
            file.write(str(self.soup))

    def insert_car_data(self, start_date, end_date, data):

        car, engine, year, gov_num, milliage, vin = data
        tags = self.soup.find_all('span')

        for i, d in enumerate(tags):
            if d.string == '00.00.00г':
                tags[i].string = ' '+start_date
                tags[i+3].string = ' '+end_date

            if d.string == 'Марка,модель ':
                d.string += ' '+car

            if d.string == 'Двигатель №':
                d.string += ' '+engine

            if d.string == 'Год выпуска':
                d.string += ' '+str(year)

            if d.string == 'Пробег':
                d.string = 'Пробег '+str(milliage)+' km'

            if d.string == 'Государственный  рег.номер':
                d.string += ' '+gov_num

            if d.string == 'VIN':
                d.string += ' '+vin

    def insert_money_data(self, data):

        nds_data = list(
                        map(lambda i:round(i, 3),
                            list(
                                map(lambda x: x*0.17, data)
                            )
                        )
                   )

        nds_data = list(map(str, nds_data))

        nds_work, nds_other, nds_zap = nds_data

        data = list(map(str, data))
        work_sum, other_sum, zap_sum = data

        tags = self.soup.find_all('span')

        for i, d in enumerate(tags):

            if d.string == 'работа_сум': d.string = work_sum

            if d.string == 'другое_сум': d.string = other_sum

            if d.string == 'запч_сум': d.string = zap_sum

            if d.string == 'всего_сум':
                d.string = str(sum(map(int, (work_sum, other_sum, zap_sum))))

            if d.string == 'работа_ндс': d.string = nds_work

            if d.string == 'другое_ндс': d.string = nds_other

            if d.string == 'запч_ндс': d.string = nds_zap

            if d.string == 'всего_ндс':
                d.string = str(sum(map(float, (nds_work, nds_other, nds_zap))))

            if d.string == 'сумма_ндс':
                d.string = str(sum(map(float, (work_sum, nds_work))))

            if d.string == 'другое_сум_ндс':
                d.string = str(sum(map(float, (other_sum, nds_other))))

            if d.string == 'запч_сум_ндс':
                d.string = str(sum(map(float, (zap_sum, nds_zap))))

            if d.string == 'всего_сум_ндс':
                d.string = str(sum(map(float, (
                            str(sum(map(int, (work_sum, other_sum, zap_sum)))),
                            str(sum(map(float, (nds_work, nds_other, nds_zap))))
                ))))

    def __gen_usluga_data(self, data):

        tags = self.soup.find_all('table')
        for i, d in enumerate(tags):
            for j, dd in enumerate(d.find_all('span')):
                if dd.string == 'Код работы':

                    for m in range(len(data)):
                        new_tr = self.soup.new_tag('tr')
                        self.__gen_table(new_tr, 6)
                        d.append(new_tr)
                    return

    def insert_data(self, usluga_data, parts_data):

        self.__gen_usluga_data(usluga_data)
        self.__gen_parts_data(parts_data)

        u = [x for i in usluga_data for x in i]
        p = [x for i in parts_data for x in i]

        tags = self.soup.find_all('table')
        for i, d in enumerate(tags):
            for j, dd in enumerate(d.find_all('span')):
                if i == 2 and dd.string == 'NEW ITEM':
                    d.find_all('span')[j].string = ' '+str(u[0])
                    u.remove(u[0])

                if i == 3 and dd.string == 'NEW ITEM':
                    d.find_all('span')[j].string = ' '+str(p[0])
                    p.remove(p[0])

    def __gen_parts_data(self, data):
        tags = self.soup.find_all('table')
        for i, d in enumerate(tags):
            for j, dd in enumerate(d.find_all('span')):
                if dd.string == 'Код запчасти':

                    for m in range(len(data)):
                        new_tr = self.soup.new_tag('tr')
                        self.__gen_table(new_tr, 5)
                        d.append(new_tr)
                    return

    def __gen_table(self, tr, columns):
        for k in range(columns):

            td = self.soup.new_tag('td')
            td['style'] = "vertical-align:top; padding-left:0; padding-right:0; padding-top:0; padding-bottom:0;"

            p = self.soup.new_tag('p')
            p['style'] = " margin-top:12px; margin-bottom:12px; margin-left:0px; \
                            margin-right:0px; -qt-block-indent:0; text-indent:0px;"

            span = self.soup.new_tag('span')
            span['style'] = " font-size:8pt;"
            span.string = 'NEW ITEM'

            p.append(span)
            td.append(p)
            tr.append(td)
        return tr

if __name__ == '__main__':

    Make_html().save_file()

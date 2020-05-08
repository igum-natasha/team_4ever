import csv
import requests
import datetime
from pymongo import MongoClient
import pandas as pd


class WorkWithCsvTable:
    def __init__(self, data):
        self.data = data

    def write_table(self, file_name):
        with open(file_name, 'w') as file:
            fieldnames = []
            for i in self.data:
                for keys in i.keys():
                    if keys not in fieldnames:
                        fieldnames.append(keys)
            writer = csv.DictWriter(file, fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def read_table(self, file_name):
        with open(file_name, 'r') as file:
            table = csv.DictReader(file)
            for row in table:
                array = {}
                for key in row.keys():
                    array[key] = row[key]
                self.data.append(array)

    def get_data(self):
        return self.data


class WorkWithCoronaData:
    def __init__(self, prov, count, data1, table, now, day):
        self.prov = prov
        self.count = count
        self.data1 = data1
        self.table = table
        self.now = now
        self.day = day

    def get_table(self):

        self.data1 = datetime.date.today()
        self.data1 = self.data1.strftime("%Y-%m-%d").split('-')
        while True:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/' \
                f'csse_covid_19_daily_reports/{self.data1[1]}-{self.data1[2]}-{self.data1[0]}.csv'
            r = requests.get(url, allow_redirects=True)

            if r.status_code != 200:
                self.data1 = datetime.date(int(self.data1[0]), int(self.data1[1]), int(self.data1[2]))
                day = datetime.timedelta(days=self.day + 1)
                self.data1 -= day
            else:
                break
            self.data1 = str(self.data1).split('-')
        with open('google.csv', 'wb') as corona:
            corona.write(r.content)
        data_new = WorkWithCsvTable(data=[])
        data_new.read_table("google.csv")
        self.table = data_new.data
        '''if int(self.data1[1]) < 10:
            self.data1[1] = '0' + str(int(self.data1[1]) - 1)
        else:
            self.data1[1] = str(int(self.data1[1]) - 1)'''

    def provinces(self):
        self.get_table()
        self.prov = [{'Province_State': [row['Country_Region'], row['Province_State'], int(row['Active'])]}
                     for row in self.table if int(row['Active']) != 0 and row['Province_State'] != '']
        self.count = [int(row['Active']) for row in self.table
                      if int(row['Active']) != 0 and row['Province_State'] != '']
        self.count.sort(reverse=True)

    def corona_dynamics(self):
        self.get_table()
        k = 0
        buf = []
        for row in self.table:
            if int(row['Active']) != 0 and row["Country_Region"] not in buf:
                buf.append(row["Country_Region"])
                self.now[k] = [row["Country_Region"],
                               int(row['Confirmed']),
                               int(row['Deaths']),
                               int(row['Recovered']),
                               int(row["Active"])]
                self.count[k] = int(row['Active'])
                k += 1
            elif int(row['Active']) != 0 and row["Country_Region"] in buf:
                for key, value in self.now.items():
                    if value[0] == row["Country_Region"]:
                        self.now[key] = [row["Country_Region"],
                                         value[1] + int(row['Confirmed']),
                                         value[2] + int(row['Deaths']),
                                         value[3] + int(row['Recovered']),
                                         value[4] + int(row["Active"])]
                        self.count[key] = value[4] + int(row["Active"])
        self.count.sort(reverse=True)

    def corona_russia(self):
        self.get_table()
        k = 0
        for row in self.table:
            if row["Country_Region"] == "Russia":
                self.now[k] = [row["Country_Region"],
                               int(row['Confirmed']),
                               int(row['Deaths']),
                               int(row['Recovered']),
                               int(row["Active"])]


class Website:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        r = requests.get(self.url)
        r.encoding = "utf-8"
        if r.status_code == 200:
            return r.json()
        else:
            return None


class WriteDb:
    def __init__(self):
        self.client = MongoClient()
        self.file = ''
        self.data = []

    def write_db(self, day: str, db_name: str):
        db = self.client[db_name]
        if day not in db.list_collection_names():
            day = db[day]
            df = pd.read_csv(self.file)
            records_ = df.to_dict(orient='records')
            day.insert_many(records_)

    def find_doc(self, day: str, db_name: str):
        db = self.client[db_name]
        if day in db.list_collection_names():
            results = 1
        else:
            results = -1
        for x in db[day].find():
            self.data.append(x)
        if results != -1:
            return self.data
        return 0

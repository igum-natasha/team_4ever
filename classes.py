import csv
import requests
import datetime
class WorkWithCsvTable():
    @staticmethod
    def write_table(file_name):
        data=[]
        with open(file_name, 'wb') as file:
            writer = csv.DictWriter(file)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    @staticmethod
    def read_table(file_name):
        data=[]
        with open(file_name, 'r') as file:
            table=csv.DictReader(file)
            for row in table:
                array = {}
                for key in row.keys():
                    array[key] = row[key]
                data.append(array)
        return data

class WorkWithCoronaData(WorkWithCsvTable):
    def __init__(self):
        self.table=[]
    def get_table(self):
        data = str(datetime.date.today())
        data1 = data.split('-')
        day = 0
        while True:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{data1[1]}-{int(data1[2]) - day}-{data1[0]}.csv'
            r = requests.get(url, allow_redirects=True)
            if r.status_code != 200:
                day += 1
            else:
                break
        corona = open('google.csv', 'wb')
        corona.write(r.content)
        corona.close()
        self.table=WorkWithCsvTable.read_table('google.csv')

    @staticmethod
    def Provinces(prov,count):
        table = WorkWithCsvTable.read_table('google.csv')
        for row in table:
             if int(row['Active']) != 0:
                if row['Province_State'] != '':
                    prov[f"{row['Province_State']}"] = int(row['Active'])
                else:
                    prov[f"{row['Country_Region']}"] = int(row['Active'])
                count.append(int(row['Active']))
        count.sort(reverse=True)

class Website():
    @staticmethod
    def get_data(url):
        r = requests.get(url)
        r.encoding = "utf-8"
        s = r.json()
        return s

s=Website.get_data('https://cat-fact.herokuapp.com/facts')
ma = 0
all=s['all']
print(all)



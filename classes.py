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
    @staticmethod
    def get_table(data):
        data1 = datetime.date.today()
        data1 = data1.strftime("%m-%d-%Y").split('-')
        while True:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{data1[0]}-{data1[1]}-{data1[2]}.csv'
            r = requests.get(url, allow_redirects=True)
            if r.status_code != 200:
                if int(data1[1]) < 10:
                    data1[1] = '0' + str(int(data1[1]) - 1-data)
                else:
                    data1[1] = str(int(data1[1]) - 1-data)
            else:
                break
        corona = open('google.csv', 'wb')
        corona.write(r.content)
        corona.close()
        table=WorkWithCsvTable.read_table('google.csv')
        if int(data1[1]) < 10:
            data1[1] = '0' + str(int(data1[1]) - 1)
        else:
            data1[1] = str(int(data1[1]) - 1)
        return data1

    @staticmethod
    def provinces(prov,count):
        WorkWithCoronaData.get_table()
        table=WorkWithCsvTable.read_table('google.csv')
        for row in table:
             if int(row['Active']) != 0:
                if row['Province_State'] != '':
                    prov[f"{row['Province_State']}"] = int(row['Active'])
                else:
                    prov[f"{row['Country_Region']}"] = int(row['Active'])
                count.append(int(row['Active']))
        count.sort(reverse=True)

    @staticmethod
    def corona_dynamics(data,count):
        WorkWithCoronaData.get_table(data)
        table = WorkWithCsvTable.read_table('google.csv')
        now={}
        k=0
        buf=[]
        for row in table:
            if int(row['Active'])!=0  and row["Country_Region"] not in buf:
                buf.append(row["Country_Region"])
                now[k]=[row["Country_Region"],
                 int(row['Confirmed']),
                 int(row['Deaths']),
                 int(row['Recovered']),
                 int(row["Active"])]
                count[k]=int(row['Active'])
                k += 1
            elif int(row['Active'])!=0 and row["Country_Region"] in buf:
                for key,value in now.items():
                    if value[0]==row["Country_Region"]:
                        now[key] = [row["Country_Region"],
                                  value[1]+int(row['Confirmed']),
                                  value[2]+int(row['Deaths']),
                                  value[3]+int(row['Recovered']),
                                  value[4]+int(row["Active"])]
                        count[key] = value[4]+int(row["Active"])


        count.sort(reverse=True)
        return now

class Website():
    @staticmethod
    def get_data(url):
        r = requests.get(url)
        r.encoding = "utf-8"
        s = r.json()
        return s



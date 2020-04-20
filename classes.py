import csv
import requests
import datetime
class WorkWithCsvTable():
    def __init__(self):
        self.data=[]
    def write_table(self,file_name):
        with open(file_name, 'wb') as file:
            fieldnames=[]
            for i in self.data:
                for keys in i.keys():
                    fieldnames.append(keys)
            writer = csv.DictWriter(file,fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)

    def read_table(self,file_name):
        with open(file_name, 'r') as file:
            table=csv.DictReader(file)
            for row in table:
                array = {}
                for key in row.keys():
                    array[key] = row[key]
                self.data.append(array)
    def get_data(self):
        return self.data

class WorkWithCoronaData:
    def __init__(self,prov,count,data1,table,now,day):
        self.prov=prov
        self.count=count
        self.data1=data1
        self.table=table
        self.now=now
        self.day=day
    def get_table(self):

        self.data1 = datetime.date.today()
        self.data1 = self.data1.strftime("%m-%d-%Y").split('-')
        while True:
            url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{self.data1[0]}-{self.data1[1]}-{self.data1[2]}.csv'
            r = requests.get(url, allow_redirects=True)
            if r.status_code != 200:
                if int(self.data1[1]) < 10:
                    self.data1[1] = '0' + str(int(self.data1[1]) - 1-self.day)
                else:
                    self.data1[1] = str(int(self.data1[1]) - 1-self.day)
            else:
                break
        with open('google.csv', 'wb') as corona:
            corona.write(r.content)
        data_new=WorkWithCsvTable()
        data_new.read_table("google.csv")
        self.table=data_new.get_data()
        if int(self.data1[1]) < 10:
            self.data1[1] = '0' + str(int(self.data1[1]) - 1)
        else:
            self.data1[1] = str(int(self.data1[1]) - 1)


    def provinces(self):
        self.get_table()
        for row in self.table:
             if int(row['Active']) != 0:
                if row['Province_State'] != '':
                    self.prov[f"{row['Province_State']}"] = int(row['Active'])
                else:
                    self.prov[f"{row['Country_Region']}"] = int(row['Active'])
                self.count.append(int(row['Active']))
        self.count.sort(reverse=True)

    def corona_dynamics(self):
        self.get_table()
        k=0
        buf=[]
        for row in self.table:
            if int(row['Active'])!=0  and row["Country_Region"] not in buf:
                buf.append(row["Country_Region"])
                self.now[k]=[row["Country_Region"],
                 int(row['Confirmed']),
                 int(row['Deaths']),
                 int(row['Recovered']),
                 int(row["Active"])]
                self.count[k]=int(row['Active'])
                k += 1
            elif int(row['Active'])!=0 and row["Country_Region"] in buf:
                for key,value in self.now.items():
                    if value[0]==row["Country_Region"]:
                        self.now[key] = [row["Country_Region"],
                                  value[1]+int(row['Confirmed']),
                                  value[2]+int(row['Deaths']),
                                  value[3]+int(row['Recovered']),
                                  value[4]+int(row["Active"])]
                        self.count[key] = value[4]+int(row["Active"])
        self.count.sort(reverse=True)

    def corona_russia(self):
        self.get_table()
        k = 0
        for row in self.table:
            if row["Country_Region"]=="Russia":
                self.now[k] = [row["Country_Region"],
                          int(row['Confirmed']),
                          int(row['Deaths']),
                          int(row['Recovered']),
                          int(row["Active"])]



class Website:
    def __init__(self,url):
        self.url=url

    def get_data(self):
        try:
            r = requests.get(self.url)
            r.encoding = "utf-8"
            if r.status_code==200:
                return r.json()
        except Exception as exc:
            print(f'Error {exc}')



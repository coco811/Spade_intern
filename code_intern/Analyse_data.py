import csv
import pandas as pd

class data_site():
    def __init__(self,file):
        self.file=file
        self.df=None

    def read_data_site(self):
        self.df = pd.read_csv(self.file, parse_dates=True)


    def write_new_csv_hourly(self):
        with open('Hourly_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            head=["Date","T Fortress","RH Fortress","Ws Fortress","Wd Fortress","T junction","RH junction","Ws Junction","Wd Junction","T Nipika","RH Nipika","Ws Nipika","Wd Nipika"]
            writer.writerow(head)
            for i in range(int(len(self.df[:])/12)+1):
                data_1_hour = self.df[0+i*12:12+i*12]
                data_to_add=[]
                for j in range(int(len(self.df.columns))):
                    a=data_1_hour[head[j]]
                    if j==0:
                        data_to_add.append(self.df['Date'][0+i*12])
                    else:
                        data_to_add.append(a.mean())
                writer.writerow(data_to_add)



    def __call__(self):
        self.read_data_site()
        self.write_new_csv_hourly()

class get_simul():
    def __init__(self,file):
    self.file=file





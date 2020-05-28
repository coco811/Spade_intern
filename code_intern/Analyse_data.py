import csv
import pandas as pd
from code_intern import plot_function as plt_func
idex_temps=[]
import datetime
import numpy as np
from netCDF4 import num2date
import matplotlib.pyplot as plt
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

class data_site():
    def __init__(self,file_csv,data):
        self.file=file_csv
        self.df=None
        self.data = data
        self.position_site = [(50.82423333, -115.1972167), (50.785568, -115.160941),
                              (50.61183889, -115.8008167)]  # lat,long
        self.index_storm = plt_func.plot_graph(self.data).get_index_storm()
        self.index_site = []
        self.temp_3_site = []

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
                        date_time_str = self.df['Date'][0 + i * 12]
                        datetime_str = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                        data_to_add.append(datetime_str)
                    else:
                        data_to_add.append(a.mean())
                writer.writerow(data_to_add)

    def get_site_index(self):
        lon=self.data['lon'][:]
        lat=self.data['lat'][:]
        for i in self.position_site:
            array_near =np.sqrt( np.square( lat - i[0] ) +  np.square( lon - i[1]  ) )
            idx = np.where( array_near == array_near.min())
            self.index_site.append((idx[0][0],idx[1][0]))

    def get_array_temperature_simul(self):


        for i in range(len(self.index_site)):
            tempe = self.data['tas'][:, self.index_site[i][0], self.index_site[i][1]]
            self.temp_3_site.append(tempe.data)


    def date(self):
        times = self.data.variables['time'][:]
        idx = pd.date_range(start='2019-04-15 01:00:00', freq='H', periods=len(times))
        return idx

    def get_time_temps_lenght(self):
        df = pd.read_csv('Hourly_data.csv', parse_dates=['Date'])
        array_simul=self.date()
        start=np.where(array_simul==df['Date'][0])[0][0]

        end=np.where(array_simul==df['Date'][len(df['Date'])-1])[0][0]
        for i in range(len(self.temp_3_site)):
            self.temp_3_site[i]=self.temp_3_site[i][start:end+1]-273.15

        # for i in range(len(df['Date']))):
        #     pass


    def plot(self):
        site = ['Fortress', 'junction', 'Nipika']
        df = pd.read_csv('Hourly_data.csv', parse_dates=['Date'])
        # fig = plt.figure(facecolor='white', figsize=(10, 4), dpi=300)

        for i in range(len(self.temp_3_site)):
            fig = plt.figure(facecolor='white')
            ax = plt.subplot(1, 1, 1)
            ax.plot(df['Date'],self.temp_3_site[i],label=f'Simulation {site[i]}')
            ax.plot(df['Date'],df[f'T {site[i]}'], label=f'Terrain data {site[i]}')
            plt.legend()
            plt.show()

    def __call__(self):
        self.read_data_site()
        # self.write_new_csv_hourly()
        self.get_site_index()
        self.get_array_temperature_simul()
        self.get_time_temps_lenght()
        self.plot()







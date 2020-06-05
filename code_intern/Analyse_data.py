import csv
import pandas as pd
from code_intern import plot_function as plt_func
idex_temps=[]
import datetime
import numpy as np
import scipy.stats.mstats as stat
from netCDF4 import num2date
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

class data_site():
    def __init__(self,file_csv,data,**kwargs):
        self.file=file_csv
        self.df=None
        self.data = data
        self.position_site = [(50.82423333, -115.1972167), (50.785568, -115.160941),
                              (50.61183889, -115.8008167)]  # lat,long
        self.index_storm = plt_func.plot_graph(self.data).get_index_storm()
        self.index_site = []
        self.data_simul_3_site = []
        self.data_aff = kwargs.get("Data_aff", 'temperature')
        self.topo=np.load('SPADE_dm_array.npy')
        self.topo_site={'Fortress':2076, 'junction':1580, 'Nipika':1087}

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
        site = ['Fortress', 'junction', 'Nipika']
        for i in range(len(self.position_site)):
            array_near =np.sqrt( np.square( lat - self.position_site[i][0] ) +  np.square( lon - self.position_site[i][1]  ) )
            idx = np.where( array_near == array_near.min())

            topo=self.topo[idx[0][0]-3:idx[0][0]+3,idx[1][0]-3:idx[1][0]+3]
            # print(topo)
            altitude = self.topo_site[site[i]]
            array_near_2 = abs(topo - altitude)
            idx_2 = np.where(array_near_2 == array_near_2.min())
            print(altitude-self.topo[idx[0][0]-3+idx_2[0][0],idx[1][0]-3+idx_2[1][0]])
            self.index_site.append((idx[0][0]-3+idx_2[0][0],idx[1][0]-3+idx_2[1][0]))


    def get_array_simul(self):
        if self.data_aff == 'temperature':
            for i in range(len(self.index_site)):
                tempe = self.data['tas'][:, self.index_site[i][0], self.index_site[i][1]]-273.15
                self.data_simul_3_site.append(tempe.data)
        if self.data_aff == 'precipitation':
            for i in range(len(self.index_site)):
                precip = self.data['pr'][:, self.index_site[i][0], self.index_site[i][1]]*3600
                self.data_simul_3_site.append(precip.data)
        if self.data_aff == 'pression':
            for i in range(len(self.index_site)):
                precip = self.data['pr'][:, self.index_site[i][0], self.index_site[i][1]]*3600
                self.data_simul_3_site.append(precip.data)
    def date(self):
        times = self.data.variables['time'][:]
        idx = pd.date_range(start='2019-04-15 01:00:00', freq='H', periods=len(times))
        return idx

    def get_time_temps_lenght(self):
        df = pd.read_csv('/Users/olivier1/Documents/GitHub/Spade_intern/pluvio_data_analyse/Hourly_data.csv.nosync.csv', parse_dates=['Date'])
        array_simul=self.date()
        start=np.where(array_simul==df['Date'][0])[0][0]

        end=np.where(array_simul==df['Date'][len(df['Date'])-1])[0][0]
        for i in range(len(self.data_simul_3_site)):
            self.data_simul_3_site[i]=self.data_simul_3_site[i][start:end+1]



    def scatter_plot(self):
        site = ['Fortress', 'junction', 'Nipika']
        df = pd.read_csv('/Users/olivier1/Documents/GitHub/Spade_intern/pluvio_data_analyse/Hourly_data.csv.nosync.csv',
                         parse_dates=['Date'])
        for i in range(len(self.data_simul_3_site)):
            fig = plt.figure(facecolor='white')
            # fig = plt.figure(facecolor='white',figsize=(10,10), dpi=300)
            ax = plt.subplot(1, 1, 1)

            y=df[f'T {site[i]}']
            x=self.data_simul_3_site[i]
            X = sm.add_constant(x)
            model = sm.OLS(y, X, missing='drop')
            results = model.fit()

            plt.plot(self.data_simul_3_site[i],self.data_simul_3_site[i]*results.params[1]+results.params[0], 'r', label='fitted line')
            plt.plot(self.data_simul_3_site[i], self.data_simul_3_site[i], 'k',
                     label='1:1')
            ax.scatter(self.data_simul_3_site[i], df[f'T {site[i]}'], label='original data')
            plt.text(-7, 16,f'R$^2$={results.rsquared:.3f}')
            ax.set_xlabel(f'Simulation temperature {site[i]} (\u2103)')
            ax.set_ylabel(f'Temperature {site[i]} (\u2103)')
            ax.set_ylim([-15, 30])
            ax.set_xlim([-15, 30])
            plt.legend(loc='upper left')


            plt.savefig(f'Analyse_scatter_fit_{site[i]}_lowres.nosync.png', bbox_inches='tight')


    def plot(self):
        site = ['Fortress', 'junction', 'Nipika']
        df = pd.read_csv('/Users/olivier1/Documents/GitHub/Spade_intern/pluvio_data_analyse/Hourly_data.csv.nosync.csv', parse_dates=['Date'])
        for i in range(len(self.data_simul_3_site)):
            fig = plt.figure(facecolor='white', figsize=(10, 4), dpi=300)
            ax = plt.subplot(1, 1, 1)

            event = pd.read_csv("dates_of_storms.csv.nosync.csv", parse_dates=True)
            for j in range(len(event['number'])):
                debut = event['start'][event['number'][j] - 1]
                fin = event['finish'][event['number'][j] - 1]
                plt.axvspan(mdates.datestr2num([debut]),mdates.datestr2num([fin]), color='grey', alpha=0.2)

            ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
            ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d/%m"))
            ax.set_xlabel('Date')

            ax.plot(df['Date'],self.data_simul_3_site[i],label=f'Simulation {site[i]}',linewidth=0.5)
            if self.data_aff == 'precipitation':
                data_h_site = pd.read_csv(f'/Users/olivier1/Documents/GitHub/Spade_intern/pluvio_data_analyse/Hourly_data_pr_{site[i]}.csv.nosync', parse_dates=['Date'])
                ax.set_ylim([-0.2, 19])
                ax.set_ylabel('Precipitation (mm) ')
                ax.plot(data_h_site['Date'],data_h_site[f'Acc'], label=f'Data {site[i]}', linewidth=0.5)
                plt.legend(bbox_to_anchor=(0.55, -0.2, 0.2, 0.1), loc='lower left',
                           ncol=2, borderaxespad=0., prop={'size': 8})
                plt.savefig(f'comparasion_pre{site[i]}.png', bbox_inches='tight')

            if self.data_aff == 'temperature':
                ax.set_ylim([-15, 30])
                ax.set_ylabel('Temperature (\u2103) ')
                ax.plot(df['Date'],df[f'T {site[i]}'], label=f'Data {site[i]}',linewidth=0.5)
                plt.legend(bbox_to_anchor=(0.55, -0.2, 0.2, 0.1), loc='lower left',
                           ncol=2, borderaxespad=0., prop={'size': 8})
                plt.savefig(f'comparasion_temp{site[i]}.png', bbox_inches='tight')

            if self.data_aff == 'pression':
                ax.set_ylim([-15, 30])
                ax.set_ylabel('pression (hpa) ')
                ax.plot(df['Date'], df[f'T {site[i]}'], label=f'Data {site[i]}', linewidth=0.5)
                plt.legend(bbox_to_anchor=(0.55, -0.2, 0.2, 0.1), loc='lower left',
                           ncol=2, borderaxespad=0., prop={'size': 8})
                plt.savefig(f'comparasion_temp{site[i]}.png', bbox_inches='tight')




    def __call__(self):
        if self.data_aff=='temperature':
            self.read_data_site()
            # self.write_new_csv_hourly()
            self.get_site_index()
            # self.get_altitude_similar()
            self.get_array_simul()
            self.get_time_temps_lenght()
            self.plot()
            self.scatter_plot()
        if self.data_aff == 'precipitation':
            self.read_data_site()
            # self.write_new_csv_hourly()
            self.get_site_index()
            self.get_array_simul()
            self.get_time_temps_lenght()
            self.plot()




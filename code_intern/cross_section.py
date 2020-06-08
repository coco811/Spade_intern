import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap


class cross_section():
    def __init__(self, file_csv, data, **kwargs):
        self.file = file_csv
        self.data = data
        self.position_site = [(50.82423333, -115.1972167), (50.785568, -115.160941),
                              (50.61183889, -115.8008167)]  # lat,long
        self.index_site = []
        self.lats = self.data.variables['lat'][:, :]
        self.lons = self.data.variables['lon'][:, :]
        self.domaine = {}
        self.Cen_lat = 0
        self.Cen_lon = 0
        self.extent = []
        self.get_domaine()
        self.loc = {'Powerline_loc': [50.82423333, -115.1972167], 'Junction_loc': [50.785568, -115.160941],
                    'Nipika_loc': [50.61183889, -115.8008167], 'Storm_Lodge_loc': [51.25283667, -115.9988733],
                    'BGI_loc': [51.026681, -115.034411]}
        self.map = Basemap(llcrnrlon=-116.5, llcrnrlat=50.5, urcrnrlon=-114.5, urcrnrlat=51.5, resolution='l',
                           projection='lcc', lat_0=self.Cen_lat, lon_0=self.Cen_lon)
        self.ndat = 17
        self.dist_ndat = np.arange((self.ndat))
        self.dist_km = self.dist_ndat * 3

        self.xy = {}
        self.topo = np.load('SPADE_dm_array.npy')
        self.data_aff = {'II': np.zeros((self.ndat)), 'JJ': np.zeros((self.ndat)), 'TOPO': np.zeros((self.ndat)),
                         'longc': np.zeros((self.ndat)), 'latgc': np.zeros((self.ndat))}

    def get_domaine(self):
        self.domaine = {'LL_lat': self.lats[0][0], 'LL_lon': self.lons[0][0], 'UL_lat': self.lats[-1][0],
                        'UL_lon': self.lons[-1][0],
                        'LR_lat': self.lats[0][-1], 'LR_lon': self.lons[0][-1], 'UR_lat': self.lats[-1][-1],
                        'UR_lon': self.lons[-1][-1]}
        self.Cen_lat = self.domaine['LL_lat'] + ((self.domaine['UL_lat'] - self.domaine['LL_lat']) / 2)
        self.Cen_lon = self.domaine['LL_lon'] + ((abs(self.domaine['LL_lon']) - abs(self.domaine['LR_lon'])) / 2)
        self.extent = [self.domaine['UL_lon'], self.domaine['LR_lon'], self.domaine['LL_lat'], self.domaine['UR_lat']]
        self.map = Basemap(llcrnrlon=-116.5, llcrnrlat=50.5, urcrnrlon=-114.5, urcrnrlat=51.5, resolution='l',
                           projection='lcc', lat_0=self.Cen_lat, lon_0=self.Cen_lon)

    def get_line(self):
        xx, yy = self.map(self.lons, self.lats)
        xgc, ygc = self.map.gcpoints(self.loc['Nipika_loc'][1], self.loc['Nipika_loc'][0], self.loc['Powerline_loc'][1],
                                     self.loc['Powerline_loc'][0], self.ndat)
        self.xy.update({'xx': xx, 'yy': yy, 'xgc': xgc, 'ygc': ygc})
        for j in range(self.ndat):
            dist = np.sqrt((xx - xgc[j]) ** 2 + (yy - (ygc[j])) ** 2)
            I, J = np.where(dist == np.min(dist))
            self.data_aff['II'][j] = int(I)
            self.data_aff['JJ'][j] = int(J)
            self.data_aff['TOPO'][j] = self.topo[I, J]
            self.data_aff['latgc'][j] = self.lats[I, J]
            self.data_aff['longc'][j] = self.lons[I, J]

    def plot(self):
        fig, ax = plt.subplots(figsize=(15, 4), dpi=300, facecolor='white')
        ax.set_title('Vertical cross-section (3-km resolution): Topography', loc='left', fontsize=10)
        ax.plot(self.dist_km, self.data_aff['TOPO'], color='darkgrey', linewidth=2)
        ax.fill_between(self.dist_km, self.data_aff['TOPO'], color='grey', alpha=.35)
        ax.set_ylim(0, 4000)
        ax.set_xlim(self.dist_km[0], self.dist_km[-1])
        ax.set_xlabel('Distance (km)')
        ax.set_ylabel('Elevation (m)')
        ax.grid()
        ax.text(self.dist_km[0], -500, 'Nipika', va='center', ha='center', fontsize=16)
        ax.text(self.dist_km[-1], -500, 'Fortress', va='center', ha='center', fontsize=16)
        plt.show()

    def __call__(self):
        self.get_domaine()
        self.get_line()
        self.plot()


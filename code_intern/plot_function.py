import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle
import pandas as pd
from netCDF4 import num2date


rivers = cfeature.NaturalEarthFeature(
    category='physical', name='rivers_lake_centerlines',
    scale='10m', facecolor='none', edgecolor='blue')

states_provinces = cfeature.NaturalEarthFeature(
    category='cultural',
    name='admin_1_states_provinces_lines',
    scale='50m',
    facecolor='none')




class plot_graph():
    def __init__(self, data,**kwargs):
        self.data = data
        self.time = kwargs.get("time", None)
        self.event = kwargs.get('event',False)
        self.save= kwargs.get("save", True)
        self.domaine={}
        self.Cen_lat = 0
        self.Cen_lon = 0
        self.extent=[]
        self.get_domaine()
        self.small_domaine = {'smallLL_lat': 50.5, 'smallLL_lon': -116.5, 'smallUL_lat': 51.5, 'smallUL_lon': -116.5,
                              'smallLR_lat': 50.5,'smallLR_lon': -114.5, 'smallUR_lat': 51.5, 'smallUR_lon': -114.5}

        self.map_proj = ccrs.LambertConformal(central_latitude=self.Cen_lat, central_longitude=self.Cen_lon)
        self.data_proj = ccrs.PlateCarree()
        self.rotated_pole_proj = ccrs.RotatedPole(pole_latitude=data['rotated_pole'].grid_north_pole_latitude,
                                                  pole_longitude=-data['rotated_pole'].grid_north_pole_longitude)
        self.i=0


    def cartopy_xlabel(self, ax, x_lons, myproj, tick_fs):
        # transform the corner points of my map to lat/lon
        xy_bounds = ax.get_extent()
        ll_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0], xy_bounds[2], myproj)
        lr_lonlat = ccrs.Geodetic().transform_point(xy_bounds[1], xy_bounds[2], myproj)
        # take the median value as my fixed latitude for the x-axis
        l_lat_median = np.median([ll_lonlat[1], lr_lonlat[1]])  # use this lat for transform on lower x-axis
        x_lats_helper = np.ones_like(x_lons) * l_lat_median

        x_lons = np.asarray(x_lons)
        x_lats_helper = np.asarray(x_lats_helper)
        x_lons_xy = myproj.transform_points(ccrs.Geodetic(), x_lons, x_lats_helper)
        x_lons_xy = list(x_lons_xy[:, 0])  # only lon pos in xy are of interest
        x_lons = list(x_lons)

        x_lons_labels = []
        for j in range(len(x_lons)):
            if x_lons[j] > 0:
                ew = r'$^\circ$E'
                x_lons_labels.append(str(x_lons[j]) + ew)
            else:
                ew = r'$^\circ$W'
                x_lons_labels.append(str(x_lons[j] * -1) + ew)
        ax.set_xticks(x_lons_xy)
        ax.set_xticklabels(x_lons_labels, fontsize=tick_fs)

    def cartopy_ylabel(self, ax, y_lats, myproj, tick_fs):
        xy_bounds = ax.get_extent()
        ll_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0], xy_bounds[2], myproj)
        ul_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0], xy_bounds[3], myproj)
        l_lon_median = np.median([ll_lonlat[0], ul_lonlat[0]])  # use this lon for transform on left y-axis
        y_lons_helper = np.ones_like(y_lats) * l_lon_median

        y_lats = np.asarray(y_lats)
        y_lats_xy = myproj.transform_points(ccrs.Geodetic(), y_lons_helper, y_lats)
        y_lats_xy = list(y_lats_xy[:, 1])  # only lat pos in xy are of interest

        y_lats = list(y_lats)

        y_lats_labels = []
        for j in range(len(y_lats)):
            if y_lats[j] > 0:
                ew = r'$^\circ$N'
                y_lats_labels.append(str(y_lats[j]) + ew)
            else:
                ew = r'$^\circ$S'
                y_lats_labels.append(str(y_lats[j] * -1) + ew)
        ax.set_yticks(y_lats_xy)
        ax.set_yticklabels(y_lats_labels, fontsize=tick_fs)


    def get_domaine(self):
        """

        :return: get the domaine of the heatmap from the data
        """
        lats = self.data.variables['lat'][:, :]
        lons = self.data.variables['lon'][:, :]
        self.domaine = {'LL_lat':lats[0][0] , 'LL_lon':lons[0][0],'UL_lat':lats[-1][0], 'UL_lon': lons[-1][0],'LR_lat':lats[0][-1], 'LR_lon':lons[0][-1],'UR_lat':lats[-1][-1], 'UR_lon' :lons[-1][-1]}
        self.Cen_lat = self.domaine['LL_lat'] + ((self.domaine['UL_lat'] - self.domaine['LL_lat']) / 2)
        self.Cen_lon = self.domaine['LL_lon'] + ((abs(self.domaine['LL_lon']) - abs(self.domaine['LR_lon'])) / 2)
        self.extent = [self.domaine['UL_lon'], self.domaine['LR_lon'], self.domaine['LL_lat'], self.domaine['UR_lat']]

    def get_mean_temp(self):
        """
        :return: array lon/lat of mean temperature value
        """

        with open('../Stock_array/Array_mean_temp', 'rb') as fp:
            tempe_moy = pickle.load(fp)-273
        return tempe_moy

    def nearest_ind(self,items, pivot):
        time_diff = np.abs([date - pivot for date in items])
        return time_diff.argmin()

    def get_index_storm(self):
        start = []
        finish = []
        df = pd.read_csv("dates_of_storms.csv.nosync.csv", parse_dates=True)
        for i in range(len(df['number'])):
            debut = df['start'][df['number'][i] - 1]
            fin = df['finish'][df['number'][i] - 1]
            times = self.data.variables['time']
            vtimes = num2date(times[:], units=times.units)
            index_start = self.nearest_ind(vtimes, pd.Timestamp(debut))
            index_finish = self.nearest_ind(vtimes, pd.Timestamp(fin))
            start.append(int(index_start))
            finish.append(int(index_finish))
        return start,finish

    def get_mean_temp_event(self,start,finish,number):
        # tempe_moy_event = np.mean(self.data['tas'][start:finish, :, :], axis=0)
        # with open(f'Array_mean_temp_event{number+1}', 'wb') as fp:
        #     pickle.dump(tempe_moy_event, fp, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f'../Stock_array/Array_mean_temp_event{number+1}', 'rb') as fp:
            tempe_moy_event = pickle.load(fp)-273.15
        return tempe_moy_event

    def get_slice(self):
        """
        :return: array of the slice in x and y
        """
        pass 

    def plot_temp_heatmap(self,heat_data):
        '''
        :return: plot the heatmap of the temperature
        '''

        fig = plt.figure(facecolor='white',figsize=(10,4), dpi=300)
        ax = plt.subplot(1,1,1,projection=self.map_proj)
        ax.set_extent([self.extent[0] - 0.5, self.extent[1] + 0.5, self.extent[2] - 0.5, self.extent[3] + 0.5], self.data_proj)

        ax.add_feature(states_provinces, edgecolor='black', linewidth=.5)
        ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        # ax.add_feature(rivers, linewidth=0.5)
        ax.coastlines('10m', edgecolor='black', linewidth=.5)
        x_lines = np.arange(180, -180, -10)
        y_lines = np.arange(0, 90, 10)
        gl = ax.gridlines()
        gl.xlocator = ticker.FixedLocator(x_lines)
        gl.ylocator = ticker.FixedLocator(y_lines)

        x, y = [self.domaine['LL_lon'], self.domaine['UL_lon'], self.domaine['UR_lon'], self.domaine['LR_lon'], self.domaine['LL_lon']], [self.domaine['LL_lat'], self.domaine['UL_lat'], self.domaine['UR_lat'], self.domaine['LR_lat'], self.domaine['LL_lat']]
        ax.plot(x, y, marker='o', markersize=.5, color='red', linewidth=.75, linestyle='--', transform=self.data_proj)

        small_x = [self.small_domaine['smallLL_lon'], self.small_domaine['smallUL_lon'], self.small_domaine['smallUR_lon'], self.small_domaine['smallLR_lon'], self.small_domaine['smallLL_lon']]
        small_y = [self.small_domaine['smallLL_lat'], self.small_domaine['smallUL_lat'], self.small_domaine['smallUR_lat'], self.small_domaine['smallLR_lat'], self.small_domaine['smallLL_lat']]
        ax.plot(small_x, small_y, marker='o', markersize=.5, color='k', linewidth=.75, linestyle='--',
                transform=self.data_proj)

        levels = np.arange(-40, 41, 1)
        levels_tick = np.arange(-40, 41, 5)
        cn = ax.contourf(self.data['lon'][:], self.data['lat'][:], heat_data, cmap='coolwarm', transform=self.data_proj,levels=levels)
        colorbar=plt.colorbar(cn, ax=ax,pad=0.05, aspect=50, shrink=.75, extend='Max',ticks=levels_tick)
        colorbar.set_label('Temperature [\u2103]', rotation=270,fontsize=10,labelpad=11)
        colorbar.ax.tick_params(labelsize=7)
        x_labels = np.arange(-80, -150, -10)  # want these longitudes as tick positions
        y_labels = np.arange(30, 65, 10) #  want these latitudes as tick positions
        tick_fs = 10
        self.cartopy_xlabel(ax, x_labels, self.map_proj, tick_fs)
        self.cartopy_ylabel(ax, y_labels, self.map_proj, tick_fs)
        ax.set_title('VALID: 15-04-2019', loc='right', fontsize=8)
        ax.set_title(f'SPADE simulation domain  ', loc='left', fontsize=8)
        if self.event==True:
            if self.save == True:
                plt.savefig(f'mean_temp_event{self.i+1}.png', bbox_inches='tight')
                plt.savefig(f'mean_temp_event{self.i + 1}.pdf', bbox_inches='tight')
            else:
                plt.show()
        else:
            if self.save==True:
                plt.savefig('mean_temp.png', bbox_inches='tight')
                plt.savefig('mean_temp.pdf', bbox_inches='tight')
            else:
                plt.show()


    def __call__(self):
        if self.event == True:
            start, finish = self.get_index_storm()
            for i in range(len(start)):
                self.i=i
                heat_data = self.get_mean_temp_event(start[i],finish[i],i)
                self.plot_temp_heatmap(heat_data)
        else:
            heat_data = self.get_mean_temp()
            self.plot_temp_heatmap(heat_data)

import numpy as np
from datetime import datetime

import cartopy.crs as ccrs
import cartopy.feature as cfeature

from netCDF4 import Dataset as cdf4_ds
from netCDF4 import num2date
from metpy.units import units

from scipy.ndimage import gaussian_filter


import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
from matplotlib.dates import MO, TU, WE, TH, FR, SA, SU
import matplotlib.ticker as ticker


from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
rivers = cfeature.NaturalEarthFeature(
    category='physical', name='rivers_lake_centerlines',
    scale='10m', facecolor='none', edgecolor='blue')
states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='50m',
        facecolor='none')

def pratique(projection_crs, latlon):
    fig = plt.figure()
    rect = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes(rect, projection=projection_crs)
    ax.set_extent(latlon, crs=projection_crs)
    ax.coastlines(linewidth=0.5, color='black')
    ax.add_feature(rivers, linewidth=1)

    # city_data = ['Vancouver', 'BC', 49.246292, -123.116226, 'k']
    # ax.plot(city_data[2], city_data[1], marker='o',
    #         markersize=2.0, markeredgewidth=1.0,
    #         linestyle='None', label=city_data[0], transform=projection_crs)
    # ax.legend()
    plt.show()

def make_plot( projection_crs, latlon, heat_data):

    fig = plt.figure()
    rect = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes(rect, projection=projection_crs)
    ax.set_extent(latlon, crs=projection_crs)

    ax.coastlines(linewidth=0.5, color='black')
    # ax.gridlines(crs=projection_crs, linestyle='-')
    ax.add_feature(states_provinces, edgecolor='gray')
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    lat = np.linspace(latlon[2], latlon[3], heat_data.shape[0])
    lon = np.linspace(latlon[0], latlon[1], heat_data.shape[1])
    Lat, Lon = np.meshgrid(lat, lon)

    ax.pcolormesh(Lon,Lat,np.transpose(heat_data),cmap='coolwarm')
    plt.show()
    # plt.savefig("Test_fig.pdf", bbox_inches='tight')


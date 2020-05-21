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
domaine=[]
smallLL_lat, smallLL_lon = 50.5, -116.5
smallUL_lat, smallUL_lon = 51.5, -116.5
smallLR_lat, smallLR_lon = 50.5, -114.5
smallUR_lat, smallUR_lon = 51.5, -114.5

tas_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/tas_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')
lats = tas_nc_file.variables['lat'][:, :]
lons = tas_nc_file.variables['lon'][:, :]
LL_lat, LL_lon = lats[0][0], lons[0][0]
UL_lat, UL_lon = lats[-1][0], lons[-1][0]
LR_lat, LR_lon = lats[0][-1], lons[0][-1]
UR_lat, UR_lon = lats[-1][-1], lons[-1][-1]



def cartopy_xlabel(ax,x_lons,myproj,tick_fs):
    #transform the corner points of my map to lat/lon
    xy_bounds = ax.get_extent()
    ll_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0],xy_bounds[2], myproj)
    lr_lonlat = ccrs.Geodetic().transform_point(xy_bounds[1],xy_bounds[2], myproj)
    #take the median value as my fixed latitude for the x-axis
    l_lat_median = np.median([ll_lonlat[1],lr_lonlat[1]]) #use this lat for transform on lower x-axis
    x_lats_helper = np.ones_like(x_lons)*l_lat_median

    x_lons = np.asarray(x_lons)
    x_lats_helper = np.asarray(x_lats_helper)
    x_lons_xy = myproj.transform_points(ccrs.Geodetic(), x_lons,x_lats_helper)
    x_lons_xy = list(x_lons_xy[:,0]) #only lon pos in xy are of interest
    x_lons = list(x_lons)

    x_lons_labels =[]
    for j in range(len(x_lons)):
        if x_lons[j]>0:
            ew=r'$^\circ$E'
            x_lons_labels.append(str(x_lons[j])+ew)
        else:
            ew=r'$^\circ$W'
            x_lons_labels.append(str(x_lons[j]*-1)+ew)
    ax.set_xticks(x_lons_xy)
    ax.set_xticklabels(x_lons_labels,fontsize=tick_fs)

def cartopy_ylabel(ax,y_lats,myproj,tick_fs):
    xy_bounds = ax.get_extent()
    ll_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0],xy_bounds[2], myproj)
    ul_lonlat = ccrs.Geodetic().transform_point(xy_bounds[0],xy_bounds[3], myproj)
    l_lon_median = np.median([ll_lonlat[0],ul_lonlat[0]]) #use this lon for transform on left y-axis
    y_lons_helper = np.ones_like(y_lats)*l_lon_median

    y_lats = np.asarray(y_lats)
    y_lats_xy = myproj.transform_points(ccrs.Geodetic(), y_lons_helper, y_lats)
    y_lats_xy = list(y_lats_xy[:,1]) #only lat pos in xy are of interest

    y_lats = list(y_lats)

    y_lats_labels =[]
    for j in range(len(y_lats)):
        if y_lats[j]>0:
            ew=r'$^\circ$N'
            y_lats_labels.append(str(y_lats[j])+ew)
        else:
            ew=r'$^\circ$S'
            y_lats_labels.append(str(y_lats[j]*-1)+ew)
    ax.set_yticks(y_lats_xy)
    ax.set_yticklabels(y_lats_labels,fontsize=tick_fs)

def get_temp(data, time):
    tempe=data['tas'][time, :, :] - 273.15
    return tempe

def DoRotation(xspan, yspan, RotRad=0):
    """Generate a meshgrid and rotate it by RotRad radians."""

    # Clockwise, 2D rotation matrix
    RotMatrix = np.array([[np.cos(RotRad),  np.sin(RotRad)],
                          [-np.sin(RotRad), np.cos(RotRad)]])

    x, y = np.meshgrid(xspan, yspan)
    return np.einsum('ji, mni -> jmn', RotMatrix, np.dstack([x, y]))

def grid_hetamap(data):
    lat_rpole=data['rlat'][:]
    lon_rpole=data['rlon'][:]
    Lon, Lat = np.meshgrid(lon_rpole, lat_rpole)
    return Lon,Lat

def plot_temp_heatmap(data,time):

    lats = data.variables['lat'][:, :]
    lons = data.variables['lon'][:, :]
    LL_lat, LL_lon = lats[0][0], lons[0][0]
    UL_lat, UL_lon = lats[-1][0], lons[-1][0]
    LR_lat, LR_lon = lats[0][-1], lons[0][-1]
    UR_lat, UR_lon = lats[-1][-1], lons[-1][-1]

    Cen_lat = LL_lat + ((UL_lat - LL_lat) / 2)
    Cen_lon = LL_lon + ((abs(LL_lon) - abs(LR_lon)) / 2)
    extent = [UL_lon, LR_lon, LL_lat, UR_lat]

    map_proj = ccrs.LambertConformal(central_latitude=Cen_lat, central_longitude=Cen_lon)

    # Set projection of data (so we can transform for the figure)
    data_proj = ccrs.PlateCarree()

    # rotated pole projection
    rotated_pole_proj = ccrs.RotatedPole(pole_latitude=30.938543, pole_longitude=-104.410934)

    fig = plt.figure()
    ax = plt.subplot(projection=map_proj)
    ax.set_extent([extent[0]-0.5, extent[1]+0.5, extent[2]-0.5, extent[3]+0.5] , data_proj)

    ax.add_feature(states_provinces, edgecolor='black', linewidth=.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.coastlines('10m', edgecolor='black', linewidth=.5)
    x_lines = np.arange(180, -180, -10)
    y_lines = np.arange(0, 90, 10)
    gl = ax.gridlines()
    gl.xlocator = ticker.FixedLocator(x_lines)
    gl.ylocator = ticker.FixedLocator(y_lines)

    x, y = [LL_lon, UL_lon, UR_lon, LR_lon, LL_lon], [LL_lat, UL_lat, UR_lat, LR_lat, LL_lat]
    ax.plot(x, y, marker='o', markersize=.5, color='red', linewidth=.75, linestyle='--', transform=data_proj)

    small_x = [smallLL_lon, smallUL_lon, smallUR_lon, smallLR_lon, smallLL_lon]
    small_y = [smallLL_lat, smallUL_lat, smallUR_lat, smallLR_lat, smallLL_lat]
    ax.plot(small_x, small_y, marker='o', markersize=.5, color='k', linewidth=.75, linestyle='--', transform=data_proj)
    heat_data = get_temp(data, time)


    x_labels = np.arange(-110, -120,2)  # want these longitudes as tick positions
    y_labels = np.arange(50, 52,2)  # want these latitudes as tick positions
    tick_fs = 12
    cartopy_xlabel(ax, x_labels, map_proj, tick_fs)
    cartopy_ylabel(ax, y_labels, map_proj, tick_fs)

    ax.set_title('SPADE simulation domain', loc='left', fontsize=8)
    ax.set_title('VALID: 15-04-2019', loc='right', fontsize=8)

    Lon,Lat=grid_hetamap(data)

    cn=ax.pcolormesh(Lon,Lat, heat_data, cmap='coolwarm',transform=rotated_pole_proj)
    plt.colorbar(cn, ax=ax)
    plt.show()

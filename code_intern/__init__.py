from netCDF4 import Dataset as cdf4_ds
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import seaborn as sea
from code_intern import plot_function as plt_int

if __name__ == '__main__':
    tas_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/tas_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')
    print(tas_nc_file.variables)



    smallLL_lat, smallLL_lon = 50.5, -116.5
    smallUL_lat, smallUL_lon = 51.5, -116.5
    smallLR_lat, smallLR_lon = 50.5, -114.5
    smallUR_lat, smallUR_lon = 51.5, -114.5


    frontiere=[50.5,51.5,-116.5,-114.5]


    plt_int.plot_temp_heatmap(tas_nc_file,0)
    # crs_latlon = ccrs.PlateCarree()
    # mapproj = ccrs.LambertConformal(central_latitude=Cen_lat, central_longitude=Cen_lon)
    # crs_rotated=ccrs.RotatedPole(pole_latitude=45, pole_longitude=180)
    # latlon=(-117,-114,50,52)
    # # plt_int.pratique(crs_latlon,lonlat)
    # plt_int.make_plot(crs_latlon,latlon,tempe_0)
    # plt.figure()
    # plt.title(f"\n Graph d'essaie du plot des températures au temps zéros\n")
    # ax = sea.heatmap(tempe_0, cmap='coolwarm')
    # ax.set_xlabel('Longitude [modifie les graduations later] ')
    # ax.set_ylabel('Latitude [modifie les graduations later]')
    # plt.show()

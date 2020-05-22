from netCDF4 import Dataset as cdf4_ds
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from code_intern import plot_function as plt_int

if __name__ == '__main__':
    tas_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/tas_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')
    print(tas_nc_file.variables)
    plt_int.plot_graph(tas_nc_file,0).plot_temp_heatmap()



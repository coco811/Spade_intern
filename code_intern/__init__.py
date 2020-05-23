from netCDF4 import Dataset as cdf4_ds
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sea
from code_intern import plot_function as plt_int
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle
if __name__ == '__main__':


    tas_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/tas_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')
    tempe_moy = np.mean(tas_nc_file['tas'][:, :, :], axis=0)
    with open('Array_mean_temp', 'wb') as fp:
        pickle.dump(tempe_moy, fp, protocol=pickle.HIGHEST_PROTOCOL)

    # print(tas_nc_file['tas'])
    # plt_int.plot_graph(tas_nc_file).plot_temp_heatmap()



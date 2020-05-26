from netCDF4 import Dataset as cdf4_ds

import numpy as np

from code_intern import plot_function as plt_int
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle

if __name__ == '__main__':
    pr_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/pr_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')
    print(pr_nc_file.variables)

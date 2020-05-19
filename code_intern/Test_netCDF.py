import numpy as np
import pandas as pd

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

if __name__ == '__main__':
    pr_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/pr_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')  # file shape[time, lat, lon]
    tas_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/tas_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')

    times = pr_nc_file.variables['time']
    vtimes = num2date(times[:], units=times.units)
    print(f'{vtimes[0]}')

    times = pr_nc_file.variables['time'][:]
    idx = pd.date_range(start='2019-04-15 01:0:00', freq='H', periods=len(times))

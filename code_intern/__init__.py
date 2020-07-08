from netCDF4 import Dataset as cdf4_ds

import numpy as np

from code_intern import plot_function as plt_int
from code_intern import Analyse_data as Ana_data
from code_intern import cross_section as crossec
try:
    import cPickle as pickle
except ImportError:  # python 3.x
    import pickle
import pandas as pd
import datetime
import csv
def get_precipitation_doc():
    Nipika= pd.read_csv('../pluvio_data_analyse/Geonor_nipika.csv.nosync.csv', parse_dates=['Date'])
    junction = pd.read_csv('../pluvio_data_analyse/Pluvio_Junction_pro.csv.nosync.csv', parse_dates=['Date'])
    powerline = pd.read_csv('../pluvio_data_analyse/Pluvio_powerline.csv.nosync.csv', parse_dates=['Date'])
    doc=[Nipika ,junction,powerline]
    doc_name = ['Nipika', 'junction', 'Fortress']
    for i in range(len(doc)):
        diff = doc[i]['Acc'].diff(periods=1)
        with open(f'Hourly_data_pr_{str(doc_name[i])}.csv.nosync', 'w', newline='') as file:
            writer = csv.writer(file)
            head = ["Date",'Acc']
            writer.writerow(head)
            for j in range(len(diff)):
                data = [doc[i]['Date'][j],diff[j]]
                writer.writerow(data)


def get_mean_calc(data):
    tempe_moy = np.mean(data['tas'][:, :, :], axis=0)
    with open('../Stock_array/Array_mean_temp', 'wb') as fp:
        pickle.dump(tempe_moy, fp, protocol=pickle.HIGHEST_PROTOCOL)

def intrp1d(varin,z,ztype,zref):
    nz = len(z)
    end = False
    if ztype=="Z":
        for k in range(nz):
            if ((z[k]>=zref) and (not end)):
                varout = varin[k]-(varin[k]-varin[k-1])/(z[k]-z[k-1])*(z[k]-zref)
                end = True
                break
    if ztype=="P":
        p = z
        pref = zref
        for k in range(nz):
            if ((p[k]<=pref) and (not end)):
                varout = varin[k]-(varin[k]-varin[k-1])/(p[k]-p[k-1])*(p[k]-pref)
                end = True
                break
    return varout
# ################# Pour interpoler sur Z, provient de xsect.py/wrf_utils.py de SEB #####################
# GZ_array = GZ_array * 10 #en dam vers metres
# Zmax = 6000. # La hauteur maximale de l'interpolation
# dZ = 100. # L'épaisseur entre chaque niveaux Z
# nz = int(Zmax/dZ)+1
# #Declaration des variables interpolee
# T_interp=np.zeros((ndat,nz))
# Z_interp = np.linspace(0.,Zmax,nz)
# UU_interp=np.zeros((ndat,nz))
# VV_interp=np.zeros((ndat,nz))
# for i in range(distance):
#     for k in range(nz):
#         T_interp[i,k]=intrp1d(TT_array[i,:],GZ_array[i,:],"Z",Z_interp[k])
#         UU_interp[i,k]=intrp1d(UU_array[i,:],GZ_array[i,:],"Z",Z_interp[k])
#         VV_interp[i,k]=intrp1d(VV_array[i,:],GZ_array[i,:],"Z",Z_interp[k])
if __name__ == '__main__':
    "plot temps simulation"
    # get_precipitation_doc()

    # pr_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/pr_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc.nosync')
    tas_nc_file = cdf4_ds('/Users/olivier1/Documents/Data_stage/tas_CA_Rockies_3km_P3_ERA5-1h_ISBA_USGS.nc')
    # print(tas_nc_file.variables)
    # print(pr_nc_file.variables)
    # print(tas_nc_file.variables)
    # plt_int.plot_graph(tas_nc_file,event=True,save=True).__call__()

    # Ana_data.data_site('Alldata.csv',tas_nc_file,Data_aff='temperature').__call__()
    crossec.cross_section('Alldata.csv',tas_nc_file).__call__()

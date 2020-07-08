trajectory_data_readme.txt = information regarding the data extracted for trajoectory analysis

DIRECTORIES:
named as per the length of the cross section and the resolution of the data. Ie. Cross_section_460_1km is data for the 460km long cross section using 1km resolution data. 

SUB_DIRECTORIES:
storm dates. Ie. June_21_storm

DATA_DIRECTORIES:
Variables: data for each cross section that changed depending on the date (eg. Temperature)
Constants: data for each cross section that does not change depending on the date (eg. Elevation along the transect)

CONSTANTS:
transect_elevation.npy: z values along the transect. shape=[length of transect]

transect_distance.npy: x values along transect, easy for 1km data as there is one data point per km. shape=[length of transect]

transect_boolean_mask.npy: full 1060x1060 array with Trye values along transect. Place onto 1060x1060 array to extract data along transect. Eg clipped_data_array = data[mask]. shape=[full grid 1060x1060]

transect_lats / lons .npy: lats and lons along the transect. shape=[length of transect]
    
p_levels_hPa.npy: list of levels in hPa. shape=[number of levels]
p_levels_rpn.npy: list of levels using rpn code, relates directly to p_levels_hPa. required as'ip1' to access rpn files. shape=[number of levels]

timestamps_strings.npy: timestamps in string format for each hour of the storm in question. shape=[number of timesteps]
timestamps_rpn.npy: timestamps using rpn code, relates directly to timestapms_strings. required as 'datev' to access rpn files. shape=[number of timesteps]

VARIABLES:
T2_array.npy: 2-m temperature along cross section. shape=[timesteps, length of cross section]

UU / VV _10m_knots.npy: 10m wind vectors along the cross section, in knots. shape=[timesteps, length of cross section]

TT_array.npy: temperature along cross section at all levels as per p_levels_hPa. shape=[timesteps, levels, length of cross section]

UU / VV _array.npy: wind vectors in knots, along cross section for all levels as per p_levels_hPa. shape=[timesteps, levels, length of cross section]

GZ_array.npy: geopotential, in dam, for all levels as per p_levels. shape=[timesteps, levels, length of cross section]. required for interpolation of variables from pressure levels to heights in meters  

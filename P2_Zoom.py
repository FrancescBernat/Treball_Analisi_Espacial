#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P2_Zoom.py
@Date    :   2023/12/14 17:30:13
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

Provam d'enfocar la regió que ens interessa estudiar.
'''

import numpy as np
import xarray as xr
import netCDF4 as nc
import cartopy as cart
import matplotlib as mp
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Per a cambiar les lletres a l'estil que és te a latex
mp.rcParams['mathtext.fontset'] = 'stix'
mp.rcParams['font.family'] = 'STIXGeneral'
mp.rcParams.update({'font.size': 14})

arxiu = 'AQUA_MODIS.20190104T020501.L2.SST.nc'

# Llegim arxiu nc
data = nc.Dataset('DadesMar/'+ arxiu, 'r')

# Extreim el dia de lectura
time = data.getncattr('time_coverage_start')
T = time.replace('T', ' ').split('.')[0]

# Extreim el sst
Geo = data.groups['geophysical_data']
sst = np.fliplr(Geo.variables['sst'][:])

# Extreim les coordenades
nav = data['navigation_data']
lat = np.fliplr(nav['latitude'][:])
lon = np.fliplr(nav['longitude'][:])

# Definim les coordenades màximes i mínime
min_lon = 1
max_lon = 6

min_lat = 37
max_lat = 42

# Cream un data array per tenir 
da = xr.DataArray(sst, dims=['x', 'y'], 
                  coords = dict(lon=(["x", "y"], lon), 
                                lat=(["x", "y"], lat)))

# Si els punts estan a dins o fora de la regió d'interes
mask_lon = (da.lon >= min_lon) & (da.lon <= max_lon)
mask_lat = (da.lat >= min_lat) & (da.lat <= max_lat)

# Eliminam els punts fora dels límits marcats
cro_da = da.where(mask_lon & mask_lat, drop=True)


_RGB_CODES = ["#663300", "#852800", "#a41e00", "#c21400", "#e10a00", "#ff0000", "#ea2915", 
             "#d65229", "#ce7137", "#d0853f", "#d29946", "#e4c27c", "#f6ebb2", "#d6ffe1", 
             "#7af4ff", "#00ccff", "#15a3d6", "#297aad", "#285b99", "#144799", "#003399",
             "#2933ae", "#5233c2", "#7b33d7", "#a433eb", "#cc33ff"]
_WARMTOCOLD = LinearSegmentedColormap.from_list('', _RGB_CODES[::-1], N = 256)

##########################################################################################

fig = plt.figure(figsize=(9, 7), dpi=400)
ax = plt.axes(projection=cart.crs.PlateCarree())
ax.coastlines()
ax.add_feature(cart.feature.LAND, zorder=2, edgecolor='k', linewidth=0.05)

plot = ax.contourf(cro_da.lon, cro_da.lat, cro_da, 70, transform=cart.crs.PlateCarree(),cmap=_WARMTOCOLD)# cmap='RdYlBu_r')

# Ticks per a la longitud
ax.set_xticks(np.linspace(min_lon, max_lon, 5), crs=cart.crs.PlateCarree())
lon_formatter = LongitudeFormatter(number_format='.2f')
ax.xaxis.set_major_formatter(lon_formatter)

# Ticks per a la latitud
ax.set_yticks(np.linspace(min_lat, max_lat, 5), crs=cart.crs.PlateCarree())
lat_formatter = LatitudeFormatter(number_format='.2f')
ax.yaxis.set_major_formatter(lat_formatter)

ax.set_xlim([min_lon, max_lon])
ax.set_ylim([min_lat, max_lat])

cb = plt.colorbar(plot)
cb.set_label("sst (ºC)", rotation=270)
ax.set_title(f"Dades sst pel dia {T}")
plt.show()
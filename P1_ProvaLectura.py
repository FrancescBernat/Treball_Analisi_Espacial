#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P1_ProvaLectura.py
@Date    :   2023/12/09 23:33:03
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

Representam les dades dels satel·lits que hem descarregat.
'''

import matplotlib
import numpy as np
import netCDF4 as nc
import datetime as dt
import cartopy as cart
import matplotlib.pyplot as plt
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# Per a cambiar les lletres a l'estil que és te a latex
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams.update({'font.size': 14})

arxiu = 'AQUA_MODIS.20190104T020501.L2.SST.nc'

# Llegim arxiu nc
data = nc.Dataset('DadesMar/'+ arxiu, 'r')

if 0:
    print(data.ncattrs())
    print(data.getncattr('title'))

Geo = data.groups['geophysical_data']

# Extreim informació del dia
info = data['scan_line_attributes']
dia = int(info['day'][0])
Temps = dt.date(2020, 1, dia)
Temps.strftime("%d/%m/%Y")

time = data.getncattr('time_coverage_start')
T = time.replace('T', ' ').split('.')[0]

# Extreim les coordenades
nav = data['navigation_data']
lat = np.fliplr(nav['latitude'][:])
lon = np.fliplr(nav['longitude'][:])

# Extreim i ordenam correctament les dades sst
sst = np.fliplr(Geo.variables['sst'][:])

fig = plt.figure(figsize=(9, 7), dpi=400)

# Representam el mapa 
ax = plt.axes(projection=cart.crs.PlateCarree())
ax.coastlines()
ax.add_feature(cart.feature.LAND, zorder=2, edgecolor='k', linewidth=0.05)

plot = ax.contourf(lon, lat, sst, 70, transform=cart.crs.PlateCarree())

# Ticks per a la longitud
ax.set_xticks(np.arange(np.min(lon[:]), np.max(lon[:]), 6), crs=cart.crs.PlateCarree())
lon_formatter = LongitudeFormatter(number_format='.2f')
ax.xaxis.set_major_formatter(lon_formatter)

# Ticks per a la latitud
ax.set_yticks(np.arange(np.min(lat[:]), np.max(lat[:]), 5), crs=cart.crs.PlateCarree())
lat_formatter = LatitudeFormatter(number_format='.2f')
ax.yaxis.set_major_formatter(lat_formatter)

cb = plt.colorbar(plot)
cb.set_label("sst (ºC)", rotation=270)
ax.set_title(f"Dades sst pel dia {T}")
plt.show()
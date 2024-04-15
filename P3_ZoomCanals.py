#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P3_ZoomCanals.py
@Date    :   2023/12/15 14:20:40
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

    Glo --> Abrevació per les coordenades que conté les 
            Illes Balears
    CMa --> Abreviació que usaré pel canal de Mallorca
    CMe --> Abreviació que usaré pel canal de Menorca

Ara enfocam també pel canal de Mallorca i pel de Menorca.    
'''

import numpy as np
import xarray as xr
import netCDF4 as nc
import cartopy as cart
import matplotlib as mp
import matplotlib.pyplot as plt

from cartopy.mpl.ticker import LatitudeFormatter
from cartopy.mpl.ticker import LongitudeFormatter

# Per a cambiar les lletres a l'estil que és te a latex
mp.rcParams['mathtext.fontset'] = 'stix'
mp.rcParams['font.family'] = 'STIXGeneral'
mp.rcParams.update({'font.size': 14})

arxiu = 'AQUA_MODIS.20190104T020501.L2.SST.nc'

# Definim funcions per alleugerir la feina
def DadesMODIS(arxiu):
    '''
    Funció que, donat el nom d'un arxiu determinat nom d'un arxiu de 
    sst retorna:

        T   --> El temps en que és va començar a enregistrar les 
                dades.
        sst --> Les dades sst
        lat --> La latitud
        lon --> La longitud
    '''
    
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

    return T, sst, lat, lon

T, sst, lat, lon = DadesMODIS(arxiu)


data = xr.DataArray(
                    sst, dims=['x', 'y'], 
                    coords = dict(lon=(["x", "y"], lon), 
                                  lat=(["x", "y"], lat))
                    )

# Definesc ara les latituds i les longituds de cada zona.
lat_Glo = [37, 42]
lon_Glo = [1, 6]

lat_CMe = [39.7, 40]
lon_CMe = [3.2, 3.9]

lat_CMa = [38.6, 39.5]
lon_CMa = [1.5, 3]

def ZonaZoom(dades, lon_Loc, lat_Loc):
    '''
    Funció que donat unes dades (en DataArray) i unes longitud
    i latituds minimes i máximes. Retorna el troz que és troba 
    localitzat entre aquestes coordenades.

        dades --> DataArray de xarray amb lon i lat de coordenades

        lon_Loc --> Diccionari amb la longitud minima i la maxima

        lat_Loc --> Diccionari amb la latitud mínima i la maxima 
    '''

    min_lon, max_lon = lon_Loc
    min_lat, max_lat = lat_Loc

    mask_lon = (dades.lon >= min_lon) & (dades.lon <= max_lon)
    mask_lat = (dades.lat >= min_lat) & (dades.lat <= max_lat)

    return dades.where(mask_lon & mask_lat, drop=True)

# Ara per a poder visualitzar 
def Repr(PlotData, lon_Loc, lat_Loc, Zona):
    '''
    Funció per a representar un contorn del sst de l'area de
    interes.
    '''

    # Extreim les longituds i latituds mínimes i maximes
    min_lon, max_lon = lon_Loc
    min_lat, max_lat = lat_Loc

    fig = plt.figure(figsize=(9, 7), dpi=400)
    ax = plt.axes(projection=cart.crs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cart.feature.LAND, zorder=2, edgecolor='k', linewidth=0.05)

    plot = ax.contourf(PlotData.lon, PlotData.lat, PlotData, 70, 
                       transform=cart.crs.PlateCarree(), cmap='RdYlBu_r')

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
    ax.set_title(f"Dades sst pel dia {T} a {Zona}")
    plt.show()

# Dades de cada zona
lats = [lat_Glo, lat_CMe, lat_CMa]
lons = [lon_Glo, lon_CMe, lon_CMa]
labels = ['Illes Balears', 'Canal de Menorca', 
          'Canal de Mallorca']

# Iteram per a cada zona d'estudi
for la, lo, lab in zip(lats, lons, labels):
    red_data = ZonaZoom(data, lo, la)
    Repr(red_data, lo, la, lab)
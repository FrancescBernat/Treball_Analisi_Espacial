#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   funcions.py
@Date    :   2023/12/16 13:49:05
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

Codi on s'han escrit les funcions que emplen els altres
arxius .py per a simplificar un poc el codi que tenen
aquells arxius.
'''

import numpy as np
import netCDF4 as nc
import matplotlib as mp
import cartopy as cart
import matplotlib.pyplot as plt
import matplotlib.ticker as tck

from cartopy.mpl.ticker import LatitudeFormatter
from cartopy.mpl.ticker import LongitudeFormatter

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
    data = nc.Dataset(arxiu, 'r')

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

def Repr(PlotData, lon_Loc, lat_Loc, Zona, T):
    '''
    Funció per a representar un contorn del sst de l'area de
    interes.
    '''

    # Per a cambiar les lletres a l'estil que és te a latex
    mp.rcParams['mathtext.fontset'] = 'stix'
    mp.rcParams['font.family'] = 'STIXGeneral'
    mp.rcParams.update({'font.size': 14})

    # Extreim les longituds i latituds mínimes i maximes
    min_lon, max_lon = lon_Loc
    min_lat, max_lat = lat_Loc

    fig = plt.figure(figsize=(9, 7), dpi=400)
    ax = plt.axes(projection=cart.crs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cart.feature.LAND, zorder=2, edgecolor='k', linewidth=0.05)

    levels = np.linspace(-4, 18, 100+1)
    plot = ax.contourf(PlotData.lon, PlotData.lat, PlotData, 70, 
                       transform=cart.crs.PlateCarree(), cmap='RdYlBu_r',
                       levels=levels)

    # Ticks per a la longitud
    ax.set_xticks(np.linspace(min_lon, max_lon, 5), crs=cart.crs.PlateCarree())
    lon_formatter = LongitudeFormatter(number_format='.2f')
    ax.xaxis.set_major_formatter(lon_formatter)

    # Ticks per a la latitud
    ax.set_yticks(np.linspace(min_lat, max_lat, 5), crs=cart.crs.PlateCarree())
    lat_formatter = LatitudeFormatter(number_format='.2f')
    ax.yaxis.set_major_formatter(lat_formatter)

    # Límitam els eixos
    ax.set_xlim([min_lon, max_lon])
    ax.set_ylim([min_lat, max_lat])

    cb = plt.colorbar(plot)
    cb.set_label("sst (ºC)", rotation=270)
    ax.set_title(f"Dades sst pel dia {T} a {Zona}")
    plt.show()

def GuardGraf(PlotData, lon_Loc, lat_Loc, Zona, T):
    '''
    Funció per a guardar la representació d'un contorn del sst de l'area de
    interes.
    '''

    # Per a cambiar les lletres a l'estil que és te a latex
    mp.rcParams['mathtext.fontset'] = 'stix'
    mp.rcParams['font.family'] = 'STIXGeneral'
    mp.rcParams.update({'font.size': 14})

    # Extreim les longituds i latituds mínimes i maximes
    min_lon, max_lon = lon_Loc
    min_lat, max_lat = lat_Loc

    fig = plt.figure(figsize=(9, 7), dpi=400)
    ax = plt.axes(projection=cart.crs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cart.feature.LAND, zorder=2, edgecolor='k', linewidth=0.05)

    levels = np.linspace(4, 18, 100+1)
    plot = ax.contourf(PlotData.lon, PlotData.lat, PlotData, 70, 
                       transform=cart.crs.PlateCarree(), cmap='RdYlBu_r',
                       levels=levels)

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
    date  = T.strftime("%Y_%m_%d_%H_%M_%S")
    plt.savefig( Zona +'/'+ date +'.png', dpi=450)
    plt.close(fig)

def fillPlot(x, Mitj, DesvEst, titol, col):
    
    mp.rcParams['mathtext.fontset'] = 'stix'
    mp.rcParams['font.family'] = 'STIXGeneral'
    mp.rcParams.update({'font.size': 17})

    fig, ax = plt.subplots(figsize=(15, 8), dpi=600)

    ax.fill_between(x, Mitj-DesvEst, Mitj+DesvEst, 
                    alpha=.5, linewidth=0, color=col)
    ax.plot(x, Mitj, linewidth=2, color=col)


    ax.set(xticks=x[::100], yticks=np.linspace(-4, 20, 9))
    ax.set_ylabel('sst (ºC)', fontsize=30)

    ax.set_title(titol, fontsize=25)

    # Per tenir ticks petits en l'eix y
    ax.yaxis.set_minor_locator(tck.AutoMinorLocator())

    # Formata les dades de l'eix x per a que siguin llegibles
    fig.autofmt_xdate()
    plt.show()
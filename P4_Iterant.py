#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P4_Iterant.py
@Date    :   2023/12/16 13:03:27
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

    IB  -->  Per referirnos a les Illes Balears
    CMe -->  Per referirnos al canal de Menorca
    CMa -->  Per referirnos al canal de Mallorca

Iteram per a totes les dades de satel·lit devallades.    
'''

import glob 
import numpy as np
import pandas as pd
import xarray as xr
import funcions as fun
import datetime as dt
from importlib import reload

# Recarregam el fitxer amb les funcions per a evitar errors
reload(fun)

nom_arxius = 'DadesMar/*_MODIS.*.SST.nc'

arxius = glob.glob(nom_arxius)

# Definesc ara les latituds i les longituds de cada zona.
lat_Glo = [38, 41]
lon_Glo = [1, 5]

lat_CMe = [39.7, 40]
lon_CMe = [3.2, 3.9]

lat_CMa = [38.6, 39.5]
lon_CMa = [1.5, 3]

lats = [lat_Glo, lat_CMe, lat_CMa]
lons = [lon_Glo, lon_CMe, lon_CMa]
labels = ['Illes Balears', 'Canal de Menorca', 
          'Canal de Mallorca']

# Cream llistes i Dataframes buits per usar mes endavant
Mit = []
Desv = []
numNan = []
Tam = []

Dades_Sat = pd.DataFrame()

for file in arxius:

    [i.clear() for i in [Mit, Desv, numNan]]

    T, sst, lat, lon = fun.DadesMODIS(file)

    Satelit = file.split('_')[0].split('\\')[1]

    data = xr.DataArray(
                        sst, dims=['x', 'y'], 
                        coords = dict(lon=(["x", "y"], lon), 
                                    lat=(["x", "y"], lat))
                        )

    date = dt.datetime.strptime(T, "%Y-%m-%d %H:%M:%S")


    for la, lo in zip(lats, lons):

        red_data = fun.ZonaZoom(data, lo, la)

        numNan.append(np.count_nonzero(np.isnan(red_data.data)))
        Mit.append(np.nanmean(red_data.data))
        Desv.append(np.nanstd(red_data.data))
        Tam.append(red_data.size)

    df = pd.DataFrame(
        {'dia': [T], 'satelit':[Satelit], 
         'Nan IB':numNan[0],  'Mitj IB':Mit[0],  'Desv IB':Desv[0], 'Tam IB':Tam[0],
         'Nan CMe':numNan[1], 'Mitj CMe':Mit[1], 'Desv CMe':Desv[1], 'Tam CMe':Tam[1],
         'Nan CMa':numNan[2], 'Mitj CMa':Mit[2], 'Desv CMa':Desv[2], 'Tam CMa':Tam[2]}
        )

    Dades_Sat = pd.concat([Dades_Sat, df], ignore_index=True)
    Dades_Sat = Dades_Sat.sort_values(by='dia')
    # Guardam el dataframe per treballar-ne mes endavant
    Dades_Sat.to_pickle("./dataframe.pkl") 
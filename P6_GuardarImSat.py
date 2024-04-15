#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P6_GuardarImSat.py
@Date    :   2023/12/18 16:04:05
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

Guardam el camp de SST que veu el  satel·lit, per cada
una de les zones i per cada un dels dies.
'''

import glob 
import numpy as np
import xarray as xr
import funcions as fun
import datetime as dt
from importlib import reload

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
labels = ['IB', 'CMe',  'CMa']

for file in arxius:

    T, sst, lat, lon = fun.DadesMODIS(file)

    Satelit = file.split('_')[0].split('\\')[1]

    data = xr.DataArray(
                        sst, dims=['x', 'y'], 
                        coords = dict(lon=(["x", "y"], lon), 
                                    lat=(["x", "y"], lat))
                        )

    date = dt.datetime.strptime(T, "%Y-%m-%d %H:%M:%S")

    fun.GuardGraf(data, 
                [np.nanmin(data.lon.data), np.nanmax(data.lon.data)],
                [np.nanmin(data.lat.data), np.nanmax(data.lat.data)], 
                'Imatges/Glob', date)

    for la, lo, lab in zip(lats, lons, labels):

        red_data = fun.ZonaZoom(data, lo, la)

        lab = 'Imatges/' + lab

        fun.GuardGraf(red_data, lo, la, lab, date)
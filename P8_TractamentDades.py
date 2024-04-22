#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P8_TractamentDades.py
@Date    :   2024/04/21 17:44:14
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

En aquest arxiu començam a omplir els buids donats a les
dades de Satel·lit.
'''

import numpy as np
import pandas as pd
import funcions as fun
import matplotlib as mp
import datetime as dt
import matplotlib.pyplot as plt
import funcions_interp as fun_int
from importlib import reload

reload(fun)
reload(fun_int)

mp.rcParams['mathtext.fontset'] = 'stix'
mp.rcParams['font.family'] = 'STIXGeneral'
mp.rcParams.update({'font.size': 17})

df = pd.read_pickle("./complete_data.pkl")

# sst que suposam és la temperatura superficial mitjana 
sst_med = 12.74
# sst pel davall suposam que son temperatures falses
sst_min =  6.94 

dataIni = dt.datetime(2019, 12, 31)
dataFin = dt.datetime(2020, 2, 1)

for i in range(df.shape[0]):
    if dataIni < dt.datetime.strptime(df['T'][i], "%Y-%m-%d %H:%M:%S") < dataFin:

        x = df['Dades'][i]

        # Miram el tamany de la matriu x, en cas de no tenir un dia completament
        # buit de dades
        if x.size > 0: 
            x.data[x.data < sst_min] = np.nan

            # Extreim les longituds i les latituds, els nostres punts de les malles
            lat = x.lat.data
            lon = x.lon.data

            # Considerarem que els punts on tenim dades distintes a nan, son els punts amb dades
            ind = np.isnan(x.data)

            # En cas de que no tenguem que tots els indexos siguin nan
            if not ind.all():

                # Extreim les dades "bones"
                val = x.data[~ind]
                lon_red = x['lon'].data[~ind]
                lat_red = x['lat'].data[~ind]

                # Interpolam
                valInt = fun_int.ObsInterpolats(lon_red, lat_red, lon, lat, val, 2)

                # Actualitzam les dades dolentes
                x.data[ind] = valInt[ind]
                fun.GuardGraf(x, [1, 5], [38, 41], "Balears", df['T'][i])
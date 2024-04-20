#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P4_Iterant.py
@Date    :   2023/12/16 13:03:27
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   2.0

    IB  -->  Per referirnos a les Illes Balears

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

Dades_Sat = pd.DataFrame()
Dades_Tot = pd.DataFrame()

for file in arxius:

    T, sst, lat, lon = fun.DadesMODIS(file)

    Satelit = file.split('_')[0].split('\\')[1]

    data = xr.DataArray(
                        sst, dims=['x', 'y'], 
                        coords = dict(lon=(["x", "y"], lon), 
                                    lat=(["x", "y"], lat))
                        )

    # Elimin les que tenen temperatures inferiors al Antartic (-2)
    sst[sst<-0] = np.nan
    data_red = xr.DataArray(
                            sst, dims=['x', 'y'], 
                            coords = dict(lon=(["x", "y"], lon), 
                                        lat=(["x", "y"], lat))
                            )

    date = dt.datetime.strptime(T, "%Y-%m-%d %H:%M:%S")


    # for la, lo in zip(lats, lons):

    red_data = fun.ZonaZoom(data, lon_Glo, lat_Glo)
    red_data_Posib = fun.ZonaZoom(data_red, lon_Glo, lat_Glo)


    numNan = (np.count_nonzero(np.isnan(red_data.data)))
    Mit = (np.nanmean(red_data.data))
    Med = (np.nanmedian(red_data.data))
    Desv = (np.nanstd(red_data.data))
    Tam = (red_data.size)

    # Per a les dades "reduïdes"
    numNan_red = (np.count_nonzero(np.isnan(red_data_Posib.data)))
    Mit_red = (np.nanmean(red_data_Posib.data))
    Med_red = (np.nanmedian(red_data_Posib.data))
    Desv_red = (np.nanstd(red_data_Posib.data))
    Tam_red = (red_data_Posib.size)

    df = pd.DataFrame(
        {'dia': [T], 'satelit':[Satelit], 
         'Nan':numNan,  'Mitj':Mit,  'Med':Med,  'Desv':Desv, 'Tam':Tam,
         'Nan red':numNan_red, 'Mitj red':Mit_red, 'Med red':Med_red, 
         'Desv red':Desv_red, 'Tam red':Tam_red
         }
        )

    df2 = pd.DataFrame({"Dades" : [red_data], "Dades red" : [red_data_Posib],
                        "T":[T]})
    
    Dades_Sat = pd.concat([Dades_Sat, df], ignore_index=True)
    Dades_Sat = Dades_Sat.sort_values(by='dia')

    Dades_Tot = pd.concat([Dades_Tot, df], ignore_index=True)
    Dades_Tot = Dades_Tot.sort_values(by='dia')

    # Guardam el dataframe per treballar-ne mes endavant
    Dades_Sat.to_pickle("./dataframe.pkl") 
    Dades_Tot.to_pickle("./complete_data.pkl")

print("Programa acabat!")
#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P5_Grafiques1d.py
@Date    :   2023/12/18 15:53:45
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

Analitzam la mitjana i la desviació estandard del SST
per a cada una de les nostres regions d'interés.
'''

import numpy as np
import pandas as pd
import funcions as fun
import matplotlib as mp
import matplotlib.pyplot as plt
from importlib import reload

reload(fun)

mp.rcParams['mathtext.fontset'] = 'stix'
mp.rcParams['font.family'] = 'STIXGeneral'
mp.rcParams.update({'font.size': 17})

df = pd.read_pickle("./dataframe.pkl")

# Miram les files (r --> rows) on tenim nan
r, _ = np.where(df.isna())
r = np.unique(r)

# Miram els indexos on els Nan superen el 50 %.
ind_Bad = []

for var in ['CMe', 'CMa', 'IB']:

    # Supos que quan hi ha menys nans 
    # es quan només es te en compte les illes
    minNan = df['Nan '+var].min()

    aux = np.squeeze(np.where(
        (df['Nan '+var]-minNan)/df['Tam '+ var] > 0.4
        ))
    ind_Bad += aux.tolist()

# Combinam el cas anterior amb  els llocs on son tots nans
ind = np.unique(ind_Bad + r.tolist())

colors = ['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD']

x = df['dia']
Mit_IB, Mit_CMe, Mit_CMa = [df['Mitj ' + var] for var in ['IB', 'CMe', 'CMa']]
Desv_IB, Desv_CMe, Desv_CMa = [df['Desv ' + var] for var in ['IB', 'CMe', 'CMa']]

for M, D, tit, col in zip([Mit_IB, Mit_CMe, Mit_CMa],
                [Desv_IB, Desv_CMe, Desv_CMa], 
                ['Illes Balears', 'Canal de Menorca',
                 'Canal de Mallorca'], range(3)):
    
    # Graficam les dades sense filtrar
    fun.fillPlot(x, M, D, tit, colors[col])
    
    # # Filtram les dades
    # M[ind] = np.nan
    # D[ind] = np.nan

    # # Graficam les dades filtrades
    # fun.fillPlot(x, M, D, tit, colors[col])

colors = ["#0718e9", "#38e416", "#eb3f24"]

fig, ax = plt.subplots(figsize=(12, 10), dpi=400)

i = 0
for Mit, Desv, lab in zip([Mit_IB, Mit_CMa, Mit_CMe],
                          [Desv_IB, Desv_CMa, Desv_CMe],
                          ["Illes Balears", "Canal de Mallorca",
                           "Canal de Menorca"]):
    ax.errorbar(x, Mit, Desv, fmt='o', linewidth=2, capsize=6,
                label=lab, color=colors[i])
    i += 1

ax.grid()
ax.set(xticks=x[::5]) # Reduim les dades a un nombre manejable
ax.set_ylabel('sst (ºC)', fontsize=30)
ax.legend()
fig.autofmt_xdate() # Formata les dates del fons 
plt.show()
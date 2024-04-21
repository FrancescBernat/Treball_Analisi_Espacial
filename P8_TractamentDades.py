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
from importlib import reload

reload(fun)

mp.rcParams['mathtext.fontset'] = 'stix'
mp.rcParams['font.family'] = 'STIXGeneral'
mp.rcParams.update({'font.size': 17})

df = pd.read_pickle("./complete_data.pkl")

# sst que suposam és la temperatura superficial mitjana 
sst_med = 12.34
# sst pel davall suposam que son temperatures falses
sst_min =  6.16 


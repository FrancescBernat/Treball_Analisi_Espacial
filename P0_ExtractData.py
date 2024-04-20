#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P0_ExtractData.py
@Date    :   2023/12/12 16:04:59
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.1

Arxiu per a descarregar totes les dades de Modis sense
haver-ho de fer manualment. 

Segurament hi hagui alguna manera més eficient.

Necesites estar enregistrat en la teva sessió per a que 
te permeti descarregar-te les dades.
'''

import time
import pyautogui
import webbrowser
import urllib.request

# file = "Data2020.txt"

for year in [2018, 2017]:#[2020, 2021, 2022, 2023, 2024]:
    
    with open(f"Data{year}.txt", 'r') as f:
        Lines = f.readlines()

    for l in Lines:

        # Obri en una pestanya del navegador
        webbrowser.open(l)

        # Deixam descansar un temps per a que es descarregui sense problemes
        time.sleep(2)

    print(f"Finished {year}!")
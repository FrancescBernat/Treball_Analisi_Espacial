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

print("Acces the data")
username = str(input("Username: "))
password = str(input("Password: "))

file = "Data2020.txt"

# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login

password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)

# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.
from http.cookiejar import CookieJar
cookie_jar = CookieJar()

# import requests
# from requests.auth import HTTPBasicAuth

# theurl= 'myLink_queriedResult/result.xls'
# username = 'myUsername'
# password = 'myPassword'

# r=requests.get(theurl, auth=HTTPBasicAuth(username, password))
# Install all the handlers.

opener = urllib.request.build_opener(
    urllib.request.HTTPBasicAuthHandler(password_manager),
    #urllib.request.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib.request.HTTPSHandler(debuglevel=1),   # details of the requests/responses
    urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)

with open(file, 'r') as f:
    Lines = f.readlines()

for l in Lines:

    # if i == 0:
    #     # Obri en una pestanya del navegador
    #     webbrowser.open(l)

    #     # Deixam descansar un temps per a que es descarregui sense problemes
    #     time.sleep(60)
        
    # else:
    #     # Obri en una pestanya del navegador
    #     webbrowser.open(l)

        # Deixam descansar un temps per a que es descarregui sense problemes
        # time.sleep(3)
    name = l.split('/')[-1].split('.')
    urllib.request.urlretrieve(l, f"{name[0]}.{name[1]}.{name[2]}.{name[3]}.nc")

    # Tancam el navegador (el que fa és "pitjar" les
    # tecles "ctrl" i "w" alhora --> Combinació que si 
    # estas en el navegador tanca la pestanya)
    # pyautogui.hotkey('ctrl', 'w')
    # print("tab closed \n")

print("Finished!")
#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   P7_CrearGifs.py
@Date    :   2023/12/20 16:12:11
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0

Generam gif's amb totes les imatges descarregades previament.
'''

import glob
import imageio

# subfolders = ['IB', 'CMe',  'CMa', 'Glob']
# folders = ['Imatges/'+i for i in subfolders]

folder = "Balears"
name = "SST_Interpolat"

filenames = glob.glob(folder+"/*.png")

# Anam afegit les imatges a una carpeta
images = []
for filename in filenames:
    images.append(imageio.imread(filename))

# Guarda les imatges dins aquesta carpeta com a un gif
imageio.mimsave(name+'.gif', images,
                format='GIF', duration=900)
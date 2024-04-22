#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   funcions_interp.py
@Date    :   2024/04/22 02:50:38
@Author  :   Francesc Bernat Bieri Tauler 
@Version :   1.0
'''

import numpy as np
import pandas as pd

def P(x, y, ordre):
    """
        Funció que calcula la matriu P per un polinomi
        de ordre n.

        En general, ho calcula pel cas bidimensional (x, y).
        Però, si y està buida, només ho fara per a la x.
    """
    x = x.flatten()
    
    if not len(y):
        P = np.ones([ordre+1, len(x)])

        for i in range(ordre):
            i += 1
            P[i] = x**i

        return P
    
    else:
        y = y.flatten()

        P = np.ones([1, len(x)])
        aux = np.ones([2, len(x)])

        for i in range(ordre):
            i += 1
            aux[0] = x**i
            aux[1] = y**i 
            P = np.append(P, aux, axis=0)
        
        if ordre > 1:
            
            for i, j in zip(range(1, ordre), range(1, ordre)):

                aux2 = np.array( [(x**i)*(y**j)] )

                # print(aux2.shape, P.shape)

                P = np.append(P, aux2, axis=0)

                while i-1:
                    aux2 = np.array([(x**(i-1))*(y**j)])
                    P = np.append(P, aux2, axis=0)

                    aux2 = np.array([(x**i)*(y**(j-1))])
                    P = np.append(P, aux2, axis=0)
                    i -= 1


            
        return P

def alpha(P, valors):
    """
        Funció amb la que, a partir de la matriu P
        i els valors, retorna els parametres del
        polinomi de ordre n.
    """


    a1 = np.linalg.inv( np.dot(P, P.transpose()) )

    a2 = np.dot(P, valors)

    return np.dot(a1, a2)

def ObsInterpolats(x, y, xg, yg, val, ordre=1):
    """
        Funció que retorna els valors interpolats de 
        ordre n, sent ordre 1 l'ordre que retorna per defecte.
    """

    # Calculam P i alpha dels valors
    P1 = P(x, y, ordre)
    alpha1 = alpha(P1, val)

    # Obtenim les dades interpolades
    dades = np.dot(P(xg, yg, ordre).transpose(), alpha1)
    dades = np.reshape(dades, xg.shape)

    return dades
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 18:03:43 2022

@author: SIDBE ISSIAKA
"""

def entryInt(valeur):
    if valeur:
        if int(valeur):
            return True
        else:
            return False
    return False

def valeurSaisir(value):
    if entryInt(value.get()):
        return int(value.get())
    else:
        #value.delete(0,END)
        value.insert(0,"20")
        return 20

def entryFloat(valeur):
    if valeur:
        if float(valeur):
            return True
        else:
            return False
    return False

def AngleSaisir(angle):
    if entryFloat(angle.get()):
        return float(angle.get())
    else:
        #angle.delete(0,END)
        angle.insert(0,"55")
        return 55
    
def lienSaisir(value_lien):
    if entryFloat(value_lien.get()):
        return float(value_lien.get())
    else:
        #value_lien.delete(0,END)
        #value_lien.insert(0,"0")
        return 1


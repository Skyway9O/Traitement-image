# coding : utf-8
import os
'''
Exploration de fichiers.
Fournit les chemins absolus de fichiers à ouvrir, ou à sauvegarder.
Olivier Crelerot janvier 2020
'''

from tkinter import *
from tkinter.filedialog import * #cf http://tkinter.fdex.eu/doc/popdial.html?highlight=file#askopenfilename
from tkinter.messagebox import *

dir_path = os.path.dirname(os.path.realpath(__file__)) # mémorise le répertoire courant
def choixFichier():
    '''
    Permet de sélectionner un fichier avec l'explorateur.
    Retourne le chemin absolu du fichier sous forme de chaîne.
    '''
    w = Tk() # fenetre vide
    nomDeFic = askopenfilename(initialdir = dir_path, defaultextension='.*',title='Sélectionner un fichier', parent = w)
    w.destroy()
    return nomDeFic

def sauveSous():
    '''
    Permet de définir un nom de fichier à sauvegarder, avec l'explorateur.
    Retourne le chemin absolu du fichier sous forme de chaîne.
    '''
    w = Tk() # fenetre vide
    nomDeFic = asksaveasfilename(initialdir = dir_path, defaultextension='.*',title='Enregsitrer sous', filetypes=[("All files","*.*"),("txt","*.txt"), ("csv","*.csv")], parent = w)
    w.destroy()
    return nomDeFic




import fltk
import time
import vect
import math
LARGEUR =800
HAUTEUR =600

def afficher():
    fltk.cree_fenetre(LARGEUR,HAUTEUR)

def fermer():
    fltk.ferme_fenetre()

def swapbuffer():
    fltk.mise_a_jour()

def shouldclose(ev):
    return ev == "Quitte"

afficher()
while True:
    ev =  fltk.donne_ev()
    tev =  fltk.type_ev(ev)
    swapbuffer()
    time.sleep(0.1)
    print(tev)

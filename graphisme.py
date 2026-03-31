import fltk
import time
import vect
import math
LARGEUR =800
HAUTEUR =600


def afficher(repere:False):
    fltk.cree_fenetre(LARGEUR,HAUTEUR,affiche_repere=repere)

def fermer():
    fltk.ferme_fenetre()

def swapbuffer():
    fltk.mise_a_jour()

def shouldclose(ev):
    return ev == "Quitte"





















"""
test

"""
def test():
    afficher(True)
    while True:
        ev =  fltk.donne_ev()
        tev =  fltk.type_ev(ev)
        swapbuffer()
        time.sleep(0.1)
        fltk.rectangle(400,300,420,320)
        if shouldclose(tev):
            break
        print(tev)
if __name__ == "__main__" :
     test()

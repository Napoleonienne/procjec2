from os
from pathlib import Path
import json
from shutil import which
from monde import tuile,niveau
"""
just pour charger les niveau, les asset meme si je vais laisser a fltk  et sauvegarder les niveau 
pour l'instant j'essaye de voir quoi choisir pour sauvegarder peut etre un json ou un csv 
pckle mais je pense pas je pourrait pas modifier le fichier directement 
    
csv est poour l'instant ce qui collle le mieux avec le principe de niveau
un syteme de tuile et de layout colle bien

vue autemp  de truc est charger sa va etre la partie sauvegarde asset et mettre une id pour chaque point 

"""

def dump_niveau(niveau:niveau,name):
    
    

    d = {fond:niveau.}
    ch_savegarde:Path = Path('fichier jeux/save')
    if not ch_savegarde.exists():
        os


    with open(chemin) as f:
        json.dump()
        


def charger_niveau(nom:str):
    with open(chemin) as f:
        contenu = json.load(f)





    return



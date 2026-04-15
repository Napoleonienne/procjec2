from ospath, 
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
    
    

    d = {fond:niveau.fond,decor:niveau.decor,terrain:niveau.terrain}
    ch_savegarde:Path = Path('fichier jeux/save').glob()

    with open(ch_savegarde) as f:
        json.dump(d,f)
        


def charger_niveau(nom:str):
    ch_savegarde:Path = Path('fichier jeux/save')

    for ch in ch_savegarde.glob(''):
        ch.
        

    





    return



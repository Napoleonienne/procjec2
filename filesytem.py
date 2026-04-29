import os
import sys
from pathlib import Path
import json
from shutil import which
from plmace_holder import tuile,sprite
from monde import niveau
"""
just pour charger les niveau, les asset meme si je vais laisser a fltk  et sauvegarder les niveau 
pour l'instant j'essaye de voir quoi choisir pour sauvegarder peut etre un json ou un csv 
pckle mais je pense pas je pourrait pas modifier le fichier directement 
    
csv est poour l'instant ce qui collle le mieux avec le principe de niveau
un syteme de tuile et de layout colle bien

vue autemp  de truc est charger sa va etre la partie sauvegarde asset et mettre une id pour chaque point 

"""

def resource_path(relative_path)->str:
    """
    Obtient le chemin absolu vers une ressource pour la compilation avec PyInstaller. 
    ARGs:
        relative_path:le chemin relative du fichier
        
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def dump_niveau(niveau:niveau,name):
    
    

    d = {fond:niveau.fond,decor:niveau.decor,terrain:niveau.terrain}
    ch_savegarde:Path = Path('fichier jeux/save').glob()

    with open(ch_savegarde) as f:
        json.dump(d,f)
        


def charger_niveau(nom:str):
    ch_savegarde:Path = Path('fichier jeux/save')
    fichier = ch_savegarde / f"{nom}.json"

    for ch in ch_savegarde.glob(''):
        if ch.stem == nom:
            with open(ch) as f:
                d = json.load(f)
                return niveau(d['fond'],d['decor'],d['terrain'])
        


    return



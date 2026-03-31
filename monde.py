from pathlib import Path
from vect import vec2
from dataclasses import dataclass
class joueur:
    def __init__(self,pos):
        self.position =pos
        self.vistesse =0.0
        self.poid=12
        self.direction =vec2
    

    


def charger_asset():



    return

class niveau:
    """
    sera la classe qui me permetera de creer des niveau
    j'imagine pour l'inssant un syteme de tilemap pour me faciliter 
    autre probablement modifier l'iddé pour que 
    
    """
    def __init__(self):
        self.layout:list[tuile] = []
        self.decor:list[tuile] = []

@dataclass
class tuile:
    """
    tile va juste etre la classe ou sera derivé les autre element sur les jeux c'est
    donc on va faire de heritage
    je vais probablement pas utiliser les forme comme les rectangle ou autre integrer a fltk on va faire plus complexe · 
    """
    taille:int =20
    textture:str = ""
    pos:vec2 =vec2()



        

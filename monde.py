from pathlib import Path
from dataclasses import dataclass
import vect
vec2 = vect.Vec2


class joueur:
    """
    classe du joueur comme je vais etyre sur de ecs c'est une une dataclass que je mettrais a jour grace aux syteme du jeu
    """
    def __init__(self,pos:vec2):
        self.position:vec2 =pos
        self.vistesse:float =0.0
        self.poid:float=12
        self.direction:vec2 =vec2()
        self.texture:str
    

    


def charger_asset():



    return

class niveau:
    """
    sera la classe qui me permetera de creer des niveau
    j'imagine pour l'inssant un syteme de tilemap pour me faciliter 
    autre probablement modifier l'iddé pour que 
    
    """
    def __init__(self):
        self.fond:str ="",      # Image de fond
        self.decor:list[tuile] =[],     # Tuiles décoratives (sans collision)
        self.terrain:list[tuile] =[],   # Tuiles solides (avec collision)
        self.devant:str = []     # Éléments de premier plan encore a determiner a utilit peut ere pour des decor plus complexe
        
    

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



        

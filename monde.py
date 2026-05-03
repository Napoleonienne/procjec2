from pathlib import Path
from dataclasses import dataclass
from graphisme import HAUTEUR, LARGEUR, TAILE_TUILE
from filesytem import resource_path 
import graphisme
import vect
from place_holder import tuile,sprite
vec2 = vect.Vec2
import fltk




class joueur:
    """
    
    """
    def __init__(self,pos:vec2):
        self.sprite:sprite = sprite(pos,resource_path("asset/joueur/mouton.png"))
        self.position:vec2 =pos
        self.vitesse:float =0.0
        self.poids:float=12

        self.direction:vec2 =vec2()

        self.bouger:bool = True
    def get_direction(self):
        return self.direction
    
    def get_vitesse(self):
        return self.vistesse
    def sauter(self,dir:vec2):
        self.vistesse += 10
        self.direction = dir
        self.position += vect.normalize(self.direction) * self.vistesse
        b = (self.position/i for i in range(24,0,-1))
    
    def afficher(self):
        graphisme.afficher(self.sprite.texture,self.position)

    @property
    def coin_haut_gauche(self) -> vec2:
        return self.position - self.sprite.taille/2
    @property
    def coin_bas_droit(self) -> vec2:
        return self.position + self.sprite.taille/2
    
    



    



class niveau:
    """

    
    """
    def __init__(self,debut:vec2):
        self.debut:vec2 = debut
        self.fond:str ="",      # Image de fond
        self.decor:graphisme.Grille =graphisme.Grille(32),     # Tuiles décoratives (sans collision)
        self.terrain:graphisme.Grille =graphisme.Grille(32),   # Tuiles solides (avec collision)
        self.devant:list[sprite] = []     # Éléments de premier plan encore a determiner a utilit peut ere pour des decor plus complexe
    

    def afficher_fond(self):
        fltk.image(0,0,self.fond,HAUTEUR,LARGEUR)
    def afficher_decor(self):
        for tuile in self.decor:
            graphisme.positionner_grille(tuile.textture,tuile.pos)

    def afficher_terrain(self):
        for tuile in self.terrain:
            graphisme.positionner_grille(tuile.textture,tuile.pos)
    def afficher_devant(self):
        for other in self.devant:
            graphisme.positionner_grille(other.textture,other.pos)




        

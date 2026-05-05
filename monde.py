import logging
from os import name
from pathlib import Path
from dataclasses import dataclass
from graphisme import HAUTEUR, LARGEUR

import graphisme
import vect
from place_holder import Sprite, Tuile
vec2 = vect.Vec2
import fltk




class joueur:
    """
    
    """
    def __init__(self,pos:vec2):
        self.sprite:Sprite = Sprite(pos,graphisme.resource_path("asset/joueur/mouton.png"))
        self.vitesse:vec2 =vec2()
        self.poids:float=12

        self.direction:vec2 =vec2()

        self.bouger:bool = True
    def get_direction(self):
        return self.direction
    @property
    def position(self):
        return self.sprite.pos
    @position.setter
    def position(self, value: vec2):
        self.sprite.pos = value
    
  
    
    def get_vitesse(self):
        return self.vitesse

    
    def afficher(self):
        self.sprite.afficher()

    @property
    def coin_haut_gauche(self) -> vec2:
        return self.position - self.sprite.taille/2
    @property
    def coin_bas_droit(self) -> vec2:
        return self.position + self.sprite.taille/2
    

    
    



    



class niveau:
    """

    
    """
    def __init__(self,debut:vec2,fin:vec2):
        self.debut:vec2 = debut
        self.fond:str = ""      # Image de fond
        self.avant : graphisme.Grille = graphisme.Grille(32)    #aux cas ou
        self.decor:graphisme.Grille = graphisme.Grille(16)     # Tuiles décoratives (sans collision pas forcement a utiliser pour le decor mais sa peut etre plus simple pour la gestion de l'affichage)
        self.terrain:graphisme.Grille = graphisme.Grille(16)   # Tuiles solides (avec collision a utiliser pour le terrain)
        self.objet:graphisme.Grille = graphisme.Grille(8)     # Tuiles détaillées sans but précis
        self.devant:list[Sprite] = []     #  encore a determiner a utilit peut ere pour des decor plus complexe

        self.point_fin:vec2 = vec2(0,0) # Point d'arrivé du niveau
    

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
    
    def serialisation(self) -> dict[str, any]:
        """
        serialise le niveau pour la sauvegarde en json

        Returns:
            dict[str, any]: le niveau serialisé sous forme de dictionnaire {
                "debut": {"x": self.debut.x, "y": self.debut.y}, debut du niveau
                "point_fin": {"x": self.point_fin.x, "y": self.point_fin.y}, fin du niveau
                "fond": self.fond,   string de l'image de fond
                "avant": self.avant.serialisation(), serialisation de la grille avant de 32 pixels
                "decor": self.decor.serialisation(), serialisation de la grille decor de 16 pixels
                "terrain": self.terrain.serialisation(), serialisation de la grille terrain de 16 pixels
                "objet": self.objet.serialisation(), serialisation de la grille objet de 8 pixels
                "devant": [sprite.serialisation() for sprite in self.devant], serialisation de la liste de sprite devant
        
            
            }

        """
        logging.debug("niveau : Sérialisation du niveau pour le JSON")
        return {
            "debut": {"x": self.debut.x, "y": self.debut.y},
            "point_fin": {"x": self.point_fin.x, "y": self.point_fin.y},
            "fond": self.fond,
            "avant": self.avant.serialisation(),
            "decor": self.decor.serialisation(),
            "terrain": self.terrain.serialisation(),
            "objet": self.objet.serialisation(),
            "devant": [sprite.serialisation() for sprite in self.devant],
        }




        

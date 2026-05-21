import logging
from typing import Any

import graphisme
import vect
from place_holder import Sprite, Tuile,Object2d
vec2 = vect.Vec2
import fltk
from graphisme import chemin_absolue



class joueur(Object2d):
    """
    
    """
    def __init__(self,pos:vec2):
        texture = chemin_absolue("fichier_jeux/joueur/mouton.png")
        taille = vec2(0.06, 0.1)
        super().__init__(pos, texture, taille)
        self.sprite: Sprite = Sprite(pos, graphisme.chemin_absolue("fichier_jeux/joueur/mouton.png"),taille)
        self.vitesse:vec2 =vec2()
        self.poids:float=12

        self.direction:vec2 =vec2()

        self.bouger:bool = True
    def get_direction(self):
        return self.direction
    @property
    def position(self):
        return self.pos
    @position.setter
    def position(self, value: vec2):
        self.pos = value
    
  
    
    def get_vitesse(self):
        return self.vitesse

    
    def afficher(self) -> None:
        graphisme.afficher(self.sprite)

    @property
    def coin_haut_gauche(self) -> vec2:
        return self.sprite.coin_haut_gauche
    @property
    def coin_bas_droit(self) -> vec2:
        return self.sprite.coin_bas_droit
    

    
    



    



class niveau:
    """

    
    """
    def __init__(self,debut:vec2 | None = None,fin:vec2 | None = None):
        """_summary_

        Args:
            debut (vec2): debut du niveau
            fin (vec2): fin du niveau
        """
        logging.debug(f"creation du niveau")
        self.debut:vec2 = debut or vec2(0.06, 0.9)
        self.fond:str = ""      # Image de fond
        self.avant = graphisme.Grille(32,"avant")    #aux cas ou
        self.decor = graphisme.Grille(16,"decor")     # Tuiles décoratives (sans collision pas forcement a utiliser pour le decor mais sa peut etre plus simple pour la gestion de l'affichage)
        self.terrain = graphisme.Grille(16,"terrain")   # Tuiles solides (avec collision a utiliser pour le terrain)
        self.devant = graphisme.Grille(8,"devant")     # Tuiles détaillées sans but précis
        self.plan_object:list[Sprite] = []     #  encore a determiner a utilit peut ere pour des decor plus complexe

        self.gravite:vec2 = vec2(0, 5.0)

        self.point_fin:vec2 = fin or vec2(0.94, 0.9) # Point d'arrivé du niveau


    

    def afficher_fond(self):
        graphisme.afficher_fond(self.fond, tag="fond")


    def afficher_decor(self):
        self.decor.afficher()

    def afficher_terrain(self):
        self.terrain.afficher()
    def afficher_devant(self):
        for other in self.plan_object:
            graphisme.afficher(other)
    
    def serialisation(self) -> dict[str, Any]:
        """
        serialise le niveau pour la sauvegarde en json

        Returns:
            dict[str, any]: le niveau serialisé sous forme de dictionnaire {
                "debut": {"x": self.debut.x, "y": self.debut.y}, debut du niveau
                "point_fin": {"x": self.point_fin.x, "y": self.point_fin.y}, fin du niveau
                "fond":  string de l'image de fond
                "avant":  serialisation de la grille avant de 32 pixels
                "decor": serialisation de la grille decor de 16 pixels
                "terrain":  serialisation de la grille terrain de 16 pixels
                "objet":  serialisation de la grille objet de 8 pixels
                "devant":  for sprite in self.devant], serialisation de la liste de sprite devant
      
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
            "objet": self.devant.serialisation(),
            "devant": [sprite.serialisation() for sprite in self.plan_object],
        }



        

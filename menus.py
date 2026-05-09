from typing import Callable, Optional

import place_holder
from vect import Vec2
import graphisme
import vect


class Menu:
    def __init__(self,name: str,fond:str,logo:Optional[str] = None) -> None:
        self.name:str = name
        self.bouton:list[graphisme.Bouton]  = []
        self.fond:str = fond
        self.logo:Optional[str] = logo
        self.pos_logo = Vec2(0.5, 0.12)
        self.dim_logo = Vec2(0.1, 0.09)



    def ajouter_bouton(self,pos:Vec2,dim:Vec2,action:Callable,texte:str):
        self.bouton.append(graphisme.Bouton(pos,dim,texte,action,))

    def afficher(self):
        if self.fond:
            graphisme.afficher_fond(self.fond,tag=self.name)
        if self.logo:
            j =place_holder.Sprite(self.pos_logo,self.logo,self.dim_logo)
            graphisme.afficher(j, tag=f"{self.name}")
        for bouton in self.bouton:
            bouton.afficher()



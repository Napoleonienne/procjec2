from vect import Vec2
import graphisme
import vect


class Menu:
    def __init__(self,name: str,fond:str) -> None:
        self.name = name
        self.bouton:list[graphisme.Bouton]  = []
        self.fond:str = fond

    def ajoiuuter_bouton(self,pos:Vec2,dim:Vec2,action:callable,texte:str):
        self.bouton.append(graphisme.Bouton(pos,dim,texte,action))
    def afficher(self,screen):
        graphisme.afficher_fond(screen,self.fond)
        for bouton in self.bouton:
            bouton.afficher()
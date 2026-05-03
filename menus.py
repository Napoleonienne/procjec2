from vect import Vec2
import graphisme
import vect


class Menu:
    def __init__(self,name: str,fond:str,logo:str = None) -> None:
        self.name = name
        self.bouton:list[graphisme.Bouton]  = []
        self.fond:str = fond
        self.logo:str = logo
        self.pos_logo = Vec2(0.5 * graphisme.LARGEUR, 0.02 * graphisme.HAUTEUR)
        self.dim_logo = Vec2(0.1 * graphisme.LARGEUR, 0.09 * graphisme.HAUTEUR)



    def ajouter_bouton(self,pos:Vec2,dim:Vec2,action:callable,texte:str):
        self.bouton.append(graphisme.Bouton(pos,dim,texte,action,texture))
    def afficher(self,screen):
        if self.fond:
            graphisme.afficher_fond(screen,self.fond)
        if self.logo:
            graphisme.afficher_sprite(self.logo,self.pos_logo,self.dim_logo)
        for bouton in self.bouton:
            bouton.afficher()




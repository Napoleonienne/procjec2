from filesytem import resource_path
import graphisme
from vect import Vec2 as vec2




class tuile:
    """
    je vais probablement pas utiliser les forme comme les rectangle ou autre integrer a fltk on va faire plus complexe · 

    """
    taille_tuile = 20
    def __init__(self,pos:vec2,texture:str):
        self.textture:str = texture
        self.taille:vec2 = vec2(graphisme.TAILE_TUILE,graphisme.TAILE_TUILE)
        self.pos:vec2 = pos

    def get_pos(self):
        return self.pos

    def get_taille(self):
        return self.taille

    def set_pos(self,pos:vec2):
        self.pos = pos

    def set_taille(self,taille:vec2):
        self.taille = taille

    

    


class sprite:
    """
    classe de sprite qui va etre la classe de base pour les personnage et les objet du jeu
    qui a une position libre et une taille libre
    """
    def __init__(self,pos:vec2,texture:str):
        self.texture:str = texture
        self.taille:vec2 = vec2()
        self.pos:vec2 = pos


    def get_pos(self):
        return self.pos

    def get_taille(self):
        return self.taille

    def set_pos(self,pos:vec2):
        self.pos = pos

    def set_taille(self,taille:vec2):
        self.taille = taille

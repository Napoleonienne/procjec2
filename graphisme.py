import math

import fltk
import time
import vect
import logging
from typing import Optional,Callable

from filesytem import resource_path



Vec2 = vect.Vec2
TAILE_TUILE:int = 32
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='w'         
)
LARGEUR =800
HAUTEUR =600




def afficher(repere:bool = False):
    """_summary_

    Args:
        repere (False): permmet ouvrir une fenetre
    """
    logging.info("ouverture de fenetre")
    fltk.cree_fenetre(LARGEUR,HAUTEUR,affiche_repere=repere)

def fermer():
    """
    permet de fermet la fenetre
    """
    logging.info("fermeture de fenetre")
    fltk.ferme_fenetre()

def swapbuffer():
    """
    permet echanger image avec celle pré gener par le gpu
    """
    fltk.mise_a_jour()

def shouldclose(ev:str|None):
    """_summary_

    Args:
        ev (str): _description_

    Returns:
        _type_: _description_
    """
    logging.info(f"fin du programme avec l'event {ev}")
    return ev == "Quitte"
def palier(vec:Vec2)->Vec2:
    """fonction de snapping qui met une position dans la tuile apprprié

    Args:
        vec (Vec2): coordoné entrer

    Returns:
        Vec2: coordonné de la case ou est le point vec
    """
  
   
    new_vec:Vec2 = Vec2(vec.x //TAILE_TUILE+.5,vec.y//TAILE_TUILE+.5) *TAILE_TUILE
    return new_vec
def positionner_grille(path:str,tile:Vec2):
    """_summary_

    Args:
        path (str): chemin 
        tile (Vec2): position dans la grille
    """

    nv:Vec2 =palier(tile)
    fltk.image(nv.x,nv.y,path,TAILE_TUILE,TAILE_TUILE)


def afficher_sprite(path:str,pos:Vec2,taile:Vec2):
    """
    permmet afficher un sprite quelque soit sa taille et sa position dans la fenetre

    Args:
        path (str): chemin de l'image
        pos (Vec2): position ou afficher le sprite
        taile (Vec2): taille du sprite
    """
    fltk.image(pos.x,pos.y,path,taile.x,taile.y)

class button:
    def __init__(self,pos:Vec2,
                 dim:tuple[Vec2,Vec2]
                 ,text:str,
                 action_clique:Callable
                 ) -> None:
        logging.info(f"creation du bouton {text} a la position {pos} avec les dimensions {dim}")
        self.id:list[int]=[]
        global LARGEUR,HAUTEUR
        self.p1 =  Vec2()
        self.p2  =  Vec2()

        self.text:str = text
        self.action_clique:Callable = action_clique

        taille_texte:int =  20
        estim_largeur_texte = len(text) * (taille_texte * 0.35)
        estim_hauteur_texte = len(text) * (taille_texte * 0.5)
        self.activer:bool = False

        self.pos_texte:tuple = (0,0)



    def action(self,ev):
        logging.info(f"action du bouton {self.text}")
        tev:str|None = fltk.type_ev(ev)
        if tev != "ClicDroit":
            return
        x = fltk.abscisse(ev)
        y = fltk.ordonnee(ev)
        if x is None or y is None:
            return

        if  self.p1.x < x <self.p2.x and  self.p1.y <y <self.p2.y and self.activer == True:
            self.action_clique()


    def set_area(self,area:tuple[Vec2,Vec2])->None:
        """_summary_

        Args:
            area (tuple[Vec2,Vec2]): _description_
        """
        self.p1 =  area[0]
        self.p2  =  area[1]
    def get_area(self)->tuple[Vec2,Vec2]:
        return (self.p1,self.p2)
    
    def set_text(self,text:str)->None:
        self.text = text


    
    def afficher(self):
        """
        va afficher le buton
        """
        self.id.append(fltk.rectangle(self.p1.x,self.p1.y,self.p2.x,self.p2.y))
        self.id.append(fltk.texte(self.pos_texte[0],self.pos_texte[1],self.text))
        self.activer = True
        return
    def suppr_affichage(self):
        for i in self.id:
            fltk.efface(i)
        self.activer = False
        return
    
    def suppr(self):
        for i in self.id:
            fltk.efface(i)
        return
    


        








    
    

import itertools





def test():
    """_summary_

    """
    afficher(True)

    for i in range(0,LARGEUR,TAILE_TUILE):
        for j in range(0,HAUTEUR,TAILE_TUILE):
            fltk.rectangle(i,j,i+TAILE_TUILE,j+TAILE_TUILE,"red")

    k = itertools.product(range(0,LARGEUR+1,10),range(0,HAUTEUR+1,10))

    afficher_sprite("asset/joueur/mouton.png",Vec2(100,100),Vec2(32,32))

    abj:bouton = button(Vec2(),(Vec2(100,100),Vec2(200,200)),"test",lambda : print("test"))
    
            
        

    while True:
        ev =  fltk.donne_ev()
        tev =  fltk.type_ev(ev)
        swapbuffer()
        time.sleep(0.1)
        positionner_grille("asset/vert.jpg",Vec2(*next(k)))


        if shouldclose(tev):
            break

    fermer()
    return


if __name__ == "__main__" :
    test()

        

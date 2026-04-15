import math

import fltk
import time
import vect
import logging
from typing import Optional,Callable
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
    return ev == "Quitte"
def palier(vec:Vec2)->Vec2:
    """_summary_

    Args:
        vec (Vec2): coordoné entrer

    Returns:
        Vec2: coordonné de la case ou est le point vec
    """
  
   
    new_vec:Vec2 = Vec2(vec.x //TAILE_TUILE+.5,vec.y//TAILE_TUILE+.5) *TAILE_TUILE
    print(new_vec)
    return new_vec
def load_asset(path:str,tile:Vec2):
    """_summary_

    Args:
        path (str): _description_
        tile (Vec2): _description_
    """

    nv:Vec2 =palier(tile)
    fltk.image(nv.x,nv.y,path,TAILE_TUILE,TAILE_TUILE)


class button:
    def __init__(self,pos:Vec2,
                 dim:tuple[Vec2,Vec2]
                 ,text:str,
                 action_clique:Callable
                 ) -> None:
        self.id:list[int]=[]
        global LARGEUR,HAUTEUR
        self.p1 =  Vec2()
        self.p2  =  Vec2()

        self.text:str = text
        self.action_clique:Callable = action_clique

        taille_texte:int =  20
        estim_largeur_texte = len(text) * (taille_texte * 0.35)
        estim_hauteur_texte = len(text) * (taille_texte * 0.5)

        self.pos_texte:tuple = (0,0)

        
        
        







    def action(self,ev):
        tev:str|None = fltk.type_ev(ev)
        if tev != "ClicDroit":
            return
        x = float(fltk.abscisse(ev))
        y = float(fltk.ordonnee(ev))


        if  self.p1.x < x <self.p2.x and  self.p1.y <y <self.p2.y :
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
        return
    
    def suppr(self):
        for i in self.id:
            fltk.efface(i)
        return
    

        
        








    
    









def test():
    """_summary_

    """
    afficher(True)

    for i in range(0,LARGEUR,TAILE_TUILE):
        for j in range(0,HAUTEUR,TAILE_TUILE):
            fltk.rectangle(i,j,i+TAILE_TUILE,j+TAILE_TUILE,"red")
    load_asset("asset/vert.jpg",Vec2(790,590))
    
            
        

    while True:
        ev =  fltk.donne_ev()
        tev =  fltk.type_ev(ev)
        swapbuffer()
        time.sleep(0.1)

        if shouldclose(tev):
            break

    fermer()
    return


if __name__ == "__main__" :
     test()

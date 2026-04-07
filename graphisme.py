import fltk
import time
import vect
import math
import logging

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

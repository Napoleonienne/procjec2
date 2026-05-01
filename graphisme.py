import math
from socket import create_server
from turtle import pos

import fltk
import time
import vect
import logging
from typing import Optional,Callable
import place_holder
import sys,os
import time

def resource_path(relative_path)->str:
    """
    Obtient le chemin absolu vers une ressource pour la compilation avec PyInstaller. 
    ARGs:
        relative_path:le chemin relative du fichier
        
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



Vec2 = vect.Vec2
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
def palier(vec:Vec2, taille_tuile:int)->Vec2:
    """fonction de snapping qui met une position dans la tuile apprprié

    Args:
        vec (Vec2): coordoné entrer
        taille_tuile (int): taille d'une tuile

    Returns:
        Vec2: coordonné de la case ou est le point vec
    """
  
   
    new_vec:Vec2 = Vec2(vec.x //taille_tuile+.5,vec.y//taille_tuile+.5) *taille_tuile
    return new_vec



def afficher_tuile(tuile:place_holder.tuile):
    """_summary_

    Args:
        path (str): chemin de l'image
        pos (Vec2): position ou afficher la tuile
        taille (int, optional): taille de la tuile. Defaults to 32.
    """
    pos:Vec2 = tuile.get_pos()
    taille:int = tuile.get_taille()
    texture:str = tuile.get_texture()
    nv_vec:Vec2 = palier(pos,taille)
    fltk.image(nv_vec.x,nv_vec.y,texture,taille)

def positionner_grille(path:str,tile:Vec2,taille:int =32):
    """_summary_

    Args:
        path (str): chemin 
        tile (Vec2): position dans la grille
    """

    nv:Vec2 =palier(tile,taille)
    fltk.image(nv.x,nv.y,path,taille,taille)


def afficher_sprite(path:str,pos:Vec2,taile:Vec2):
    """
    permmet afficher un sprite quelque soit sa taille et sa position dans la fenetre

    Args:
        path (str): chemin de l'image
        pos (Vec2): position ou afficher le sprite
        taile (Vec2): taille du sprite
    """
    fltk.image(pos.x,pos.y,path,taile.x,taile.y)

"""
def creer_bouton(
    donne: Dict[str, Any],
    nom: str,
    taille_t: int,
    texte: str,
    centre: Tuple[float, float],
    dimension: Tuple[float, float],
    remplissage: Optional[str] = None,
    fonction: Optional[Callable] = None
) -> None:
    l, h = donne["dim_f"]
    ax = l * (centre[0] - dimension[0] / 2)
    ay = h * (centre[1] - dimension[1] / 2)
    bx = l * (centre[0] + dimension[0] / 2)
    by = h * (centre[1] + dimension[1] / 2)
    a = texte.split("\n")
    b = max(a, key=len)

    tl,hl =t.taille_texte(texte,taille=taille_t)
    estim_largeur_texte = len(b) * (taille_t * 0.35)
    estim_hauteur_texte = len(a) * taille_t * 0.5

    x_texte = l * centre[0] - estim_largeur_texte
    y_texte = h * centre[1] - estim_hauteur_texte


    if x_texte < ax :
        x_texte =  ax +10
    

    if remplissage:
        t.rectangle(epaisseur=3, ax=ax, ay=ay, bx=bx, by=by, tag=nom, remplissage=remplissage)
    else:
        t.rectangle(epaisseur=3, ax=ax, ay=ay, bx=bx, by=by, tag=nom)

    t.texte(taille=taille_t, chaine=texte, x=x_texte , y=y_texte , tag=nom)
"""


def creer_texte(pos:Vec2,taile:float,texte:str):
    fltk.texte(pos.x,pos.y,texte,taille=taile)
class bouton:
    def __init__(self,pos:Vec2,
                 dim:Vec2
                 ,text:str,
                 action_clique:Callable
                 ) -> None:
        logging.info(f"creation du bouton {text} a la position {pos} avec les dimensions {dim}")
        self.id:list[int]=[]
        global LARGEUR,HAUTEUR
        self.p1:Vec2 =  pos+ dim/2
        self.p2:Vec2  =  pos - dim/2
        p = Vec2(self.p1.x,self.p2.y)

        

        self.text:str = text
        mots = text.split()

        self.action_clique:Callable = action_clique
        len_mot:int = 0
        
        

        taille_texte:int =  20

        self.activer:bool = False

        self.pos_texte:Vec2 = p+ Vec2(-len(text)*taille_texte*0.35,taille_texte*0.5)


    def action(self,ev):
        logging.info(f"action du bouton {self.text}")
        tev:str|None = fltk.type_ev(ev)
        if tev != "ClicGauche":
            return
        x = fltk.abscisse(ev)
        y = fltk.ordonnee(ev)
        if x is None or y is None:
            return

        if  self.p2.x < x <self.p1.x and  self.p2.y <y <self.p1.y and self.activer == True:
            print(f"clic sur le bouton {self.text}")
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

        self.id.append(fltk.rectangle(self.p1.x,self.p1.y,self.p2.x,self.p2.y,
                                      "blue" ,
                                      epaisseur=5))
        self.id.append(creer_texte(self.pos_texte,20,self.text))
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

def creer_grille(taile:int,couleur:str):
    for i in range(0,LARGEUR,taile):
        for j in range(0,HAUTEUR,taile):
            fltk.rectangle(i,j,i+taile,j+taile,couleur)




def test():
    """_summary_

    """
    afficher(True)
    creer_grille(8,"blue")
    creer_grille(16,"yellow")
    creer_grille(32,"red")
    


    k = itertools.product(range(0,LARGEUR+1,16),range(0,HAUTEUR+1,16))

    afficher_sprite("asset/joueur/mouton.png",Vec2(100,100),Vec2(32,32))

    abj:bouton = bouton(Vec2(400,400),Vec2(100,100),"test",lambda : print("test"))
    abj.afficher()

    
            

    while True:
        ev =  fltk.donne_ev()
        tev =  fltk.type_ev(ev)
        swapbuffer()
        time.sleep(0.1)
        positionner_grille("asset/vert.jpg",Vec2(*next(k)),16)
        abj.action(ev)

        if shouldclose(tev):
            break

    fermer()
    return


if __name__ == "__main__" :
    test()

        

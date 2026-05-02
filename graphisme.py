import fltk
import vect
import logging
import time
import os
import sys
from typing import Optional, Callable
import place_holder


def resource_path(relative_path)->str:
    """
    Obtient le chemin absolu vers une ressource pour la compilation avec PyInstaller. 
    ARGs:
        relative_path:le chemin relative du fichier
        
    """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
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
  

    new_vec: Vec2 = Vec2(
        (vec.x + taille_tuile / 2) // taille_tuile * taille_tuile,
        (vec.y + taille_tuile / 2) // taille_tuile * taille_tuile
    )

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
    d =fltk.image(pos.x,pos.y,path,taile.x,taile.y)
    return d



def creer_texte(pos:Vec2,taile:float,texte:str)->int:
    id = fltk.texte(pos.x,pos.y,texte,taille=taile)
    return id



class Bouton:
    """
    classe bouton pour genereer un bouton et ses intrecation dans le monde 
    on  va voir si je me fais chiez a creer les etat quand la souris est dessus
    """
    def __init__(
        self,
        pos: Vec2,
        dim: Vec2,
        text: str,
        action_clique: Callable[[], None],
        couleur: str = "blue",
        couleur_hover: str = "lightblue",
        taille_texte: int = 20,
        tag: Optional[str] = None
    ) -> None:
        logging.info(f"Création du bouton '{text}' à la position {pos} avec la dimension {dim}")
        
        self.pos = pos
        self.dim = dim
        self.text = text
        self.action_clique = action_clique
        self.couleur = couleur
        self.couleur_hover = couleur_hover
        self.taille_texte = taille_texte
        self.actif = True
        self.hover = False
        self.id_rect: Optional[int] = None
        self.id_texte: Optional[int] = None
        self.tag = tag

    @property
    def coin_haut_gauche(self) -> Vec2:
        return self.pos - self.dim / 2

    @property
    def coin_bas_droit(self) -> Vec2:
        return self.pos + self.dim / 2

    def _calculer_pos_texte(self) -> Vec2:
        """Calcule la position pour centrer le texte."""
        largeur_texte, _ = fltk.taille_texte(self.text, taille=self.taille_texte)
        return self.pos - Vec2(largeur_texte / 2, self.taille_texte / 2)

    def afficher(self) -> None:
        """Affiche le bouton et son texte."""
        logging.info(f"Affichage du bouton '{self.text}' à la position {self.pos} avec la dimension {self.dim}")
        self.suppr_affichage()  # Nettoie les anciens IDs
        self.id_rect = fltk.rectangle(
            self.coin_haut_gauche.x, self.coin_haut_gauche.y,
            self.coin_bas_droit.x, self.coin_bas_droit.y,
            self.couleur_hover if self.hover else self.couleur,
            epaisseur=5,
        )
        pos_texte = self._calculer_pos_texte()
        self.id_texte = fltk.texte(
            pos_texte.x, pos_texte.y,
            self.text,
            taille=self.taille_texte,
        )

    def suppr_affichage(self) -> None:
        """Efface le bouton de l'écran."""
        logging.info(f"Suppression de l'affichage du bouton '{self.text}'")
        if self.id_rect:
            fltk.efface(self.id_rect)
        if self.id_texte:
            fltk.efface(self.id_texte)
        self.id_rect = None
        self.id_texte = None

    def action(self, ev) -> None:
        """Gère les interactions avec le bouton."""
        
        if not self.actif:
            return
        tev = fltk.type_ev(ev)
        if tev == "": 
            x, y =  fltk.abscisse_souris(), fltk.ordonnee_souris()
            if x is None or y is None:
                return
            self.hover = (
                self.coin_haut_gauche.x < x < self.coin_bas_droit.x and
                self.coin_haut_gauche.y < y < self.coin_bas_droit.y
            )

        
        elif tev == "ClicGauche":
            x, y = fltk.abscisse(ev), fltk.ordonnee(ev)
            if (
                x is not None and y is not None and
                self.coin_haut_gauche.x < x < self.coin_bas_droit.x and
                self.coin_haut_gauche.y < y < self.coin_bas_droit.y
            ):
                self.action_clique()

        








    

import itertools
class Grille:
    def __init__(self, taille_tuile: int):
        self.taille_tuile = taille_tuile
        self.tuiles = {}  # {(x, y): tuile}

    def ajouter_tuile(self, pos: Vec2, texture: str):
        pos_snappée = palier(pos, self.taille_tuile)
        self.tuiles[(pos_snappée.x, pos_snappée.y)] = place_holder.tuile(pos_snappée, texture, self.taille_tuile)

    def afficher(self):
        for tuile in self.tuiles.values():
            afficher_tuile(tuile)
    
    



def test():
    afficher(True)
    # Afficher une grille statique (pas besoin de recalculer à chaque frame)
    grille = Grille(32)
    grille.ajouter_tuile(Vec2(0, 0), "asset/vert.jpg")
    grille.afficher()


    # Position fixe pour le sprite
    afficher_sprite("asset/joueur/mouton.png", Vec2(100, 100), Vec2(32, 32))

    # Bouton avec gestion du hover
    bouton_test = Bouton(
        pos=Vec2(400, 400),
        dim=Vec2(200, 60),
        text="Test",
        action_clique=lambda: print("Bouton cliqué !"),
    )
    bouton_test.afficher()

    while True:
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)

        # Gestion du hover
        bouton_test.action(ev)

        swapbuffer()
        time.sleep(0.016)  # ~60 FPS

        if shouldclose(tev):
            break

    fermer()


if __name__ == "__main__" :
    test()

        

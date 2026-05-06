from dataclasses import dataclass
import re

import fltk
import vect
import logging
import time
import itertools
import os
import sys
from typing import Optional, Callable, Tuple
from tkinter import Tk, Event as TkEvent
import place_holder


def resource_path(relative_path)->str:
    """
    Obtient le chemin absolu vers une ressource pour la compilation avec PyInstaller. 
    ARGs:
        relative_path:le chemin relative du fichier
        
    """
    logging.debug(f"graphisme : Obtention du chemin absolu pour la ressource '{relative_path}'")
    try:
        base_path = sys._MEIPASS # type: ignore
    except AttributeError:
        base_path = os.path.abspath(".")

    res:str =os.path.join(base_path, relative_path)

    try:
        assert os.path.exists(res)
    except AssertionError:
        logging.error(f"Le fichier suivant n'existe pas : {res}")
        res = os.path.join(base_path, "asset/missing.jpg") 
        logging.warning(f"Utilisation du fichier de secours : {res}")
    
    return res
    



Vec2 = vect.Vec2


HAUTEUR =600
LARGEUR =round(HAUTEUR*16/9)




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


def afficher_sprite(sprite:place_holder.Sprite):
    """permet afficher un object sprite

    Args:
        sprite (place_holder.Sprite): _description_
    """
    logging.info(f"graphisme :Affichage du sprite à la position {sprite.pos} avec la texture '{sprite.texture}' et la taille {sprite.taille}")

    fltk.image(sprite.pos.x, sprite.pos.y, sprite.texture, sprite.taille.x, sprite.taille.y)


    
def fleche(pos1:Vec2,pos2:Vec2):
    """
    permet afficher une fleche entre deux point

    Args:
        pos1 (Vec2): position de depart
        pos2 (Vec2): position d'arriver
    """
    logging.info(f"graphisme : Affichage d'une flèche de {pos1} à {pos2}")


    fltk.fleche(pos1.x,pos1.y,pos2.x,pos2.y,epaisseur=10,couleur="red")


def swapbuffer():
    """
    permet echanger image avec celle pré gener par le gpu
    """
    logging.info("graphisme : Echange du buffer pour afficher la nouvelle image")
    fltk.mise_a_jour()

def shouldclose(ev:evenement):
    """_summary_

    Args:
        ev (str): _description_

    Returns:
        _type_: _description_
    """
    logging.debug(f"graphisme : Vérification de l'événement pour la fermeture de la fenêtre : {ev.type}")

    return ev.type == "Quitte"
def palier(vec:Vec2, taille_tuile:int)->Vec2:
    """fonction de snapping qui met une position dans la tuile apprprié

    Args:
        vec (Vec2): coordoné entrer
        taille_tuile (int): taille d'une tuile

    Returns:
        Vec2: coordonné de la case ou est le point vec
    """
  
    logging.debug(f"graphisme : Snapping de la position {vec} à la grille avec une taille de tuile de {taille_tuile}")
    new_vec: Vec2 = Vec2(
        (vec.x + taille_tuile / 2) // taille_tuile * taille_tuile,
        (vec.y + taille_tuile / 2) // taille_tuile * taille_tuile
    )

    return new_vec



def afficher_tuile(tuile:place_holder.Tuile):
    """permet afficher une tuile

    Args:
        path (str): chemin de l'image
        pos (Vec2): position ou afficher la tuile
        taille (int, optional): taille de la tuile. Defaults to 32.
    """
    logging.info(f"graphisme : Affichage de la tuile à la position {str(tuile.pos)} avec la texture '{tuile.texture}' et la taille {str(tuile.taille)}")
    pos:Vec2 = tuile.pos
    taille:int = tuile.taille
    texture:str = tuile.texture
    nv_vec:Vec2 = palier(pos,taille)
    tuile.id = fltk.image(nv_vec.x,nv_vec.y,texture,taille)

def effacer_tuile(tuile:place_holder.Tuile):
    """_summary_

    Args:
        tuile (place_holder.Tuile): tuile a effacer
    """
    logging.info(f"graphisme : Effacement de la tuile à la position {tuile.pos} avec la texture '{tuile.texture}' et la taille {tuile.taille}")
    if tuile.id != None:
        fltk.efface(tuile.id)
        tuile.id = None

def positionner_grille(path:str,tile:Vec2,taille:int =32):
    """_summary_

    Args:
        path (str): chemin 
        tile (Vec2): position dans la grille
    """

    nv:Vec2 =palier(tile,taille)
    fltk.image(nv.x,nv.y,path,taille,taille)




def creer_texte(pos:Vec2,taile:float,texte:str)->int:
    id = fltk.texte(pos.x,pos.y,texte,taille=taile)
    return id

def afficher_fond(path:str):

    fltk.image(LARGEUR/2,HAUTEUR/2,path,LARGEUR,HAUTEUR)

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
        logging.info(f"graphisme : Création du bouton '{text}' à la position {pos} avec la dimension {dim}")
        
        self.pos = pos
        self.dim = dim
        self.text = text
        self.action_clique = action_clique
        self.couleur = couleur
        self.couleur_hover = couleur_hover
        self.taille_texte = taille_texte
        self.actif = True
        self.hover = False # je sais pas comment faire a part le laisser tourner pendant tout execution de la fenetre pour verifier  mais sa me parait pas ouf
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

    def dessus(self, pos: Vec2) -> bool:
        """Vérifie si une position est au-dessus du bouton."""
        logging.info(f"graphisme : Vérification si la position {pos} est au-dessus du bouton '{self.text}'")
        x, y =  fltk.abscisse_souris(), fltk.ordonnee_souris()
        if x is None or y is None:
            return False
        hover = (
            self.coin_haut_gauche.x < x < self.coin_bas_droit.x and
            self.coin_haut_gauche.y < y < self.coin_bas_droit.y
        )
        return hover

    def action(self, ev:evenement) -> None:
        """Gère les interactions avec le bouton."""
        logging.info(f"graphisme : Gestion de l'événement sur le bouton '{self.text}'")
        if not self.actif:
            return
  
  

        
        elif ev.type == "ClicGauche":
            x, y = fltk.abscisse(ev.data), fltk.ordonnee(ev.data) # type: ignore
            if (
                x is not None and y is not None and
                self.coin_haut_gauche.x < x < self.coin_bas_droit.x and
                self.coin_haut_gauche.y < y < self.coin_bas_droit.y
            ):
                self.action_clique()

        








    

class Grille:
    def __init__(self, taille_tuile: int):
        self.taille_tuile = taille_tuile
        self.tuiles = {}  # {(x, y): tuile}
    def ajouter_tuile(self, pos: Vec2,tuile:place_holder.Tuile):
        pos_snappée = palier(pos, self.taille_tuile)
        self.tuiles[(pos_snappée.x, pos_snappée.y)] = tuile
    
    def get_tuile(self, pos: Vec2) -> Optional[place_holder.Tuile]:
        pos_snappée = palier(pos, self.taille_tuile)
        return self.tuiles.get((pos_snappée.x, pos_snappée.y), None)
    


    def supprimer_tuile(self, pos: Vec2):
        pos_snappée = palier(pos, self.taille_tuile)
        key = (pos_snappée.x, pos_snappée.y)
        if key in self.tuiles:
            del self.tuiles[key]

    def afficher(self):
        for tuile in self.tuiles.values():
            afficher_tuile(tuile)
    def effacer(self):
        for tuile in self.tuiles.values():
            effacer_tuile(tuile)

    def serialisation(self) -> dict[tuple[float, float], dict]:
        """Convertit la grille en une liste de dictionnaires pour la sérialisation dans le json."""
        logging.info("graphisme : Sérialisation de la grille pour le JSON")
        j ={}
        for key, tuile in self.tuiles.items():
            j[(tuile.pos.x, tuile.pos.y)] = tuile.serialisation()
        return j
            
    
    def __iter__(self):
        return itertools.chain(self.tuiles.values())




@dataclass
class evenement:
    type: str | None =""
    data: tuple | None = None


def get_evenement():
    """obtie juste les  evenemznt

    Returns:
        _type_: _description_
    """
    res:evenement = evenement(type=None, data=None)
    res.data = fltk.donne_ev()
    res.type = fltk.type_ev(res.data)
    return res



def test():
    afficher(True)
    # Afficher une grille statique (pas besoin de recalculer à chaque frame)
    grille = Grille(32)
    grille.ajouter_tuile(Vec2(0, 0), "asset/vert.jpg")
    grille.afficher()
    afficher_fond(None,"asset/vert.jpg")


    # Position fixe pour le sprite

    # Bouton avec gestion du hover
    bouton_test = Bouton(
        pos=Vec2(400, 400),
        dim=Vec2(200, 60),
        text="Test",
        action_clique=lambda: print("Bouton cliqué !"),
    )

    bouton_test.afficher()


    while True:
        evenement = get_evenement()

        

        # Gestion du hover
        bouton_test.action(evenement)

        swapbuffer()
        time.sleep(0.016)  # ~60 FPS

        if shouldclose(evenement):
            break

    fermer()


if __name__ == "__main__" :
    logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='graphisme.log',  
    filemode='w'         
)
    test()

        

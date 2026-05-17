from __future__ import annotations

from dataclasses import dataclass
from email.policy import default
import multiprocessing.pool
import operator

import fltk
import vect
import logging
import time
import itertools
import os
from pathlib import Path
import sys
from typing import Optional, Callable, Tuple, overload
from tkinter import Tk, Event as TkEvent
import place_holder
import multiprocessing


def process(f,*kwarg):
    """permet d'executer une fonction dans un processus a part pour pas faire freeze la fenetre

    Args:
        f (function): la fonction a executer
        *kwarg: les argument de la fonction
    """
    logging.info(f"graphisme : Lancement de la fonction '{f.__name__}' dans un processus séparé avec les arguments {kwarg}")
    pool = multiprocessing.Pool(processes=1)
    pool.apply_async(f, kwarg)
    pool.close()


def chemin_absolue(relative_path: str) -> str:
    """
    Obtient le chemin absolu vers une ressource pour la compilation avec PyInstaller. 
    ARGs:
        relative_path:le chemin relative du fichier
        
    """
    logging.debug(f"graphisme : Obtention du chemin absolu pour la ressource '{relative_path}'")
    try:
        base_path = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    except AttributeError:
        base_path = Path(__file__).resolve().parent

    res = base_path / relative_path

    if not res.exists():
        logging.error(f"Le fichier suivant n'existe pas : {res}")

    return str(res)


def _normaliser_chemin(path: str | None) -> str | None:
    if path is None:
        return None
    if os.path.isabs(path):
        return path
    return chemin_absolue(path)
    



Vec2 = vect.Vec2



FENETRE_HAUTEUR = 600
FENETRE_LARGEUR = round(FENETRE_HAUTEUR*16/9)



def definir_fenetre(largeur: int | None = None, hauteur: int | None = None) -> None:
    """
    definir les dimmesion de la fenetre 
    si elle sont changer

    Args:
        largeur (int | None, optional): largeur de la fenetre
        hauteur (int | None, optional): hauteur de la fenetre
    """
    global FENETRE_LARGEUR, FENETRE_HAUTEUR
    if largeur is not None:
        FENETRE_LARGEUR = largeur
    if hauteur is not None:
        FENETRE_HAUTEUR = hauteur





def vers_pixels(vec: Vec2) -> Vec2:
    return Vec2(vec.x * FENETRE_LARGEUR, vec.y * FENETRE_HAUTEUR)


def versCoordonneNormaliser(vec: Vec2) -> Vec2:
    """_summary_

    Args:
        vec (Vec2): la position entrer en pixel

    Returns:
        Vec2: _description_
    """

    return Vec2(vec.x / FENETRE_LARGEUR, vec.y / FENETRE_HAUTEUR)

def verscoordonnefenetre(vec: Vec2) -> Vec2:
    """_summary_

    Args:
        vec (Vec2): la position entrer en coordonné normalisé

    Returns:
        Vec2: _description_
    """
    return Vec2(vec.x * FENETRE_LARGEUR, vec.y * FENETRE_HAUTEUR)


def valeur_pixels(val: float) -> float:
    """
    prend le pourrcentage et le met a echelle de la fenetre
 
    Args:
        val (float): une valeur entre 0 et 1

    Returns:
        float: _description_
    """
    return val * min(FENETRE_LARGEUR, FENETRE_HAUTEUR)




def ouvrir_fenetre(repere:bool = False, largeur: int | None = None, hauteur: int | None = None):
    """_summary_

    Args:
        repere (False): permmet ouvrir une fenetre
    """
    logging.info("ouverture de fenetre")
    definir_fenetre(largeur=largeur, hauteur=hauteur)
    fltk.cree_fenetre(FENETRE_LARGEUR,FENETRE_HAUTEUR,affiche_repere=repere)

def fermer():
    """
    permet de fermet la fenetre
    """
    logging.info("fermeture de fenetre")
    fltk.ferme_fenetre()


def fleche(pos1:Vec2,pos2:Vec2,epaisseur:float = 0.01,tag:str ="fleche joueur"):
    """
    permet afficher une fleche entre deux point

    Args:
        pos1 (Vec2): position de depart
        pos2 (Vec2): position d'arriver

    """
    logging.info(f"graphisme : Affichage d'une flèche de {pos1} à {pos2}")


    pos1_pixels = vers_pixels(pos1)
    pos2_pixels = vers_pixels(pos2)
    epaisseur = max(1, round(valeur_pixels(epaisseur)))
    id = fltk.fleche(
        pos1_pixels.x,
        pos1_pixels.y,
        pos2_pixels.x,
        pos2_pixels.y,
        epaisseur=epaisseur,
        couleur="red",
        tag=tag
    )

def supprimer_el(tag:str|int):
    """
    permet de suprimer tout les element d'un tag

    Args:
        tag (str): le tag ou id a suprimer
    """
    logging.info(f"graphisme : Suppression de tous les éléments avec le tag '{tag}'")
    fltk.efface(tag)




def swapbuffer():
    """
    permet echanger image avec celle pré gener par le gpu
    """
    logging.info("graphisme : Echange du buffer pour afficher la nouvelle image")
    fltk.mise_a_jour()

def effacerTout() -> None:
    """Efface tout le contenu actuellement affiché."""
    fltk.efface_tout()

def shouldclose(ev: evenement | None) -> bool:
    """_summary_

    Args:
        ev (str): _description_

    Returns:
        _type_: _description_
    """
    if ev is None:
        return False
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







def creer_texte(pos:Vec2,taile:float,texte:str)->int:
    pos_pixels = vers_pixels(pos)
    taille_pixels = max(1, round(valeur_pixels(taile)))
    id = fltk.texte(pos_pixels.x,pos_pixels.y,texte,taille=taille_pixels)
    return id

def afficher_fond(path: str | None, tag):
    chemin = _normaliser_chemin(path)
    if chemin is None:
        return
    centre = vers_pixels(Vec2(0.5, 0.5))
    taille = vers_pixels(Vec2(1.0, 1.0))
    fltk.image(
        round(centre.x),
        round(centre.y),
        chemin,
        round(taille.x),
        round(taille.y),
        tag=tag,
    )


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
        taille_texte: float = 0.03,
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

    def _calculer_pos_texte(self, taille_texte_pixels: float) -> Vec2:
        """Calcule la position pour centrer le texte."""
        
        largeur_texte, _ = fltk.taille_texte(self.text, taille=taille_texte_pixels) # type: ignore
        centre_pixels = vers_pixels(self.pos)
        return centre_pixels - Vec2(largeur_texte / 2, taille_texte_pixels / 2)

    def afficher(self) -> None:
        """Affiche le bouton et son texte."""
        logging.info(f"Affichage du bouton '{self.text}' à la position {self.pos} avec la dimension {self.dim}")
        self.suppr_affichage()  # Nettoie les anciens IDs
        coin_haut_gauche_pixels = vers_pixels(self.coin_haut_gauche)
        coin_bas_droit_pixels = vers_pixels(self.coin_bas_droit)
        epaisseur = max(1, round(valeur_pixels(0.005)))
        taille_texte_pixels = max(1, round(valeur_pixels(self.taille_texte)))
        self.id_rect = fltk.rectangle(
            coin_haut_gauche_pixels.x, coin_haut_gauche_pixels.y,
            coin_bas_droit_pixels.x, coin_bas_droit_pixels.y,
            self.couleur_hover if self.hover else self.couleur,
            epaisseur=epaisseur,
            tag=self.tag
        )
        pos_texte = self._calculer_pos_texte(taille_texte_pixels)
        self.id_texte = fltk.texte(
            pos_texte.x, pos_texte.y,
            self.text,
            taille=taille_texte_pixels,
            tag=self.tag
        )


    def suppr_affichage(self) -> None:
        """Efface le bouton de l'écran."""
        logging.info(f"Suppression de l'affichage du bouton '{self.text}'")
        if self.id_rect:
            fltk.efface(self.id_rect)
        if self.id_texte:
            fltk.efface(self.id_texte)

        self.actif = False
        self.id_rect = None
        self.id_texte = None

    def dessus(self, pos: Vec2) -> bool:
        """Vérifie si une position est au-dessus du bouton."""
        logging.info(f"graphisme : Vérification si la position {pos} est au-dessus du bouton '{self.text}'")
        x, y =  fltk.abscisse_souris(), fltk.ordonnee_souris()
        if x is None or y is None:
            return False
        pos_pixels = versCoordonneNormaliser(Vec2(x, y))
        hover = (
            self.coin_haut_gauche.x < pos_pixels.x < self.coin_bas_droit.x and
            self.coin_haut_gauche.y < pos_pixels.y < self.coin_bas_droit.y
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
                x is not None and y is not None
            ):
                pos_pixels = versCoordonneNormaliser(Vec2(x, y))
                if (
                    self.coin_haut_gauche.x < pos_pixels.x < self.coin_bas_droit.x and
                    self.coin_haut_gauche.y < pos_pixels.y < self.coin_bas_droit.y
                ):
                    self.action_clique()

        




def afficher(object: place_holder.Object2d, tag: str = ""):
    """permet d'afficher un object2d

    Args:
        object (place_holder.Object2d): _description_
        tag (str): Tag pour l'objet
    """
    logging.info(f"graphisme : Affichage de l'objet à la position {object.pos} avec la texture '{object.texture}' et la taille {object.taille}")
    pos_pixels = vers_pixels(object.pos)
    taille_pixels = vers_pixels(object.taille)
    texture = _normaliser_chemin(object.texture)
    if texture is None:
        return
    fltk.image(
        round(pos_pixels.x),
        round(pos_pixels.y),
        texture,
        round(taille_pixels.x),
        round(taille_pixels.y),
        tag=tag,
    )



def get_pos_souris() -> Vec2:
    """obtient les coordoné de la souris exprimé entre 0 et 1

    Returns:
        Vec2: _description_
    """
    x, y = fltk.abscisse_souris(), fltk.ordonnee_souris()
    if x is None or y is None:
        return Vec2(0, 0)
    return versCoordonneNormaliser(Vec2(x, y))

def get_clic_gauche(ev:evenement) -> Vec2:
    """obtient la position du clic gauche de la souris en coordonnées .


    Returns:
        Optional[Vec2]: _description_
    """
    return Vec2(fltk.abscisse(ev.data), fltk.ordonnee(ev.data)) # type: ignore

class Grille:
    def __init__(self, taille_tuile: int, tag: str):
        self.taille_tuile = taille_tuile
        self.tuiles:dict[tuple[int, int], place_holder.Tuile] = {}  # {(x, y): tuile}
        self.tag = tag

    def ajouter_tuile(
        self,
        pos: Vec2 = vect.Vec2(),
        tuile=None,
        texture: str | None = None,
        property: dict  = {},
    ):
        
        """



        Raises:
            ValueError: _description_
        """

        pos_snappée = palier(pos, self.taille_tuile)

        if tuile is not None:
            self.tuiles[(tuile.pos.x, tuile.pos.y)] = tuile
        elif texture is not None:
            tuile = place_holder.Tuile(pos, texture, self.taille_tuile)
            tuile.property.update(property)
            self.tuiles[(pos_snappée.x, pos_snappée.y)] = tuile # pyright: ignore[reportArgumentType]
        else:
            raise ValueError("Soit une tuile, soit une texture doit être fournie.")
    
    def get_tuile(self, pos: Vec2) -> place_holder.Tuile:
        pos_snappée = palier(pos, self.taille_tuile)
        air =  place_holder.Tuile(pos=pos,texture="",taille=self.taille_tuile,tag ="air")
        return self.tuiles.get((pos_snappée.x, pos_snappée.y), air) # pyright: ignore[reportArgumentType, reportCallIssue]
    


    def supprimer_tuile(self, pos: Vec2):
        pos_snappée = palier(pos, self.taille_tuile)
        key = (pos_snappée.x, pos_snappée.y)
        t = self.get_tuile(pos_snappée)
        if key in self.tuiles:
            
            del self.tuiles[key] # pyright: ignore[reportArgumentType]



    def afficher(self):
        for tuile in self.tuiles.values():
            afficher(tuile)
    def desaficher(self):
        for tuile in self.tuiles.values():
            fltk.efface(tuile.id)
            tuile.id = None       
           

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
    """obtien juste les  evenement

    Returns:
        _type_: _description_
    """
    res:evenement = evenement(type=None, data=None)
    res.data = fltk.donne_ev()
    res.type = fltk.type_ev(res.data)
    return res

logging.basicConfig(
level=logging.INFO, 
format='%(asctime)s - %(levelname)s - %(message)s',
filename='graphisme.log',  
filemode='w'         
)

        

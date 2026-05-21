from dataclasses import dataclass
from hmac import new
import itertools
from turtle import pos, update
from typing import Any, Generator, Optional, Tuple

from numpy import angle
import graphisme
import monde 
import place_holder
import heapq
import physique
import vect
from graphisme import verscoordonnefenetre,versCoordonneNormaliser

from math import cos,sin,radians


class noeud():
    """
    class utiliré pour l'algo de recherche A*
        coord: la position du noeud
        parent: le noeud parent de ce noeud
        g: le cout pour arriver a ce noeud addition depuis le premier noeud
        h: l'estimation du cout pour arriver a l'objectif a partir de ce noeud
        f: g+h
    """
    def __init__(self,_coord:vect.Vec2,_parent:noeud | None,_g:float=float('inf'),_h:float=0) -> None:
        
        self.coord:vect.Vec2 = _coord
        self.parent:noeud | None = _parent
        self.g:float = _g
        self.h:float = _h
    @property
    def f(self)->float:
        return self.g+self.h
            







    

def recherche_stupide(nv:monde.niveau)->list:
    j1:monde.joueur = monde.joueur(nv.debut)
    res:list[vect.Vec2] = []
    


    while  vect.norme(nv.point_fin -j1.position) > 1e-5:
        direction = nv.point_fin - j1.position
        j1.vitesse = direction if vect.norme(direction )< 15 else  vect.normalize(direction)*15
        physique.update_physique(nv, 0.1, j1)
        res.append(j1.position)


    return  res






    
    
    


def simuler_saut(joueur:monde.joueur,direction,nv:monde.niveau,pas =0.69,max_saut:float = 15.0):
    """simule un saut

    Args:
        joueur (_type_): le faut joueur
        direction (_type_): direction qui sera donné
        nv (monde.niveau): le monde ou il evolue
        pas (float, optional):pas de la simulation. Defaults to 0.1.

    Returns:
        _type_: _description_
    """


    joueur.vitesse = direction if vect.norme(direction )< max_saut else  vect.normalize(direction)*max_saut

    while vect.norme(joueur.vitesse ) > 1e-5:
        physique.update_physique(nv, pas, joueur)


def get_valide_neigbooor(nv:monde.niveau,n:noeud,pas:float,max_saut:float = 15.0) -> Generator[noeud, Any, None]:
    """
    comme c'est lourd on va fair que ce soit un lazy generator
    creer tout les voisin de la position actuel

    Args:
        nv (monde.niveau): le niveau ou il evolue
        n (noeud): le noeud pour lequel on cherche les voisins

    Returns:
        Generator[noeud, Any, None]: un générateur de noeuds voisins valides
    """

    
    

    for i in range(0,360,15):
            angle = radians(i)
            cos_a = cos(angle)
            sin_a = sin(angle)
            for k in range(0,int(max_saut)+1):
                joueur = monde.joueur(n.coord)
                direction = vect.Vec2(cos_a,sin_a)*k
                joueur.vitesse = direction 
                
                estimation = n.coord+direction
                if estimation.x > 1 or estimation.x < 0 or estimation.y > 1 or estimation.y < 0:
                    continue
                simuler_saut(joueur,direction*pas,nv,pas,max_saut)
                if not (0 <= joueur.position.x <= 1 and 0 <= joueur.position.y <= 1):#on sait jamais si y a un bug dans la physique et que l'ia est la seule a pour voir acceder
                    continue
                h = vect.norme(nv.point_fin - joueur.position)
                g = vect.norme(joueur.position - n.coord)
                yield noeud(joueur.position,
                            n,
                            n.g+g,
                            h
                            )



def reconstruire_chemin(noeud_final:noeud)->list:
    """reconstruit le chemin a partir du noeud final

    Args:
        noeud_final (noeud): le noeud final

    Returns:
        list: la suite d'action a faire
    """
    chemin: list[vect.Vec2] = []

    noeud_actuel:noeud = noeud_final
    while noeud_actuel.parent is not None:
        chemin.append(noeud_actuel.coord)
        noeud_actuel = noeud_actuel.parent
    chemin.reverse()
    return chemin



def  algoA(nv:monde.niveau,obj)->Optional[list]:

    """
    implementation de algo Recherche A 

    Args:
        nc (list): le niveau qu'il doit resoudre 
        obj: les coordoné de l'obectif qu'il doit atteindre

    Returns:
        list: la suite action a faire
    """

  
    noeud_depart = noeud(
        _coord=(nv.debut),
        _parent=None,
        _h=vect.norme(nv.point_fin - nv.debut)
    )


    open_list: list[tuple[float, vect.Vec2]] = [(noeud_depart.f, noeud_depart.coord)]  
    open_dict:dict[vect.Vec2,noeud] = {noeud_depart.coord: noeud_depart}         
    closed_set:set[vect.Vec2] = set()     

    




    while open_list:
        pos_actuelle = heapq.heappop(open_list)[1]
        noeud_actuel = open_dict.get(pos_actuelle)

        if noeud_actuel == None:
            continue
   
        closed_set.add(pos_actuelle)
        if pos_actuelle == nv.point_fin:
            return reconstruire_chemin(noeud_actuel)
            
        voisin = get_valide_neigbooor(nv,noeud_actuel,0.70)
        for n in voisin:
            if n.coord in closed_set:
                continue
            if n.coord not in open_dict or n.g < open_dict[n.coord].g:
                open_dict[n.coord] = n
                heapq.heappush(open_list, (n.f, n.coord))
          

                
    return None
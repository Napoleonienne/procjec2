import itertools
from turtle import update
from typing import Any, Generator, Tuple

from numpy import angle
import graphisme
import monde 
import place_holder
import physique
import vect
from graphisme import verscoordonnefenetre,versCoordonneNormaliser

from math import cos,sin,radians


class noeud():
    def __init__(self,coord:vect.Vec2,f,g,parent=None):
        self.coord:vect.Vec2 = coord
        self.parent:noeud | None = parent
        self.cout_depart_actuel = f
        self.cout_estime_actuelle_fin = g





    

def recherche_stupide(nv:monde.niveau)->list:
    j1:monde.joueur = monde.joueur(nv.debut)
    res:list[vect.Vec2]
    


    while  vect.norme(nv.point_fin -j1.position) < 2:
        if j1.direction == vect.Vec2() and  j1.vitesse == vect.Vec2():


  
    




    return 






    
    
    


def simuler_saut(joueur,direction,nv:monde.niveau,pas =0.1,max_saut:float = 15.0):
    """simule un saut

    Args:
        joueur (_type_): le faut joueur
        direction (_type_): direction qui sera donné
        nv (monde.niveau): le monde ou il evolue
        pas (float, optional):pas de la simulation. Defaults to 0.1.

    Returns:
        _type_: _description_
    """


    joueur.vistesse = direction if vect.norme(direction )< max_saut else  vect.normalize(direction)*max_saut

    while joueur.vistesse != vect.Vec2(0,0):
        physique.update_physique(nv, pas, joueur)


def get_valide_neigbooor(nv:monde.niveau,pos,pas:float,max_saut:float = 15.0) -> Generator[noeud, Any, None]:
    """
    comme c'est lourd on va fair que ce soit un lazy generator
    creer tout les voisin de la position actuel

    Args:
        nv (monde.niveau): le niveau ou il evolue
        joueur (monde.joueur): la position actuel du joueur

    Returns:
    noeud: noeud de position voisin valide
    """
    joueur:monde.joueur = monde.joueur(pos)

    
    

    for i in range(0,360,5):
            angle = radians(i)
            cos_a = cos(angle)
            sin_a = sin(angle)
            for k in range(0,int(max_saut)+1):
                joueur.position = pos
                direction = vect.Vec2(cos_a,sin_a)*k
                joueur.vitesse = direction 
                
                if direction.x >graphisme.FENETRE_HAUTEUR or direction.x < 0 or direction.y > graphisme.FENETRE_LARGEUR or direction.y < 0:
                    continue
                simuler_saut(joueur,direction*pas,nv,pas,max_saut)
                yield noeud((joueur.position),0,vect.norme(nv.point_fin - joueur.position))



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
    return chemin



def  algoA(nv:monde.niveau,obj)->list:

    """
    implementation de algo Recherche A 

    Args:
        nc (list): le niveau qu'il doit resoudre 
        obj: les coordoné de l'obectif qu'il doit atteindre

    Returns:
        list: la suite action a faire
    """
    joueur:monde.joueur = monde.joueur(nv.debut)
    solution:list[vect.Vec2] = []
  
    noeud_depart = noeud(
        (nv.debut),
          0, 
          vect.norme(nv.point_fin - nv.debut))
    noeud_fin = noeud(
        (nv.point_fin), 
            0,
            0
                        )

    while joueur.position != nv.point_fin:




        



  
    return solution
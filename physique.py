from doctest import debug_script
import logging
from turtle import pos
import graphisme
from place_holder import Sprite, Tuile,Object2d
import place_holder
import vect
import monde





GRAVITE = None



def set_gravite(g:vect.Vec2,monde:monde.niveau):
    monde.gravite = g





def colision(obj1: Object2d,obj2:Object2d)->bool:
    """
    permet de tester les colision entre 2 object


    Args:
        obj1 (Object2d): le premier object
        obj2 (Object2d): le deuxieme object

    Returns:
        bool: si sa touche ou pas
    """

    

    obj1_hg: vect.Vec2 = obj1.coin_haut_gauche
    obj1_bd: vect.Vec2 = obj1.coin_bas_droit

    obj2_hg: vect.Vec2 = obj2.coin_haut_gauche
    obj2_bd: vect.Vec2 = obj2.coin_bas_droit

    



    return( obj2_bd.x >= obj1_hg.x and
            obj2_hg.x <= obj1_bd.x and
            obj2_bd.y >= obj1_hg.y and
            obj2_hg.y <= obj1_bd.y
         
    )



def ressoudre_colision(obj1: monde.joueur,obj2:Object2d):
    """
    permet de ressoudre les colision entre 2 object
    pour le moment sa ne gère que les colision entre le joueur et les tuiles du terrain


    Args:
        obj1 (monde.joueur): le joueur
        obj2 (Object2d): la tuile du terrain

    Returns:
        bool: si sa touche ou pas
    """


    obj1_hg: vect.Vec2 = obj1.coin_haut_gauche
    obj1_bd: vect.Vec2 = obj1.coin_bas_droit

    obj2_hg: vect.Vec2 = obj2.coin_haut_gauche
    obj2_bd: vect.Vec2 = obj2.coin_bas_droit

    penetration:dict[str, float] = {
        "gauche": obj1_bd.x - obj2_hg.x,
        "droite": obj2_bd.x - obj1_hg.x,
        "haut": obj1_bd.y - obj2_hg.y,
        "bas": obj2_bd.y - obj1_hg.y
    }

    min_penetration_cote:str = min(penetration, key=lambda cote: penetration[cote])


    match min_penetration_cote:
        case "gauche":
            obj1.position.x = obj2_hg.x - obj1.sprite.taille.x / 2
            obj1.vitesse.x = 0
        case "droite":
            obj1.position.x = obj2_bd.x + obj1.sprite.taille.x / 2
            obj1.vitesse.x = 0
        case "haut":
            obj1.position.y = obj2_hg.y - obj1.sprite.taille.y / 2
            obj1.vitesse.y = 0
            obj1.direction.y = 0
        case "bas":
            obj1.position.y = obj2_bd.y + obj1.sprite.taille.y / 2
            obj1.vitesse.y = 0
            obj1.direction.y = 0

        
        
    






def applique_effet(joueur:monde.joueur,tuile:place_holder.Tuile,nv:monde.niveau):
    """
    applique les effets au joueur

    Args:
        joueur (monde.joueur): le joueur
        dt (float): le temps écoulé depuis le dernier update
    """

    


    if tuile.property.get("rebondissante", False):
        joueur.vitesse.y = -abs(joueur.vitesse.y) * 0.8
    if tuile.property.get("glissante", False):
        joueur.vitesse.x *= 0.95
    if tuile.property.get("amortissante", False):
        joueur.vitesse *= 0.9
    if tuile.property.get("mortelle", False):
        joueur.position = nv.debut
        joueur.vitesse = vect.Vec2(0, 0)
        joueur.direction = vect.Vec2(0, 0)
    if tuile.tag =='air':
        joueur.vitesse *= 0.8


   


def update_physique(monde:monde.niveau,dt:float,joueur:monde.joueur):
    """
    va update la physique a chaque frame, en appliquant la gravité et en gérant les colision entre le joueur et les tuiles du terrain

    Args:
        monde (monde.niveau): le niveau actuel du jeu
        dt (float): le temps écoulé depuis le dernier update
        joueur (monde.joueur): le joueur
    """
    joueur.position +=  monde.gravite* dt

    joueur.position += joueur.vitesse * dt


    for  tuile in monde.terrain:
        if colision(joueur, tuile) :
            if tuile.property.get("solide", False) :
                ressoudre_colision(joueur, tuile)
                applique_effet(joueur, tuile, monde)
    for tuile in monde.devant:
        if colision(joueur, tuile):
            if tuile.property.get("solide", False):
                ressoudre_colision(joueur, tuile)
            applique_effet(joueur, tuile, monde)
    

    joueur.vitesse -= joueur.vitesse * dt
    
        






    return








                                                                                                                                    
import logging
import graphisme
from place_holder import Sprite, Tuile,Object2d
import vect
import monde



def colision(obj1: Object2d,obj2:Object2d)->bool:
    """
    permet de tester les colision entre 2 object


    Args:
        obj1 (Object2d): le premier object
        obj2 (Object2d): le deuxieme object

    Returns:
        bool: si sa touche ou pas
    """

    

    obj1_hg = obj1.coin_haut_gauche
    obj1_bd = obj1.coin_bas_droit

    obj2_hg = obj2.coin_haut_gauche
    obj2_bd = obj2.coin_bas_droit





    return( obj2_bd.x > obj1_hg.x and
            obj2_hg.x < obj1_bd.x and
            obj2_bd.y > obj1_hg.y and
            obj2_hg.y < obj1_bd.y
         
    )







def amorti(joueur: monde.joueur, tuile: Tuile) :
    """
    regle les colision si amortie

    Args:
        joueur (monde.joueur): _description_
        tuile (Tuile): _description_
    """
    


def terrain_glissant():
     

    return

def appliquer_physique(joueur: monde.joueur, dt: float,monde:monde.niveau):
    """apllique la physique du aux jour

    Args:
        joueur (monde.joueur): _description_
        dt (float): _description_
        monde (monde.niveau): niveau actuel
    """
    

    logging.info(f"applique la physique par rapport aux taux")

    if joueur.vitesse != 0:
    g_a = monde.avant
    terain = monde.terrain
    g_d= monde.devant
    l_spr =monde.plan_object


    g_a.get_tuile(joueur.position)
    terain.get_tuile(joueur.position)
    g_d.get_tuile(joueur.position)

    

    for sprite in l_spr:
        if colision(joueur, sprite):
            pass
       
                
    return vect.Vec2


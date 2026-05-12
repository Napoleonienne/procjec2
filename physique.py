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







def appliquer_gravite(joueur: monde.joueur, dt: float,monde:monde.niveau):
    """applique la gravité au joueur

    Args:
        joueur (monde.joueur): le joueur a qui appliquer la gravité
        dt (float): le temps écoulé depuis la dernière mise à jour
        monde (monde.niveau): le niveau actuel pour vérifier les collisions avec le terrain
    """
    g = monde.gravite
    joueur.vitesse -= g * dt 
    


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
    


    t =g_a.get_tuile(joueur.position)
    y=terain.get_tuile(joueur.position)
    j =g_d.get_tuile(joueur.position)




    if colision(joueur,t):
        logging.info("le joueur touche une tuile")
        





    if colision(joueur,y):
        logging.info("le joueur touche une tuile de terrain")
        if y.property.get("glissant", False):
            terrain_glissant()
        if y.property.get("rebondissante", False):
            joueur.vitesse.y = -joueur.vitesse.y * 0.8  # Exemple de rebond
        if y.property.get("amortissante", False):
            joueur.vitesse.y = 0  # Arrête le mouvement vertical
        if y.property.get("mortelle", False):
            logging.info("le joueur est mort")
            # Gérer la mort du joueur (réinitialiser le niveau, etc.)
        



    if colision(joueur,j):
        logging.info("le joueur touche une tuile de devant")



    if t.tag == "air" and y.tag == "air" and j.tag == "air":
        appliquer_gravite(joueur, dt,monde)

        

    

    

    for sprite in l_spr:
        if colision(joueur, sprite):
            pass

       
                
    return vect.Vec2


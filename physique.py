import logging

from place_holder import Tuile
import vect
import monde

def collision(obj:Tuile, joueur: monde.joueur) -> bool:
    """Vérifie si cette tuile entre en collision avec le joueur."""
    return (
        (obj.coin_haut_gauche.x <= joueur.coin_bas_droit.x and obj.coin_bas_droit.x >= joueur.coin_haut_gauche.x) and
        (obj.coin_haut_gauche.y <= joueur.coin_bas_droit.y and obj.coin_bas_droit.y >= joueur.coin_haut_gauche.y) 
    )



def amorti(joueur: monde.joueur, tuile: Tuile) :
        if joueur.direction.y > 0:  # En train de tomber
            joueur.position.y = tuile.coin_haut_gauche.y - joueur.sprite.taille.y / 2
            joueur.vitesse = 0
        elif joueur.direction.y < 0:  # En train de sauter
            joueur.position.y = tuile.coin_bas_droit.y + joueur.sprite.taille.y / 2
            joueur.vitesse = 0
        if joueur.direction.x > 0: 
            joueur.position.x = tuile.coin_haut_gauche.x - joueur.sprite.taille.x / 2
        elif joueur.direction.x < 0:   
            joueur.position.x = tuile.coin_bas_droit.x + joueur.sprite.taille.x / 2


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
    for tuile in monde.terrain:
            if collision(tuile, joueur):
                if tuile.property["amortissante"]:  
                    amorti(joueur, tuile)
                elif tuile.property["mortelle"]:
                    # Réinitialiser la position du joueur ou appliquer une pénalité
                    joueur.position = monde.debut # Exemple de réinitialisation
                    joueur.vitesse = 0
                    joueur.direction = vect.Vec2()
                elif tuile.property[""]:


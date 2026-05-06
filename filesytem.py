import logging
from operator import le
from os import path
from pathlib import Path
import json
from turtle import st
from typing import Optional
from vect import Vec2
from monde import niveau
from place_holder import Tuile, Sprite
import os
from graphisme import Grille


sauvegardes_dispo:dict[str ,Path] = {}


def peupler_sauvegardes():
    """
    a lancer aux lancement de l'aplication
    Peuple le dictionnaire des sauvegardes disponibles en scannant le dossier de sauvegarde.
    """
    global sauvegardes_dispo
    ch_sauvegarde= Path(resource_path('fichier jeux/save'))
    if not ch_sauvegarde.exists():
        logging.warning(f"Le dossier de sauvegarde '{ch_sauvegarde}' n'existe pas. Création du dossier.")
        ch_sauvegarde.mkdir(parents=True, exist_ok=True)


    for file in ch_sauvegarde.glob('*.json'):
        nom = file.stem
        sauvegardes_dispo[nom] = file

    
    logging.info(f"Sauvegardes disponibles : {list(sauvegardes_dispo.keys())}")


def resource_path(relative_path)->Optional[str]:
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
        logging.error(f"Le fichier niveay n'existe pas : {res}")
        return None
     
    
    return res

def charger_options():
    """Charge les options du jeu depuis un fichier JSON."""
    options_path = Path('options.json')
    try:
        logging.info(f"Chargement des options depuis '{options_path}'")
        assert options_path.exists()
        with open(options_path, 'r', encoding='utf-8') as f:
            options = json.load(f)
            logging.info("Options chargées avec succès.")
            return options
    except (AssertionError, json.JSONDecodeError):
        logging.error(f"Erreur lors du chargement des options depuis '{options_path}'")
        raise Exception(f"Erreur lors du chargement des options depuis '{options_path}'")
    return {}


def sauvegarder_niveau(level: niveau, name: str):
    """Sauvegarde le niveau dans un fichier JSON."""
    logging.info(f"Sauvegarde du niveau '{name}'")
    global sauvegardes_dispo
    sauvegardes_dispo[name] = Path(resource_path(f"fichier jeux/save/{name}.json"))


    level_serialiser = level.serialisation()

    ch_savegarde = resource_path('fichier jeux/save') + f"/{name}.json"
    ch_savegarde.parent.mkdir(parents=True, exist_ok=True)
    with open(ch_savegarde, 'w', encoding='utf-8') as f:
        json.dump(level_serialiser, f)




def charger_niveau(nom: str)-> niveau:
    """
    permet de charger le niveau a partir d'un fichier .json et de le convertir en un objet niveau

    Args:
        nom (str): nom du niveau a charger
    """
    ch_savegarde = sauvegardes_dispo[nom]
    logging.info(f"Chargement du niveau '{nom}'")
    with open(ch_savegarde, 'r') as f:
        donne_niveau = json.load(f)
    
    debut = Vec2(donne_niveau["debut"]["x"], donne_niveau["debut"]["y"])
    fin = Vec2(donne_niveau["point_fin"]["x"], donne_niveau["point_fin"]["y"])
    niveau_charger = niveau(debut, fin)
    niveau_charger.fond = donne_niveau["fond"]
    niveau_charger.avant = Grille(32)
    niveau_charger.decor = Grille(16)
    niveau_charger.terrain = Grille(16)
    niveau_charger.objet = Grille(8)  

    peupler_niveau(donne_niveau, niveau_charger, "avant")
    peupler_niveau(donne_niveau, niveau_charger, "decor")
    peupler_niveau(donne_niveau, niveau_charger, "terrain")
    peupler_niveau(donne_niveau, niveau_charger, "objet")



    for sprite_data in donne_niveau["devant"]:
        pos = Vec2(sprite_data["pos"]["x"], sprite_data["pos"]["y"])
        taille = Vec2(sprite_data["taille"]["x"], sprite_data["taille"]["y"])
        texture = sprite_data["texture"]
        sprite = Sprite(pos, texture, taille)
        niveau_charger.devant.append(sprite)


    return niveau_charger

def peupler_niveau(donne_niveau: dict, niveau_charger: niveau, tranche: str):
    """_summary_

    Args:
        donne_niveau (dict): les donné du niveau charger a partir du json
        niveau_charger (niveau): objecty qui reçoit
        tranche (str): la tranche a peupler (avant, decor, terrain ou objet)
    """
    logging.debug(f"Peuplement de la tranche '{tranche}' du niveau chargé")


    for tuile_data in donne_niveau[tranche].values():

        pos = Vec2(tuile_data["pos"]["x"], tuile_data["pos"]["y"])
        taille = tuile_data["taille"]
        texture = tuile_data["texture"]
        tuile = Tuile(pos, texture, taille)
        niveau_charger.avant.ajouter_tuile(pos,tuile)


def supprimer_niveau(nom: str):
    if sauvegardes_dispo.get(nom,False) or not sauvegardes_dispo[nom].exists() :
        return
    logging.info(f"Suppression du niveau '{nom}'")
    sauvegardes_dispo[nom].unlink()
    del sauvegardes_dispo[nom]
    



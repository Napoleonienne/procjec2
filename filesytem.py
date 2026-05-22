import logging
from pathlib import Path
import json

from numpy import isin
from vect import Vec2
from monde import niveau
from place_holder import Tuile, Sprite
import graphisme
from graphisme import Grille


sauvegardes_dispo: dict[str, Path] = {}


def dossier_sauvegarde() -> Path:
    base_path = Path.home() / ".saute_mouton"
    chemin = base_path / "save"
    chemin.mkdir(parents=True, exist_ok=True)
    return chemin


def peupler_sauvegardes():
    """
    a lancer aux lancement de l'aplication
    Peuple le dictionnaire des sauvegardes disponibles en scannant le dossier de sauvegarde.
    """
    global sauvegardes_dispo
    ch_sauvegarde = dossier_sauvegarde()
    for file in ch_sauvegarde.glob("*.json"):
        nom = file.stem
        sauvegardes_dispo[nom] = file

    
    logging.info(f"Sauvegardes disponibles : {list(sauvegardes_dispo.keys())}")


def charger_options():
    """charge les option
    et gere erreur si le fichier option n'est pas present

    Raises:
        ValueError: si le fichier existe
        ValueError: _description_
        Exception: _description_

    Returns:
        _type_: dictionnaire des option
    """
    options_path = Path(graphisme.chemin_absolue("fichier_jeux/option jeux/option.json"))
    try:
        logging.info(f"Chargement des options depuis '{options_path}'")
        assert options_path.exists()
        with open(options_path, 'r', encoding='utf-8') as f:
            options = json.load(f)
            fenetre = options.get("fenetre")
            if not isinstance(fenetre, dict):
                logging.error("la section 'fenetre' doit être un dictionnaire dans les options.")
            largeur = fenetre.get("largeur") 
            hauteur = fenetre.get("hauteur") 

            # Valide et normalise les dimensions de la fenêtre
            if isinstance(largeur, int):
                pass
            elif isinstance(largeur, str) and largeur.isdigit() or isinstance(largeur, float):
                largeur = int(largeur)
            else:
                largeur = graphisme.FENETRE_LARGEUR

            if isinstance(hauteur, int):
                pass
            elif isinstance(hauteur, str) and hauteur.isdigit() or isinstance(hauteur, float):
                hauteur = int(hauteur)
            else:
                hauteur = graphisme.FENETRE_HAUTEUR

            logging.info("Options chargées avec succès.")
            return options
    except (AssertionError) as e:
        logging.error(f"Erreur lors du chargement des options depuis '{options_path}' :{e}   ")
        raise Exception(f"Erreur lors du chargement des options depuis '{options_path}'")
    return {}


def sauvegarder_niveau(level: niveau, name: str):
    """Sauvegarde le niveau dans un fichier JSON."""
    logging.info(f"Sauvegarde du niveau '{name}'")
    global sauvegardes_dispo
    ch_sauvegarde = dossier_sauvegarde() / f"{name}.json"
    sauvegardes_dispo[name] = ch_sauvegarde


    level_serialiser = level.serialisation()

    ch_sauvegarde.parent.mkdir(parents=True, exist_ok=True)

    with open(ch_sauvegarde, "w", encoding="utf-8") as f:
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
    niveau_charger.avant = Grille(32,tag='avant')
    niveau_charger.decor = Grille(16,tag='decor')
    niveau_charger.terrain = Grille(16,tag='terrain')
    niveau_charger.devant = Grille(8,tag='devant')
    niveau_charger.name = donne_niveau["nom"]


    peupler_niveau(donne_niveau, niveau_charger, "avant")
    peupler_niveau(donne_niveau, niveau_charger, "decor")
    peupler_niveau(donne_niveau, niveau_charger, "terrain")
    peupler_niveau(donne_niveau, niveau_charger, "objet")



    for sprite_data in donne_niveau["devant"]:
        pos = Vec2(sprite_data["pos"]["x"], sprite_data["pos"]["y"])
        taille = Vec2(sprite_data["taille"]["x"], sprite_data["taille"]["y"])
        texture = sprite_data["texture"]
        sprite = Sprite(pos, texture, taille)
        niveau_charger.plan_object.append(sprite)


    return niveau_charger

def peupler_niveau(donne_niveau: dict, niveau_charger: niveau, tranche: str):
    """_summary_

    Args:
        donne_niveau (dict): les donné du niveau charger a partir du json
        niveau_charger (niveau): objecty qui reçoit
        tranche (str): la tranche a peupler (avant, decor, terrain ou objet)
    """
    logging.debug(f"Peuplement de la tranche '{tranche}' du niveau chargé")


    grille = getattr(niveau_charger, tranche)
    for tuile_data in donne_niveau[tranche].values():

        pos = Vec2(tuile_data["pos"]["x"], tuile_data["pos"]["y"])
        taille = tuile_data["taille"]
        if isinstance(taille, dict):
            if taille["x"] != taille["y"]:
                raise ValueError(
                    f"Les tuiles doivent être carrées dans la tranche '{tranche}' pour la position {pos}"
                )
            taille = taille["x"]
        texture = tuile_data["texture"]
        tuile = Tuile(pos, texture, taille)
        tuile.property.update(tuile_data.get("property", {}))
        grille.ajouter_tuile(pos, tuile)


def supprimer_niveau(nom: str):
    if nom not in sauvegardes_dispo or not sauvegardes_dispo[nom].exists():
        return
    logging.info(f"Suppression du niveau '{nom}'")
    sauvegardes_dispo[nom].unlink()
    del sauvegardes_dispo[nom]
    

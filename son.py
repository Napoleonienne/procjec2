

from itertools import cycle
import logging

from nava import play, stop

from graphisme import chemin_absolue






def lancer_son(ch: str,loop: bool = False):
    logging.info(f"lancement du son {ch} avec loop={loop}")
    ch = chemin_absolue(ch)
    play(ch, async_mode=True, loop=loop)

def son_menu():
    id = lancer_son("fichier_jeux/son/sons.waw/musique menu.wav", loop=True)
    return id

def son_saut():
    id = lancer_son("fichier_jeux/son/saut.mp3")
    return id
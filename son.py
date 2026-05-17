

from itertools import cycle

from nava import play, stop

from graphisme import chemin_absolue






def lancer_son(ch: str,loop: bool = False):
    ch = chemin_absolue(ch)
    play(ch, async_mode=True, loop=loop)

def son_menu():
    id = lancer_son("fichier_jeux/son/sons.waw/musique menu.wav", loop=True)
    return id

def son_saut():
    id = lancer_son("fichier_jeux/son/saut.mp3")
    return id
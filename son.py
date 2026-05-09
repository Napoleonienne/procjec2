

import nava
import graphisme


def lancer_son(ch: str):
    ch = graphisme.chemin_absolue(ch)

    nava.play(ch,async_mode=True)

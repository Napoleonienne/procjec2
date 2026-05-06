

import nava
from filesytem import resource_path


def lancer_son(ch:str)
    ch = resource_path(ch)

    nava.play(ch,async_mode=True)
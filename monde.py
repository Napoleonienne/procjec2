from pathlib import Path
from vect import vec2
class joueur:
    def __init__(self,pos):
        self.position =pos
        self.vistesse =0.0
        self.poid=12

    


def charger_asset():



    return

class niveau:
    """
    sera la classe qi me permetera de creer des niveau
    
    """
    def __init__(self):
        self.layout:list[object] = []
        self.decor:list[object] = []


class object:
    """
    object va juste etre la classe ou sera derivé les autre element su jeux c'est
    donc on va faire de heritage
    je vais probablement pas utiliser les forme comme les rectangle ou autre integrer a fltk on va faire plus complexe · 
    """
    def __init__(self):
        self.hitbox:list[list] =[ [],]
        self.textture = ""
        self.pos =vec2


        

class amorti(object):
    def __init__(self):
        super().__init__()


class colle(object):
    def __init__(self):
        super().__init__()

class amorti(object):
    def __init__(self):
        super().__init__()

class amorti(object):
    def __init__(self):
        super().__init__()
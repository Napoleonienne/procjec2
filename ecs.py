from dataclasses import dataclass
import itertools
class scene:
    def __init__(self):
        self.entité_contenus:list[entity]

    def create_entity(self):
        self.entité_contenus.append(entity())


itertools.accumulate(range(10),
                    lambda total, x: total + x / 2.0,
                    initial=0.0)
class system:
    def __init__(self):


        pass
class monde:
    pass


class entity:
    compteur:int =0
    def __init__(self):
        self.ID = self.compteur
        self.compteur =+ 1

class compnent():
    def __init__(self) -> None:
        pass




from dataclasses import dataclass
class scene:
    def __init__(self):
        self.entité_contenus:list[entity]

    def create_entity(self):
        self.entité_contenus.append(entity())



class system:
    def __init__(self):


        pass



class entity:
    compteur:int =0
    def __init__(self):
        self.ID = self.compteur
        self.compteur =+ 1

class compnent():
    def __init__(self) -> None:
        pass
        

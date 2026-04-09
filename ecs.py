import abc
from ast import Import
from dataclasses import dataclass
from abc import ABC, abstractmethod
from logging import error


component = dataclass
class scene:
    def __init__(self):
        self.sys:system  = system()
        self.entité_contenus:dict ={}

    def create_entity(self,name):
        self.entité_contenus[name] = entity

    


class System(ABC):
    """
    la classe qui permett de definir les autres syteme
    """
    @abstractmethod
    def start(self) -> None:
        """Prépare le système avant la boucle principale."""
        error("pas implementer")
        

    @abstractmethod
    def update(self) -> None:
        """Exécute la logique principale du système."""
        error("pas implementer")

    @abstractmethod
    def stop(self) -> None:
        """Nettoie les ressources du système."""
        error("pas implementer")





class entity:
    compteur:int =0
    def __init__(self):
        self.ID = entity.compteur
        entity.compteur += 1
        self.component:set = {}

    def add_component(self,data):
        self.component.add(data)
        


    
    







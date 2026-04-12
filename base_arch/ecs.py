from calendar import c
from dataclasses import dataclass
from abc import ABC, abstractmethod
from logging import error
import struct
from typing import overload

from numpy import iterable


struct = dataclass



class System(ABC):
    """
    la classe qui permett de definir les autres systèmes,
    et doitre etre hériter
    """
    def __init__(self,comp_req:set) -> None:
        super().__init__()
        self.comp_req:set = comp_req

    @abstractmethod
    def proces(self, entity: entity) -> None:
        """Exécute la logique principale du système."""
        error("pas implementer")



class component_manzger(ABC):
    """
    la classe qui permet de definir les autres composant,
    et doitre etre hériter
    """
    def __init__(self) -> None:
        super().__init__()
        self.component = dict[int,object] # un dictionnaire qui associe le type du component a son instance
    
    def add_component(self,comp_type:object)->None:
        """
        ajoute le component a la liste des component

        Args:
            comp_type (object): le component a ajouter
        """
        if comp_type in self.component:
            error(f"le component {comp_type.__name__} existe déjà")
        self.component[comp_type] = comp_type()





class entity2:
    def __init__(self):
        self.ID:int = 0
    




class entity:
    """
    l'entité est la classe qui definit out object du monde et contient les composant associé a l'instance de l'entité

    dans un langage de bas niveau je ferais pas comme sa 
    """
    compteur:int =0
    def __init__(self):
        self.ID:int = entity.compteur
        entity.compteur += 1
        self.component:set[object]

    def add_component(self,comp_type)->None:
        """
        ajpuit le component a l'entité si il n"y est pas déjà

        Args:
            comp_type (_type_): le component a ajouter

        """
        if self.has_component(comp_type):

            error(f"l'entité {self.ID} a déjà le component {comp_type.__name__}")
        self.component.add(comp_type)


    def get_component(self,comp_type)->object|None:
        """
            récupère le component de l'entité si il existe
        Args:
            comp_type (_type_): type du component a vérifier

        Returns:
            object|None: envoie le component si il existe sinon envoie None
        """
        for comp in self.component:
            if isinstance(comp,comp_type):
                return comp
        return None
    def remove_component(self,comp_type)->bool:
        """
        enleve l'instance du component de l'entité

        Args:
            comp_type (_type_): type du component a enlevé

        Returns:
            bool: _description_
        """
        select = None
        for comp in self.component:
            if isinstance(comp,comp_type):
                select = comp
                break
        self.component.remove(select)

    
    
    def has_component(self,comp_type:object|set|list)->bool:
        """
        verifie que le component existe

        Args:
            comp_type (_type_): type du component a vérifier ou ensemble de types

        Returns:
            bool: True si le component existe, False sinon
        """
        if isinstance(comp_type, (set, list)):
            for ct in comp_type:
                if not self.has_component(ct):
                    return False
            return True
        else:
            for comp in self.component:
                if isinstance(comp, comp_type):
                    return True
            return False

    


    #pour le debuging
    def __str__(self):
        return f"entité {self.ID} avec les components: {[comp.__class__.__name__ for comp in self.component]}"
    def __repr__(self):
        return self.__str__()

        


    
    

class scene:
    def __init__(self):
        self.sys:set[System]
        self.entité_contenus:dict[str,entity] ={}

    def create_entity(self,name:str):
        self.entité_contenus[name] = entity()
        return self.entité_contenus[name]
    
    def all_entity(self):
        return self.entité_contenus.values()

    def add_system(self,sys:System):
        self.sys.add(sys)
    
    def update(self):
        for _,entite in self.entité_contenus.items():
            for sys in self.sys:
                if entite.has_component(sys.comp_req):
                    sys.proces(entite)
    

    





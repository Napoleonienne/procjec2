from calendar import c
from dataclasses import dataclass
from abc import ABC, abstractmethod
from logging import error
import logging
from typing import overload
from itertools import count as _count
from numpy import iterable
from typing import NamedTuple, Any,TypeVar 


"""_summary_
je me base sur esper https://github.com/benmoran56/esper pour faire mon propre syteme ecs 

entitty compoent sytme c'est juste un syteme est aux utiliser ineritence qui pose des probleme comme on n'arrive pas entierment enfermer 
tout les qui est liée a la classe ou ineritence circulaire ou encore
le fait de devoir tu veux un sorchier mais qui soit aussi un archer 

je l'ai  decourvet quand je crois avec opengl et essayer de regarder comment faire un moteur de jeux vue que c'est aussi l'un de mes procject 

"""

_C = TypeVar('_C')
_C2 = TypeVar('_C2')
_C3 = TypeVar('_C3')
_C4 = TypeVar('_C4')

componente = dataclass
_entity_count: _count[int] = _count(start=1)
class monde(NamedTuple):
    entity_count: _count[int]
    components: dict[type[Any], set[int]]
    entities: dict[int, dict[type[Any], Any]]
    dead_entities: set[int]
    comp_cache: dict[type[Any], list[Any]]
    comps_cache: dict[tuple[type[Any], ...], list[Any]]
    processors: list['Processor']
    processors_dict: dict[type['Processor'], 'Processor']
    cache_dirty: bool
    process_times: dict[str, int]
    event_registry: dict[str, Any]


nom_monde_actuel:str ="default"
monde_actuelle:monde = monde(_count(start=1),{},{},set(),
                             {},{},[],{},
                             False,{},{})
_context_map: dict[str, monde] ={nom_monde_actuel:monde_actuelle}


def liste_des_mondes() -> dict[str, monde]:
    global _context_map

    return _context_map

def supprimer_monde(name: str) -> None:
    """
    supprime le monde entier
   
    """
    global _context_map,nom_monde_actuel
    if nom_monde_actuel == name:
        logging.error("le monde active ne peut etre supprimer")
        return

    del _context_map[name]

def changer_de_monde(name:str)->None:
    global nom_monde_actuel, monde_actuelle,_context_map
    nom_monde_actuel = name

    if name not in _context_map:
        _context_map[name] =monde(_count(start=1),{},{},set(),
                             {},{},[],{},
                             False,{},{})
        monde_actuelle = _context_map[name]
        return
    
    monde_actuelle = _context_map[name]






def clear_database() -> None:
    """Clear the Entity Component database.

    Removes all Entities and Components from the current World.
    Processors are not removed.
    """
    global _entity_count
    _entity_count = _count(start=1)
    _components.clear()
    _entities.clear()
    _dead_entities.clear()
    _clear_cache_now()
################################################
#               processor
################################################
class Processor:
    """
    base pout tout les processors, doit être hérité et la méthode process doit être implémentée

        def process(self):
            for ent, (rend, vel) in esper.get_components(Renderable, Velocity):
                your_code_here()
    """

    priority = 0

    def process(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

def add_processor(processor_instance: Processor, priority: int = 0) -> None:
    processor_instance.priority = priority 
    monde_actuelle.processors.append(processor_instance)
    monde_actuelle.processors.sort(key=lambda proc: proc.priority, reverse=True)
    monde.processors_dict[type(processor_instance)] = processor_instance



    
    





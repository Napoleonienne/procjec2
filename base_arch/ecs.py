import __future__
from calendar import c
from dataclasses import dataclass
from abc import ABC, abstractmethod
from filecmp import clear_cache
from logging import error
import logging
from typing import overload
from itertools import count as _count
from typing import NamedTuple, Any,TypeVar 
import time as _time
from array import array as _array

"""_summary_
je me base sur esper https://github.com/benmoran56/esper pour faire mon propre syteme ecs 

entitty compoent sytme c'est juste un syteme est aux utiliser ineritence qui pose des probleme comme on n'arrive pas entierment enfermer 
tout les qui est liée a la classe ou ineritence circulaire ou encore
le fait de devoir tu veux un sorchier mais qui soit aussi un archer 

je l'ai  decourvet quand je crois avec opengl et essayer de regarder comment faire un moteur de jeux vue que c'est aussi l'un de mes procject 

"""
__future__.

j = _array('I')

_C = TypeVar('_C')
_C2 = TypeVar('_C2')
_C3 = TypeVar('_C3')
_C4 = TypeVar('_C4')

componente = dataclass
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





def _clear_cache_now() -> None:
    """
    """
    global monde_actuelle
    monde_actuelle.comp_cache.clear()
    monde_actuelle.comps_cache.clear()
    monde_actuelle = monde_actuelle._replace(cache_dirty=False)

def clear_database() -> None:
    """Clear the Entity Component database.
    enleve toutes les entiter et componante du monde
    
    """
    global _entity_count
    _entity_count = _count(start=1)
    monde_actuelle.components.clear(
    )
    monde_actuelle.entities.clear
    monde_actuelle.dead_entities.clear()
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
    monde_actuelle.processors_dict[type(processor_instance)] = processor_instance


def process(*args: Any, **kwargs: Any) -> None:
    """
    execute les processor dans l'odre de priorité préetabli, en passant les arguments à chaque processor

    """

    clear_dead_entities()
    for processor in monde_actuelle.processors:
        processor.process(*args, **kwargs)


def timed_process(*args: Any, **kwargs: Any) -> None:
    """Track Processor execution time for benchmarking.

    permet de suivre le temps d'execution de chaque processor pour faire du benchmarking
    """
    clear_dead_entities()
    for processor in monde_actuelle.processors:
        start_time = _time.process_time()
        processor.process(*args, **kwargs)
        monde_actuelle.process_times[processor.__class__.__name__] = int((_time.process_time() - start_time) * 1000)

################################################
#               entity
################################################

def create_entity(*components: _C) -> int:
    """Create a new Entity, with optional initial Components.

    This function returns an Entity ID, which is a plain integer.
    You can optionally pass one or more Component instances to be
    assigned to the Entity on creation. Components can be also be
    added later with the :py:func:`esper.add_component` function.
    """
    entity = next(_entity_count)
    entity_dict = {}

    for component_instance in components:
        component_type = type(component_instance)

        if component_type not in monde_actuelle.components:
            monde_actuelle.components[component_type] = set()

        monde_actuelle.components[component_type].add(entity)
        entity_dict[component_type] = component_instance

    monde_actuelle.entities[entity] = entity_dict
    clear_cache()

    return entity


def delete_entity(entity: int, immediate: bool = False) -> None:
    """Delete an Entity from the current World.

    Delete an Entity and all of it's assigned Component instances from
    the world. By default, Entity deletion is delayed until the next call
    to :py:func:`esper.process`. You can, however, request immediate
    deletion by passing the `immediate=True` parameter. Note that immediate
    deletion may cause issues, such as when done during Entity iteration
    (calls to esper.get_component/s).

    Raises a KeyError if the given entity does not exist in the database.
    """
    if immediate:
        entity_comps = monde_actuelle.entities[entity]
        for component_type in entity_comps:
            comp_set = monde_actuelle.components[component_type]
            comp_set.discard(entity)

            if not comp_set:
                del monde_actuelle.components[component_type]

        del monde_actuelle.entities[entity]
        clear_cache()
    else:
        monde_actuelle.dead_entities.add(entity) 
    
def clear_dead_entities() -> None:
    """Finalize deletion of any Entities that are marked as dead.

    This function is provided for those who are not making use of
    :py:func:`esper.add_processor` and :py:func:`esper.process`. If you are
    calling your processors manually, this function should be called in
    your main loop after calling all processors.
    """
    # In the interest of performance, this function duplicates code from the
    # `delete_entity` function. If that function is changed, those changes should
    # be duplicated here as well.
    if not monde_actuelle.dead_entities:
        return

    for entity in monde_actuelle.dead_entities:
        entity_comps = monde_actuelle.entities[entity]

        for component_type in entity_comps:
            comp_set = monde_actuelle.components[component_type]
            comp_set.discard(entity)

            if not comp_set:
                del monde_actuelle.components[component_type]

        del monde_actuelle.entities[entity]

    monde_actuelle.dead_entities.clear()
    clear_cache()





from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, Type, TypeVar

EntityId = int
T = TypeVar("T")
System = Callable[["World"], None]


class World:
    def __init__(self) -> None:
        self._next_entity = 1
        self._components: Dict[Type[Any], Dict[EntityId, Any]] = {}
        self.resources: Dict[str, Any] = {}

    def create_entity(self) -> EntityId:
        entity = self._next_entity
        self._next_entity += 1
        return entity

    def add_component(self, entity: EntityId, component: T) -> None:
        self._components.setdefault(type(component), {})[entity] = component

    def get_component(self, entity: EntityId, component_type: Type[T]) -> T | None:
        return self._components.get(component_type, {}).get(entity)

    def remove_component(self, entity: EntityId, component_type: Type[T]) -> None:
        self._components.get(component_type, {}).pop(entity, None)

    def query(self, *component_types: Type[Any]) -> Iterable[tuple[Any, ...]]:
        if not component_types:
            return []
        base = self._components.get(component_types[0], {})
        results = []
        for entity in base.keys():
            if all(entity in self._components.get(component, {}) for component in component_types[1:]):
                components = [self._components[component][entity] for component in component_types]
                results.append((entity, *components))
        return results


class Scheduler:
    def __init__(self) -> None:
        self._systems: list[System] = []

    def add_system(self, system: System) -> None:
        self._systems.append(system)

    def run(self, world: World) -> None:
        for system in self._systems:
            system(world)

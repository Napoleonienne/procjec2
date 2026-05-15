from __future__ import annotations

from dataclasses import dataclass
import logging
import multiprocessing
import queue
from typing import Optional

import filesytem
import graphisme
import monde
from menus import Menu
import vect

from ecs import Scheduler, World

vec2 = vect.Vec2
PHYSICS_ENABLED = False


@dataclass
class GameState:
    etat: str = "menu"
    jeu_pre: bool = True
    running: bool = True


@dataclass
class LevelComponent:
    level: monde.niveau


@dataclass
class PlayerComponent:
    player: monde.joueur


@dataclass
class PhysicsComponent:
    enabled: bool = False


def _physics_loop(input_queue: multiprocessing.Queue, output_queue: multiprocessing.Queue) -> None:
    while True:
        payload = input_queue.get()
        if payload is None:
            break
        dt = payload["dt"]
        pos_x, pos_y = payload["position"]
        vel_x, vel_y = payload["velocity"]
        grav_x, grav_y = payload["gravity"]
        vel_x -= grav_x * dt
        vel_y -= grav_y * dt
        pos_x += vel_x * dt
        pos_y += vel_y * dt
        output_queue.put({"position": (pos_x, pos_y), "velocity": (vel_x, vel_y)})


class PhysicsWorker:
    def __init__(self) -> None:
        ctx = multiprocessing.get_context("spawn")
        self._input: multiprocessing.Queue = ctx.Queue()
        self._output: multiprocessing.Queue = ctx.Queue()
        self._process = ctx.Process(
            target=_physics_loop,
            args=(self._input, self._output),
            daemon=True,
        )
        self._process.start()

    def step(self, payload: dict) -> None:
        self._input.put(payload)

    def poll(self) -> Optional[dict]:
        try:
            return self._output.get_nowait()
        except queue.Empty:
            return None

    def close(self) -> None:
        if self._process is None:
            return
        self._input.put(None)
        self._process.join(timeout=1)
        if self._process.is_alive():
            self._process.terminate()
            self._process.join(timeout=1)
        self._process = None


def _get_state(world: World) -> GameState:
    return world.resources["game_state"]


def _get_level_component(world: World) -> LevelComponent:
    entity = world.resources["level_entity"]
    component = world.get_component(entity, LevelComponent)
    if component is None:
        raise RuntimeError("Niveau manquant dans l'ECS")
    return component


def _get_player_component(world: World) -> PlayerComponent:
    entity = world.resources["player_entity"]
    component = world.get_component(entity, PlayerComponent)
    if component is None:
        raise RuntimeError("Joueur manquant dans l'ECS")
    return component


def _set_level(world: World, level: monde.niveau) -> None:
    level_component = _get_level_component(world)
    level_component.level = level


def _set_player(world: World, player: monde.joueur) -> None:
    player_component = _get_player_component(world)
    player_component.player = player


def _sync_player_sprite(player: monde.joueur) -> None:
    if hasattr(player, "sprite") and player.sprite:
        player.sprite.pos = player.position


def _lancer_jeu(world: World) -> None:
    state = _get_state(world)
    state.jeu_pre = True
    state.etat = "jeu"
    level = _get_level_component(world).level
    player_component = _get_player_component(world)
    if player_component.player is None:
        player_component.player = monde.joueur(level.debut)
    player_component.player.position = level.debut
    _sync_player_sprite(player_component.player)


def _ouvrir_sauvegardes_depuis_menu(world: World) -> None:
    state = _get_state(world)
    state.jeu_pre = False
    state.etat = "menus_sauvegarde"


def _fermer_jeu(world: World) -> None:
    state = _get_state(world)
    state.running = False


def _reprendre_jeu(world: World) -> None:
    state = _get_state(world)
    state.etat = "jeu"


def _retour_menu(world: World) -> None:
    state = _get_state(world)
    state.etat = "menu"


def _ouvrir_editeur_niveau(world: World) -> None:
    logging.info("Ouverture de l'éditeur de niveau")
    state = _get_state(world)
    state.etat = "editeur_niveau"


def _charger_sauvegarde(world: World, nom_sauvegarde: str) -> None:
    logging.info("chargement du niveau %s", nom_sauvegarde)
    niveau = filesytem.charger_niveau(nom_sauvegarde)
    _set_level(world, niveau)
    _set_player(world, monde.joueur(niveau.debut))
    _get_state(world).etat = "jeu"


def _menu_principal(world: World) -> Menu:
    menu_principal = Menu(
        "menu principal",
        "fichier_jeux/menus/image de fond.jpg",
        "fichier_jeux/menus/logo.png",
    )
    menu_principal.dim_logo = vec2(0.3, 0.27)
    menu_principal.ajouter_bouton(vec2(0.5, 0.43), vec2(0.2, 0.1), lambda: _lancer_jeu(world), "jouer")
    menu_principal.ajouter_bouton(
        vec2(0.5, 0.57),
        vec2(0.2, 0.1),
        lambda: _ouvrir_sauvegardes_depuis_menu(world),
        "sauvegardes",
    )
    menu_principal.ajouter_bouton(
        vec2(0.5, 0.85),
        vec2(0.2, 0.1),
        lambda: _ouvrir_editeur_niveau(world),
        "editeur de niveau",
    )
    menu_principal.ajouter_bouton(vec2(0.5, 0.7), vec2(0.2, 0.1), lambda: _fermer_jeu(world), "quitter")
    return menu_principal


def _menu_pause(world: World) -> Menu:
    menu_pause = Menu("menu pause", "fichier_jeux/menus/image de fond.jpg")
    menu_pause.ajouter_bouton(vec2(0.5, 0.5), vec2(0.2, 0.1), lambda: _reprendre_jeu(world), "reprendre")
    return menu_pause


def _menu_sauvegarde(world: World) -> Menu:
    menu_sauvegarde = Menu("menuspause", "fichier_jeux/menus/image de fond.png")
    index = 0

    for key in filesytem.sauvegardes_dispo.keys():
        y = 0.2 + index * 0.08
        menu_sauvegarde.ajouter_bouton(
            vec2(0.5, y),
            vec2(0.08, 0.05),
            lambda nom=key: _charger_sauvegarde(world, nom),
            f"sauvegarde : {key}",
        )
        index += 1

    menu_sauvegarde.ajouter_bouton(vec2(0.05, 0.17), vec2(0.08, 0.05), lambda: _retour_menu(world), "quitter")
    return menu_sauvegarde


def _ui_system(world: World) -> None:
    state = _get_state(world)
    event = world.resources.get("event")
    if state.etat == "menu":
        menu = _menu_principal(world)
        menu.afficher()
        if event is not None:
            for bouton in menu.bouton:
                bouton.action(event)
    elif state.etat == "pause":
        menu = _menu_pause(world)
        menu.afficher()
        if event is not None:
            for bouton in menu.bouton:
                bouton.action(event)
    elif state.etat == "menus_sauvegarde":
        menu = _menu_sauvegarde(world)
        menu.afficher()
        if event is not None:
            for bouton in menu.bouton:
                bouton.action(event)
    elif state.etat == "editeur_niveau":
        _ouvrir_editeur_niveau(world)


def _physics_system(world: World) -> None:
    state = _get_state(world)
    if state.etat != "jeu":
        return
    player_entity = world.resources["player_entity"]
    player_component = world.get_component(player_entity, PlayerComponent)
    physics_component = world.get_component(player_entity, PhysicsComponent)
    if player_component is None or physics_component is None or not physics_component.enabled:
        return
    dt = world.resources.get("dt", 0.0)
    if dt <= 0:
        return
    worker: PhysicsWorker = world.resources["physics_worker"]
    pending = world.resources.get("physics_pending", False)
    if pending:
        result = worker.poll()
        if result is None:
            return
        pos_x, pos_y = result["position"]
        vel_x, vel_y = result["velocity"]
        player_component.player.position = vec2(pos_x, pos_y)
        player_component.player.vitesse = vec2(vel_x, vel_y)
        _sync_player_sprite(player_component.player)
        world.resources["physics_pending"] = False
    if not world.resources.get("physics_pending", False):
        level = _get_level_component(world).level
        payload = {
            "dt": dt,
            "position": (player_component.player.position.x, player_component.player.position.y),
            "velocity": (player_component.player.vitesse.x, player_component.player.vitesse.y),
            "gravity": (level.gravite.x, level.gravite.y),
        }
        worker.step(payload)
        world.resources["physics_pending"] = True


def _render_system(world: World) -> None:
    state = _get_state(world)
    if state.etat != "jeu":
        return
    level = _get_level_component(world).level
    player = _get_player_component(world).player
    level.afficher_fond()
    level.avant.afficher()
    level.afficher_decor()
    level.afficher_terrain()
    level.devant.afficher()
    level.afficher_devant()
    _sync_player_sprite(player)
    player.afficher()


class EcsGame:
    def __init__(self) -> None:
        self.world = World()
        self.scheduler = Scheduler()
        self._physics_worker = PhysicsWorker()
        self._setup_world()
        self._setup_systems()
        self.running = True

    def _setup_world(self) -> None:
        level = monde.niveau()
        level_entity = self.world.create_entity()
        self.world.add_component(level_entity, LevelComponent(level))
        player_entity = self.world.create_entity()
        player = monde.joueur(level.debut)
        self.world.add_component(player_entity, PlayerComponent(player))
        self.world.add_component(player_entity, PhysicsComponent(enabled=PHYSICS_ENABLED))
        self.world.resources["game_state"] = GameState()
        self.world.resources["level_entity"] = level_entity
        self.world.resources["player_entity"] = player_entity
        self.world.resources["physics_worker"] = self._physics_worker
        self.world.resources["physics_pending"] = False
        self.world.resources["event"] = None
        self.world.resources["dt"] = 0.0

    def _setup_systems(self) -> None:
        self.scheduler.add_system(_ui_system)
        self.scheduler.add_system(_physics_system)
        self.scheduler.add_system(_render_system)

    def step(self, event: graphisme.evenement | None, dt: float) -> None:
        self.world.resources["event"] = event
        self.world.resources["dt"] = dt
        self.scheduler.run(self.world)
        self.running = self.world.resources["game_state"].running

    def shutdown(self) -> None:
        self._physics_worker.close()

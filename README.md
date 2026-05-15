# procjec2

procject universitaire de jeu saute mouton 


asset utiliser :
[text](https://freesound.org/people/SG80_MED1A/sounds/789408/)

## Lancer le jeu
-lancer install.sh
- Les coordonnées `Vec2` utilisées pour l'interface sont normalisées (`x` et `y` entre `0` et `1`).

## Migration ECS / multiprocessing
- Périmètre prioritaire : joueur, collisions, menus, sauvegardes.
- Pipeline ECS basé sur `esper` dans `ecs_game.py` (composants + systèmes).
- Multiprocessing : un worker de physique est prêt pour les tâches non‑UI (rendu gardé dans le processus principal).
- La physique multiprocess est désactivée par défaut pour préserver le comportement actuel : passer `PHYSICS_ENABLED = True` dans `ecs_game.py` pour l'activer.



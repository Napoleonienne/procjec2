# procjec2

procject universitaire de jeu saute mouton 


asset utiliser :
[text](https://freesound.org/people/SG80_MED1A/sounds/789408/)

## Version C++23 (SDL2 + xmake)
- Installer xmake et un compilateur C++23.
- Construire : `xmake`
- Exécuter : `xmake run saute_mouton`
- Lancer depuis la racine du dépôt pour charger les assets.
- Dépendances gérées par xmake : `sdl2`, `sdl2_image`, `nlohmann_json`.
- Les boutons sont rendus comme rectangles pour l'instant (pas de rendu texte).

## Lancer le jeu (Python)
- Créer/activer un venv puis installer les dépendances : `pip install -r req.txt`
- Exécuter : `python main.py`
- La taille de fenêtre est configurée via `fichier_jeux/option jeux/option.json` (`fenetre.largeur`, `fenetre.hauteur`).
- Les coordonnées `Vec2` utilisées pour l'interface sont normalisées (`x` et `y` entre `0` et `1`).

## Compiler avec PyInstaller
Sous Linux/macOS :
```
pyinstaller --onefile --noconsole \
  --name saute_mouton \
  main.py \
  --add-data "fichier_jeux:fichier_jeux" \
  --hidden-import nava \
  --hidden-import tkinter \
  --hidden-import PIL.ImageTk \
  --hidden-import PIL._tkinter_finder
```

Sous Windows (remplacer `:` par `;` dans `--add-data`) :
```
pyinstaller --onefile --noconsole ^
  --name saute_mouton ^
  main.py ^
  --add-data "fichier_jeux;fichier_jeux" ^
  --hidden-import nava ^
  --hidden-import tkinter ^
  --hidden-import PIL.ImageTk ^
  --hidden-import PIL._tkinter_finder
```

Les sauvegardes sont stockées dans `~/.saute_mouton/save` pour la version PyInstaller.

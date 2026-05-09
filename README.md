# procjec2

procject universitaire de jeu saute mouton 


asset utiliser :
[text](https://freesound.org/people/SG80_MED1A/sounds/789408/)

## Lancer le jeu
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

# Project Guidelines

## Project Context
This repository is an early-stage university 2D game prototype in Python.
Code and comments are mostly in French; keep existing French naming unless explicitly asked to translate.

## Build And Run
- Create/activate a Python virtual environment before running commands.
- Install dependencies with: pip install -r req.txt
- Run the app with: python main.py
- There is currently no automated test suite in this repository.

## Architecture
- main.py: startup entrypoint that launches the app loop.
- app.py: app lifecycle and main loop orchestration.
- graphisme.py: rendering and direct FLTK integration.
- monde.py: world state models (joueur, niveau, tuile).
- vect.py: shared vector math utilities.
- ecs.py: ECS scaffolding (currently partial).
- physique.py and menus.py: placeholders for upcoming systems.
- filesytem.py: serialization experiments and file format notes.

## Conventions
- Preserve existing module boundaries; avoid putting rendering code outside graphisme.py.
- Keep math/helper logic in vect.py and reuse Vec2 instead of duplicating vector code.
- Prefer type hints in new Python code (project uses Python 3.10 style unions with |).
- Match current naming style in touched files (French domain terms are expected).
- Keep changes focused; do not rewrite unrelated spelling/style issues unless requested.

## Known Pitfalls
- main.py currently uses a broken __name__ guard and may not start as expected.
- app.py contains main loop timing logic that is likely incorrect.
- Logging is configured in multiple files; avoid adding new logging setup locations.

## Documentation
- Use README.md as the current project reference and update it when behavior or commands change.
- If adding substantial new subsystems, add focused docs under a docs/ folder and link from README.md.

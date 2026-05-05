from pickle import TRUE

import graphisme
from vect import Vec2 as vec2

class Tuile:
    """
    Classe de base pour les tuiles du jeu (système de bounding box).
    Représente une tuile avec une position, une texture et une taille.
    """
    def __init__(self, pos: vec2, texture: str, taille: int = 32):
        self.id: int | None = None
        self._texture: str = texture
        self._taille: int = taille
        self._pos: vec2 = pos

        self.property = {
            "solide": False,
            "rebondissante": False,
            "glissante": False,
            "amortissante": False,
            "mortelle": False,    
        }

    @property
    def pos(self) -> vec2:
        return self._pos

    @pos.setter
    def pos(self, value: vec2):
        self._pos = value

    @property
    def texture(self) -> str:
        return self._texture

    @property
    def taille(self) -> int:
        return self._taille

    @taille.setter
    def taille(self, value: int):
        self._taille = value

    @property
    def coin_haut_gauche(self) -> vec2:
        return self.pos - vec2(self.taille, self.taille) / 2

    @property
    def coin_bas_droit(self) -> vec2:
        return self.pos + vec2(self.taille, self.taille) / 2
    
    def serialisation(self) -> dict:
        """Convertit la tuile en un dictionnaire pour la sérialisation dans le json."""
        return {
            "pos": {"x": self.pos.x, "y": self.pos.y},
            "taille": self.taille,
            "texture": self.texture,
            "property": self.property
        }
    





class Sprite:
    """
    Classe de base pour les personnages et objets du jeu.
    Contrairement à Tuile, un Sprite a une position et une taille libres.
    
    """
    def __init__(self, pos: vec2, texture: str, taille: vec2 = vec2(32, 32)):
        self.id: int | None = None
        self._texture: str = texture
        self._taille: vec2 = taille
        self._pos: vec2 = pos
        self.property = {
            "solide": False,
        }

    @property
    def pos(self) -> vec2:
        return self._pos

    @pos.setter
    def pos(self, value: vec2):
        self._pos = value

    @property
    def taille(self) -> vec2:
        return self._taille

    @taille.setter
    def taille(self, value: vec2):
        self._taille = value

    @property
    def texture(self) -> str:
        return self._texture
    
    def serialisation(self) -> dict:
        """Convertit le sprite en un dictionnaire pour la sérialisation dans le json."""
        return {
            "pos": {"x": self.pos.x, "y": self.pos.y},
            "taille": {"x": self.taille.x, "y": self.taille.y},
            "texture": self.texture,
            "property": self.property
        }

    
    @property
    def coin_haut_gauche(self) -> vec2:
        return self.pos - self.taille / 2

    @property
    def coin_bas_droit(self) -> vec2:
        return self.pos + self.taille / 2
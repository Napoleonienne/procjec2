import graphisme
from vect import Vec2 as vec2

class Tuile:
    """
    Classe de base pour les tuiles du jeu (système de bounding box).
    Représente une tuile avec une position, une texture et une taille.
    """
    def __init__(self, pos: vec2, texture: str, taille: vec2 = vec2(32, 32)):
        self._texture: str = texture
        self._taille: vec2 = taille
        self._pos: vec2 = pos

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
    def taille(self) -> vec2:
        return self._taille

    @taille.setter
    def taille(self, value: vec2):
        self._taille = value

    def afficher(self):
        """Affiche la tuile à l'écran."""
        graphisme.afficher_sprite(self._texture, self._pos, self._taille)

    def collision(self, other: 'Tuile') -> bool:
        """Vérifie si cette tuile entre en collision avec une autre (bounding box)."""
        return (
            self._pos.x < other._pos.x + other._taille.x and
            self._pos.x + self._taille.x > other._pos.x and
            self._pos.y < other._pos.y + other._taille.y and
            self._pos.y + self._taille.y > other._pos.y
        )

class Sprite:
    """
    Classe de base pour les personnages et objets du jeu.
    Contrairement à Tuile, un Sprite a une position et une taille libres.
    """
    def __init__(self, pos: vec2, texture: str, taille: vec2 = vec2(32, 32)):
        self._texture: str = texture
        self._taille: vec2 = taille
        self._pos: vec2 = pos

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

    def afficher(self):
        """Affiche le sprite à l'écran."""
        graphisme.afficher_sprite(self._texture, self._pos, self._taille)
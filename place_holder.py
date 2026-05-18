from dataclasses import dataclass
from socket import TCP_QUICKACK
import graphisme
import vect
vec2 = vect.Vec2

class Object2d:
    """
    classe de base pour tout les object pour l'instant sprite et tuile mais je verrez plus tard pour ajouter plus
    """

    def __init__(self, pos: vec2, texture: str, taille: vec2 | int,tag:str="") :
        """
        Args:
            pos (vec2): Position centrale de l'objet.
            texture (str): Chemin vers la texture.
            taille (vec2 | int): Taille de l'objet.     
               
        """
        self.id: int | None = None
        self.texture: str = texture
        self.pos: vec2 = pos
        self.tag: str = tag

        if isinstance(taille, int):
            self._taille: vec2 = vec2(taille, taille)
        else:
            self._taille = taille

        self.property ={

        }


 
    @property
    def taille(self) -> vec2:
        return self._taille

    @taille.setter
    def taille(self, value: vec2 | int):
        if isinstance(value, int):
            self._taille = vec2(value, value)
        else:
            self._taille = value


    @property
    def coin_haut_gauche(self) -> vec2:
        """

        Returns:
            vec2: le resultat
        """
        return self.pos - self.taille / 2

    @property
    def coin_bas_droit(self) -> vec2:
        """

        Returns:
            vec2: le resultat
        """
        return self.pos + self.taille / 2

    def serialisation(self) -> dict:
        """serialise l'object en dictionnaire

        Returns:
            dict: _description_
        """
        return {
            "pos": {"x": self.pos.x, "y": self.pos.y},
            "taille": {"x": self.taille.x, "y": self.taille.y},
            "texture": self.texture,
            "property": self.property,
        }


class Sprite(Object2d):
    """Classe pour les sprites (joueur, objets mobiles, etc.)."""
    def __init__(self, pos: vec2, texture: str, taille: vec2,tag:str=""):
        """
        Args:
            taille (vec2): Taille du sprite (rectangle).
        """
        super().__init__(pos, texture, taille, tag)
        # Propriétés spécifiques aux sprites (si besoin)
        self.property.update({

        })

class Tuile(Object2d):
    """Classe pour les tuiles du jeu (blocs du niveau)."""
    def __init__(self, pos: vec2, texture: str, taille: int = 32, tag: str = ""):
        """
        Args:
            taille (int): Taille du côté de la tuile (carrée).
        """
        super().__init__(pos, texture, taille, tag)
        # Propriétés spécifiques aux tuiles
        self.property.update({
            "solide": False,
            "rebondissante": False,
            "glissante": False,
            "amortissante": False,
            "mortelle": False,    
        }
        )
    







import math
class Vec2:
    """
    classe de vecteur utille pour les math
    """
    def __init__(self,x:float=0,y:float=0):
        self.x:float =x
        self.y:float = y
    def __add__(self, other:Vec2)->Vec2:
        
        return Vec2(self.x +other.x,
                    self.y+other.y
                    )
    def __sub__(self, other:Vec2)->Vec2:
        return Vec2(self.x -other.x
            ,self.y-other.y
            )
    
    def __mul__(self, other:float)->Vec2:
        return Vec2(self.x*other ,self.y*other)
    def __truediv__(self, other:float)->Vec2:
            return Vec2(self.x/other ,self.y/other)
    def __str__(self) -> str:
        return f"({self.x},{self.y})"
   

def norme(vec:Vec2)->float:
    """
    renvoie la norme du vecteur

    Args:
        vec (Vec2): _description_

    Returns:
        float: _description_
    """
    return (vec.x**2 +vec.y**2 )**0.5
def normalize(vec:Vec2)->Vec2:
    """met le vecteur a une norme de 1

    Args:
        vec (Vec2): _description_

    Returns:
        Vec2: _description_
    """
    return vec/norme(vec)
def dot(vecA:Vec2,vecB:Vec2)->float:
    """
    PRODUIT scalaire
    Args:
        vecA (Vec2): 1er vecteur
        vecB (Vec2): 2ème vecteur

    Returns:
        float: scalaire
    """
    return vecA.x*vecB.x+vecA.y*vecB.y

def cross(vecA:Vec2,vecB:Vec2)->float:
    """
    pour savoir la direction ou va le personnage
    """
    return vecA.x*vecB.y+vecA.y*vecB.x

def rotate(vec:Vec2,angle:float)->Vec2:
    """_summary_

    Args:
        vec (Vec2): vecteur origine
        angle (float): la rotation en degré

    Returns:
        Vec2: le vecteur 
    """
    rad = math.radians(angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    return Vec2(vec.x * cos_a - vec.y * sin_a,
                vec.x * sin_a + vec.y * cos_a)
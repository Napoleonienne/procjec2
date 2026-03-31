import math
class vec2:
    def __init__(self,x=0,y=0):
        self.x =x
        self.y = y
    def __add__(self, other):
        
        return vec2(self.x +other.x,self.y+other.y)
    def __sub__(self, other):
        return vec2(self.x -other.x,self.y-other.y)
    
    def __mul__(self, other:float):
        return vec2(self.x*other ,self.y*other)
    def __truediv__(self, other):
            return vec2(self.x /other ,self.y/other)

def norme(vec:vec2):
    return (vec.x**2 +vec.y**2 )**1/2
def normalize(vec:vec2):
    return vec2/norme(vec2)
def dot(vecA:vec2,vecB:vec2):
    return vecA.x*vecB.x+vecA.y*vecB.y

def cross(vecA:vec2,vecB:vec2):
    """
    pour savoir la direction ou va le personnage
    """
    return vecA.x*vecB.y+vecA.y*vecB.x
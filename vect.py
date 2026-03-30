


class vec2:
    def __init__(self,x=0,y=0):
        self.x =x
        self.y = y
    def __add__(self, other):
        
        return vec2(self.x +other.x,self.y)
    
    def __mul__(self, other:float):
        return vec2(self.x*other,self.y*other)


def dot(vecA:vec2,vecB:vec2):
    return vecA.x*vecB.x+vecA.y*vecB.y
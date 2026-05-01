from vect import Vec2 as vec2




class tuile:
    """
    classe de tuile qui va etre la classe de base pour les tuile du jeu

    appararament j'ai fais plutot un syteme de bounding box

    """
    def __init__(self,pos:vec2,texture:str,taille:int =32):
        self.textture:str = texture
        self.taille:int = taille
        self.pos:vec2 = pos

    def get_pos(self):
        return self.pos
    
    def get_texture(self):
        return self.textture

    def get_taille(self):
        return self.taille

    def set_pos(self,pos:vec2):
        self.pos = pos

    def set_taille(self,taille:int):
        self.taille = int

    

    


class sprite:
    """
    classe de sprite qui va etre la classe de base pour les personnage et les objet du jeu
    qui a une position libre et une taille libre
    """
    def __init__(self,pos:vec2,texture:str):
        self.texture:str = texture
        self.taille:vec2 = vec2()
        self.pos:vec2 = pos


    def get_pos(self):
        return self.pos

    def get_taille(self):
        return self.taille

    def set_pos(self,pos:vec2):
        self.pos = pos

    def set_taille(self,taille:vec2):
        self.taille = taille

import PIL.Image

import graphisme
import monde
import place_holder
import logging
import vect
import filesytem
import PIL

CHEMIN_DEFAUT = "fichier_jeux/asset"
def decouper_tilesher(image, tile_size,name:str,chemin:str =CHEMIN_DEFAUT):
    """deoupe automatique de caré d'une taill t

    Args:
        image (_type_): _description_
        tile_size (_type_): _description_
        name (str): _description_
        chemin (str, optional): _description_. Defaults to CHEMIN_DEFAUT.

    Returns:
        _type_: _description_
    """
    if type(image) == str:
        image = PIL.Image.open(image)




    tiles = []
    for y in range(0, image.height, tile_size):
        for x in range(0, image.width, tile_size):
            box = (x, y, x + tile_size, y + tile_size)
            tile = image.crop(box)
            tiles.append(tile)
    return tiles



def decouper_image(image:str|PIL.Image.Image,box:tuple[int],name:str,chemin:str = CHEMIN_DEFAUT):
    """_summary_

    Args:
        image (str | PIL.Image.Image): image ou le chenmin de l'image
        box (tuple[int]): le carré adecouper
        name (str): le nom de l'image à sauvegarder
        chemin (str, optional): chemin ou sauvegarder l'image. Defaults to CHEMIN_DEFAUT.

    Returns:
        _type_: _description_
    """
    if type(image) == str:
        imag: PIL.Image.Image = PIL.Image.open(image)
    else:
        imag: PIL.Image.Image = image #type: ignore
    

    nv_img = imag.crop(box) #type: ignore
    nv_img.save(chemin)
    return nv_img



class EditeurNiveau:
    def __init__(self,nom:str ,niveau: monde.niveau):
        self._monde = niveau
        

        self.tile_selectionne = 0
        self.nom = nom

    def ajouter_tuile(self, pos: vect.Vec2):
        
    



    def sauvegarder_nv(self, chemin:str = CHEMIN_DEFAUT):
        filesytem.sauvegarder_niveau(self._monde, self.nom)






    
    

    








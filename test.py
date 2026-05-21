from email.mime import image

import fltk
from PIL import Image




from itertools import cycle

cycle = cycle([0,1,2,3,4])


fltk.cree_fenetre(400, 400,)


image = Image.open("fichier_jeux/missing.jpg")






a = (i for i in range(5))
for i in range(5):
    print(next(a))




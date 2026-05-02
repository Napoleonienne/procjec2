import itertools
import logging
import time

import fltk
import graphisme


logging.basicConfig(
    level=logging.DEBUG, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='w'         
)



def test():
    """_summary_

    """
    graphisme.afficher(True)
    graphisme.creer_grille(8,"blue")
    graphisme.creer_grille(16,"yellow")
    graphisme.creer_grille(32,"red")
    


    k = itertools.product(range(0,graphisme.LARGEUR+1,16),range(0,graphisme.HAUTEUR+1,16))

    graphisme.afficher_sprite("asset/joueur/mouton.png",graphisme.Vec2(100,100),graphisme.Vec2(32,32))

    abj:graphisme.bouton = graphisme.bouton(graphisme.Vec2(400,400),graphisme.Vec2(100,100),"test",lambda : print("test"))
    abj.afficher()

    
            

    while True:
        ev =  fltk.donne_ev()
        tev =  fltk.type_ev(ev)
        graphisme.swapbuffer()
        time.sleep(0.1)
        graphisme.positionner_grille("asset/vert.jpg",graphisme.Vec2(*next(k)),16)
        abj.action(ev)

        if graphisme.shouldclose(tev):
            break

    graphisme.fermer()
    return

class app:
    menu_etat = True
    dt =0
    lastframe =0
    def run(self):
        graphisme.afficher()
        self.mainloop()
        graphisme.fermer()
       
    def menu(self):
     
        return


    def mainloop(self):
        ev:str =""
        tev:str = ""
        while graphisme.shouldclose(tev):
            firstframe = time.time_ns()
            if app.menu_etat:
                self.menu()





            
            graphisme.swapbuffer()
            dt = app.lastframe -firstframe
            lastframe = firstframe
            pass
        return None


from calendar import c
import itertools
import logging
import time

import fltk
import graphisme
from menus import Menu


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='w'         
)





class app:
    etat = "menu"
    #etats_possibles = ["menu","jeu","pause","gameover"]  a titre indicative
    dt =0
    lastframe =0
    def run(self):
        graphisme.afficher()
        self.mainloop()
        graphisme.fermer()
        logging.info("Boucle principale terminée.")
       
    def menu_principal(self):
        menuprincipal: Menu = Menu("menu principal","fichier jeux/fond/menu.png","fichier jeux/fond/logo.png")
        return
    
    def menu_pause(self):
        menuPause :Menu = Menu("menu pause","fichier jeux/fond/pause.png")


    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement =graphisme.get_evenement()
        while not graphisme.shouldclose(evenement.type):
            evenement =graphisme.get_evenement()

            firstframe = time.time_ns()
          

            match app.etat:
                case "menu":
                    self.menu()
                case "jeu":
                    pass
                case "pause":
                    pass
                case "gameover":
                    pass

                case _:
                    logging.warning(f"État inconnu : {app.etat}")





            
            graphisme.swapbuffer()
            dt = app.lastframe -firstframe
            lastframe = firstframe
            pass
        return None


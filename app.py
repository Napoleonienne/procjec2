import itertools
import logging
import time

import fltk
import graphisme


logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='w'         
)





class app:
    menu_etat = True
    dt =0
    lastframe =0
    def run(self):
        graphisme.afficher()
        self.mainloop()
        graphisme.fermer()
        logging.info("Boucle principale terminée.")
       
    def menu(self):
     
        return


    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement =graphisme.get_evenement()
        while not graphisme.shouldclose(evenement.type):
            evenement =graphisme.get_evenement()

            firstframe = time.time_ns()
            if app.menu_etat:
                self.menu()





            
            graphisme.swapbuffer()
            dt = app.lastframe -firstframe
            lastframe = firstframe
            pass
        return None


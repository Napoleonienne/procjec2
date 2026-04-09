import logging
from time import time_ns as time
import graphisme


logging.basicConfig(
    level=logging.DEBUG, 
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
       
    def menu(self):
     
        return


    def mainloop(self):
        ev:str =""
        tev:str = ""
        while graphisme.shouldclose(tev):
            firstframe = time()
            if app.menu_etat:
                self.menu()





            
            graphisme.swapbuffer()
            dt = app.lastframe -firstframe
            lastframe = firstframe
            pass
        return None


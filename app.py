
from time import time_ns as time
import graphisme

class app:
    menu_etat = True
    dt =0
    lastframe =0
    def run(self):
        graphisme.afficher()
        self.mainloop()
        graphisme.fermer()
       
    def menu():


        return


    def mainloop(self):
        while graphisme.shouldclose:
            firstframe = time()
            if self.menu_etat:
                self.menu()





            
            graphisme.swapbuffer()
            dt = lastframe -firstframe
            lastframe = firstframe

            pass


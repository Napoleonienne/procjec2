
from time import time_ns as time
import graphisme
class app:
    
    dt =0
    lastframe =0
    def run(self):
        graphisme.afficher()
        self.mainloop()
        graphisme.fermer()
       
       

    def mainloop(self):
        while graphisme.shouldclose:
            firstframe = time()





            
            graphisme.swapbuffer()
            dt = lastframe -firstframe
            lastframe = firstframe

            pass


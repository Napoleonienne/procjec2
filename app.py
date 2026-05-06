from calendar import c
import itertools
import logging
import time
import vect
import fltk
import graphisme
from menus import Menu
import filesytem
import monde

vec2 = vect.Vec2

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='w'         
)





class app:
    jeu_pre = True # juste si il etait en jeux ou pas
    etat = "menu"
    #etats_possibles = ["menu","jeu","pause","gameover", "editeur_niveau"]  a titre indicative
    dt =0
    lastframe =0
    level_actuel:monde.niveau  = monde.niveau()
    def run(self):
        graphisme.afficher()
        filesytem.peupler_sauvegardes()
        
        self.mainloop()
        graphisme.fermer()
        logging.info("Boucle principale terminée.")
       
    def menu_principal(self):
        menuprincipal: Menu = Menu("menu principal","fichier jeux/fond/menu.png","fichier jeux/fond/logo.png")


        return
    
    def menu_pause(self):
        menuPause :Menu = Menu("menu pause","fichier jeux/fond/pause.png")

    def quitter(self):
        """
        permet de quitter un menus 
        """
        logging.info(f" quiitte le menus")
        if self.jeu_pre == True:
            self.etat = "jeu" 
        else:
            self.etat = "menus"


    def menus_sauvegarde(self):
        menusaugarde:Menu = Menu("menuspause", "fichier jeux/fond/pause.png")
        i =0
        
        for key,path in filesytem.sauvegardes_dispo.items():
            i += 40


            def sauvegarde():
                logging.info(f"chagement du niveau {key} ui se trouve {path}")
                app.level_actuel =  filesytem.charger_niveau(key)
            menusaugarde.ajouter_bouton(vec2(graphisme.LARGEUR/2,i),vec2(80,30),sauvegarde,f"sauvegarde : {key}")

    

        menusaugarde.ajouter_bouton(vec2(50,100),vec2(10,20),self.quitter,"quitter")

        menusaugarde.afficher()




    


    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement =graphisme.get_evenement()
        while not graphisme.shouldclose(evenement):
            evenement =graphisme.get_evenement()

            firstframe = time.time_ns()
          

            match app.etat:
                case "menu":
                    self.menu_principal()
                case "jeu":
                    

                    monde.joueur(self.level_actuel.debut)
                case "pause":
                    pass
                case "gameover":
                    pass
                case "editeur_niveau":
                    pass
                case "menus_sauvegarde":
                    pass

                case _:
                    logging.warning(f"État inconnu : {app.etat}")
                    raise ValueError(f"État inconnu : {app.etat}")





            
            graphisme.swapbuffer()
            dt = app.lastframe -firstframe
            lastframe = firstframe
            pass
        return None


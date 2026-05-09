import logging
import time
from typing import Optional
import vect
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
  
    def __init__(self):
        self.jeu_pre = True
        self.etat = "menu"
        self.dt = 0
        self.lastframe = 0
        self.level_actuel = monde.niveau()
        self.joueur_actuel = None  

    
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
                self.level_actuel =  filesytem.charger_niveau(key)
            menusaugarde.ajouter_bouton(vec2(graphisme.LARGEUR/2,i),vec2(80,30),sauvegarde,f"sauvegarde : {key}")

    

        menusaugarde.ajouter_bouton(vec2(50,100),vec2(10,20),self.quitter,"quitter")

        menusaugarde.afficher()

    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement:graphisme.evenement | None = None
       
        while not graphisme.shouldclose(evenement):
            evenement = graphisme.get_evenement()
        
            firstframe = time.time_ns()

            match self.etat:
                case "menu":
                    self.menu_principal()
                case "jeu":
                    if self.joueur_actuel:
                        self.joueur_actuel.afficher()
                        # physique, inputs, etc.
                case "pause":
                    self.menu_pause()
                case "menus_sauvegarde":
                    self.menus_sauvegarde()
                case _:
                    logging.warning(f"État inconnu : {self.etat}")
                    raise ValueError(f"État inconnu : {self.etat}")

            graphisme.swapbuffer()
            self.dt = firstframe - self.lastframe
            self.lastframe = firstframe

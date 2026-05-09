import logging
import time
from typing import Optional
import vect
import graphisme
from menus import Menu
import filesytem
import monde

vec2 = vect.Vec2
NANOSECONDES_PAR_SECONDE = 1_000_000_000

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  
    filemode='w'         
)





class app:
  
    def __init__(self):
        self.en_cours = True
        self.jeu_pre = True
        self.etat = "menu"
        self.dt = 0
        self.lastframe: int | None = None
        self.level_actuel = monde.niveau()
        self.joueur_actuel: monde.joueur | None = None  

    
    def run(self):
        options = filesytem.charger_options()
        fenetre = options["fenetre"]
        graphisme.ouvrir_fenetre(largeur=fenetre["largeur"], hauteur=fenetre["hauteur"])
        filesytem.peupler_sauvegardes()
        
        self.mainloop()
        graphisme.fermer()
        logging.info("Boucle principale terminée.")
       
    def menu_principal(self):
        menuprincipal: Menu = Menu(
            "menu principal",
            "fichier_jeux/menus/image de fond.png",
            "fichier_jeux/menus/logo.png",
        )
        menuprincipal.ajouter_bouton(vec2(0.5, 0.43), vec2(0.2, 0.1), self.lancer_jeu, "jouer")
        menuprincipal.ajouter_bouton(vec2(0.5, 0.57), vec2(0.2, 0.1), self.ouvrir_sauvegardes_depuis_menu, "sauvegardes")
        menuprincipal.ajouter_bouton(vec2(0.5, 0.7), vec2(0.2, 0.1), self.fermer_jeu, "quitter")
        return menuprincipal
    
    def menu_pause(self):
        menuPause: Menu = Menu("menu pause", "fichier_jeux/menus/image de fond.png")
        menuPause.ajouter_bouton(vec2(0.5, 0.5), vec2(0.2, 0.1), self.reprendre_jeu, "reprendre")
        return menuPause

    def lancer_jeu(self):
        self.jeu_pre = True
        self.etat = "jeu"
        if self.joueur_actuel is None:
            self.joueur_actuel = monde.joueur(self.level_actuel.debut)

    def ouvrir_sauvegardes_depuis_menu(self):
        self.jeu_pre = False
        self.etat = "menus_sauvegarde"

    def fermer_jeu(self):
        self.en_cours = False

    def reprendre_jeu(self):
        logging.info("reprend le jeu")
        self.etat = "jeu"

    def retour_menu(self):
        logging.info("retour au menu")
        self.etat = "menu"


    def menus_sauvegarde(self):
        menusaugarde: Menu = Menu("menuspause", "fichier_jeux/menus/image de fond.png")
        index = 0

        def creer_action_sauvegarde(nom_sauvegarde: str, chemin_sauvegarde):
            def charger_sauvegarde():
                logging.info(f"chargement du niveau {nom_sauvegarde} qui se trouve {chemin_sauvegarde}")
                self.level_actuel = filesytem.charger_niveau(nom_sauvegarde)
                self.joueur_actuel = monde.joueur(self.level_actuel.debut)
                self.etat = "jeu"
            return charger_sauvegarde
        
        for key,path in filesytem.sauvegardes_dispo.items():
            y = 0.2 + index * 0.08
            action = creer_action_sauvegarde(key, path)
            menusaugarde.ajouter_bouton(vec2(0.5, y),vec2(0.08,0.05),action,f"sauvegarde : {key}")
            index += 1

    

        menusaugarde.ajouter_bouton(vec2(0.05,0.17),vec2(0.08,0.05),self.retour_menu,"quitter")

        return menusaugarde

    def afficher_jeu(self):
        self.level_actuel.afficher_fond()
        self.level_actuel.avant.afficher()
        self.level_actuel.afficher_decor()
        self.level_actuel.afficher_terrain()
        self.level_actuel.objet.afficher()
        self.level_actuel.afficher_devant()
        if self.joueur_actuel:
            self.joueur_actuel.afficher()

    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement:graphisme.evenement | None = None
       
        while self.en_cours and not graphisme.shouldclose(evenement):
            evenement = graphisme.get_evenement()
        
            firstframe = time.time_ns()
            graphisme.effacer_tout()

            match self.etat:
                case "menu":
                    menu = self.menu_principal()
                    menu.afficher()
                    for bouton in menu.bouton:
                        bouton.action(evenement)
                case "jeu":
                    self.afficher_jeu()
                case "pause":
                    menu = self.menu_pause()
                    menu.afficher()
                    for bouton in menu.bouton:
                        bouton.action(evenement)
                case "menus_sauvegarde":
                    menu = self.menus_sauvegarde()
                    menu.afficher()
                    for bouton in menu.bouton:
                        bouton.action(evenement)
                case _:
                    logging.warning(f"État inconnu : {self.etat}")
                    raise ValueError(f"État inconnu : {self.etat}")

            graphisme.swapbuffer()
            if self.lastframe is None:
                self.dt = 0
            else:
                self.dt = (firstframe - self.lastframe) / NANOSECONDES_PAR_SECONDE
            self.lastframe = firstframe

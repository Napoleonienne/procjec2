import code
from email import generator
import logging
import time
from typing import Optional
import vect
import graphisme
from menus import Menu
import filesytem
import monde
import physique
import editeur_niveau
import solveur


vec2 = vect.Vec2

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
        self.etat = "menu" # etat possible : menu, jeu, pause, menus_sauvegarde, editeur_niveau
        self.dt = 0
        self.lastframe: int | None = None
        self.level_actuel = monde.niveau("ph")
        self.joueur_actuel: monde.joueur | None = None  
        self.distance_max = 0
        self.menusaugarde:Menu = Menu("menuspause", "fichier_jeux/menus/image de fond.png") 

   

        self.MenuPause:Menu = Menu("menu pause", "fichier_jeux/menus/image de fond.jpg")
        self.MenuPause.ajouter_bouton(vec2(0.5, 0.2), vec2(0.2, 0.1), self.ouvrir_sauvegardes_depuis_menu, texte="sauvegardes")

        self.MenuPause.ajouter_bouton(vec2(0.5, 0.2), vec2(0.2, 0.1), self.ouvrir_sauvegardes_depuis_menu, "sauvegardes")
        self.MenuPause.ajouter_bouton(vec2(0.5, 0.3), vec2(0.2, 0.1), self.retour_menu, "retour au menu")
        self.MenuPause.ajouter_bouton(vec2(0.5, 0.5), vec2(0.2, 0.1), self.reprendre_jeu, "reprendre")


        self.joueur:list[monde.joueur] = []
        self.editeur = None


        
        
        
        
        self.MenuPrincipal:Menu =Menu(
            "menu principal",
            "fichier_jeux/menus/image de fond.jpg",
            "fichier_jeux/menus/logo.png",
        )
        self.MenuPrincipal.dim_logo = vec2(0.3, 0.27)
        self.MenuPrincipal.ajouter_bouton(vec2(0.5, 0.43), vec2(0.2, 0.1), self.lancer_jeu, "jouer")
        self.MenuPrincipal.ajouter_bouton(vec2(0.5, 0.57), vec2(0.2, 0.1), self.ouvrir_sauvegardes_depuis_menu, "sauvegardes")
        self.MenuPrincipal.ajouter_bouton(vec2(0.5, 0.85), vec2(0.2, 0.1), self.ouvrir_editeur_niveau, "editeur de niveau")
        self.MenuPrincipal.ajouter_bouton(vec2(0.5, 0.7), vec2(0.2, 0.1), self.fermer_jeu, "quitter")





        self.saut_temp = None
    #partie plublic de l'app
    def run(self) -> None:
        options = filesytem.charger_options()
        fenetre = options["fenetre"]
        self.distance_max = options["VMAX"]
        self.pas = options["PAS"]
        self.initialiser_menus_sauvegarde()
        graphisme.ouvrir_fenetre(largeur=fenetre["largeur"], hauteur=fenetre["hauteur"])
        filesytem.peupler_sauvegardes()
        
        self.mainloop()
        graphisme.fermer()
        logging.info("Boucle principale terminée.")

        return













    #partie privée de l'app
     




    def ouvrir_editeur_niveau(self,nom,nouveau_niveau:bool = False):
        """permetera ouvri l'editeur

        Args:
            nouveau_niveau (bool, optional): _description_. Defaults to True.
            
        """
        nv = monde.niveau(nom) if nouveau_niveau else self.level_actuel 
        self.editeur= editeur_niveau.EditeurNiveau(nom,nv)
        logging.info("Ouverture de l'éditeur de niveau")
        
        
    

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
        


    def initialiser_menus_sauvegarde(self):
        self.menusaugarde: Menu = Menu("menuspause", "fichier_jeux/menus/image de fond.png")
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
            self.menusaugarde.ajouter_bouton(vec2(0.5, y),vec2(0.08,0.05),action,f"sauvegarde : {key}")
            index += 1

    

        self.menusaugarde.ajouter_bouton(vec2(0.05,0.17),vec2(0.08,0.05),self.retour_menu,"quitter")

        return self.menusaugarde
    

    def afficher_jeu(self):
        self.level_actuel.afficher_fond()
        self.level_actuel.avant.afficher()
        self.level_actuel.afficher_decor()
        self.level_actuel.afficher_terrain()
        self.level_actuel.devant.afficher()
        self.level_actuel.afficher_devant()
        if self.joueur_actuel:
            self.joueur_actuel.afficher()

    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement:graphisme.evenement | None = None

        solution_nv ={
            self.level_actuel.name: {
                "stupide":None,
                "algoA*": None
            }
        }
        choix_algo= ["algoA","stupe"]

        
       
        while self.en_cours and not graphisme.shouldclose(evenement):
            sv_pos_joueur = self.joueur_actuel.position if self.joueur_actuel else None
            pos_clique_gauche = None
            evenement = graphisme.get_evenement()
        
            firstframe = time.time_ns()
            graphisme.effacerTout()

            match self.etat:
                case "menu":
                    self.MenuPrincipal.afficher()
                    for bouton in self.MenuPrincipal.bouton:
                        bouton.action(evenement)
                case "jeu":
                    
                    self.afficher_jeu()
                    if evenement.type == "ClicGauche" and self.joueur_actuel.vistesse == vec2(0,0): # type: ignore
                        temp =graphisme.get_clic_gauche(evenement)
                        j =temp -self.joueur_actuel.position # type: ignore
                        if vect.norme(j) > self.distance_max:
                            j = self.distance_max
                        pos_clique_gauche = j
                    if evenement.type == "clicDroit" and self.joueur_actuel.vistesse: # type: ignore
                        self.joueur_actuel.vistesse = pos_clique_gauche # type: ignore


                    physique.update_physique(self.level_actuel, self.pas, self.joueur_actuel)  # type: ignore

                case "pause":
                    menu.afficher() # type: ignore
                    for bouton in menu.bouton: # type: ignore
                        bouton.action(evenement)
                case "solveur":
                    cin = int(input('choisir algo: 1 algo a 2 stupide'))
                    
                    

                    if solution_nv[self.level_actuel.name].get(choix_algo[cin]) is None:
                        c = solveur.algoA(self.level_actuel)
                        solution_nv[self.level_actuel.name][choix_algo[cin]] = c if c is not None else False #type ignore
                    elif not  solution_nv[self.level_actuel.name][choix_algo[cin]]: 
                        a=graphisme.creer_texte(vec2(0.5,0.5),26,"pas de solution")
                        time.sleep(0.5)
                        graphisme.supprimer_el(a)
                    else:
                        solution_nv[self.level_actuel.name].get(choix_algo[cin])
                        self.joueur
                        



                    
                        
                    


                    pass
                case "menus_sauvegarde":
                    menu = self.initialiser_menus_sauvegarde()
                    menu.afficher()
                    for bouton in menu.bouton:
                        bouton.action(evenement)
                case "editeur_niveau":
                    def bj():
                        nom = str(input("nom du niveau"))
                        creer_niveau = bool(input("voulez vous creer un nouveau niveau"))
                        self.ouvrir_editeur_niveau(nom,creer_niveau)

                    pass
                case _:
                    logging.warning(f"État inconnu : {self.etat}")
                    raise ValueError(f"État inconnu : {self.etat}")

            graphisme.swapbuffer()
            if self.lastframe is None:
                self.dt = 0
            else:
                self.dt = (firstframe - self.lastframe)
            self.lastframe = firstframe

import logging
import time
import filesytem
import graphisme
from ecs_game import EcsGame

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
        self.dt = 0.0
        self.lastframe: int | None = None
        self.ecs = EcsGame()

    def run(self):
        options = filesytem.charger_options()
        fenetre = options["fenetre"]
        graphisme.ouvrir_fenetre(largeur=fenetre["largeur"], hauteur=fenetre["hauteur"])
        filesytem.peupler_sauvegardes()

        self.mainloop()
        self.ecs.shutdown()
        graphisme.fermer()
        logging.info("Boucle principale terminée.")

    def mainloop(self):
        logging.info("Démarrage de la boucle principale.")
        evenement: graphisme.evenement | None = None

        while self.en_cours and not graphisme.shouldclose(evenement):
            evenement = graphisme.get_evenement()

            firstframe = time.time_ns()
            graphisme.effacer_tout()

            if self.lastframe is None:
                self.dt = 0.0
            else:
                self.dt = (firstframe - self.lastframe) / NANOSECONDES_PAR_SECONDE

            self.ecs.step(evenement, self.dt)
            self.en_cours = self.ecs.running

            graphisme.swapbuffer()
            self.lastframe = firstframe

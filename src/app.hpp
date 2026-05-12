#pragma once

#include "filesystem.hpp"
#include "graphisme.hpp"
#include "menus.hpp"
#include "monde.hpp"

#include <chrono>
#include <optional>
#include <string>
#include <unordered_map>

enum class EtatApp {
    Menu,
    Jeu,
    Pause,
    Sauvegardes,
    EditeurNiveau
};

class App {
public:
    void run();

private:
    void mainloop();
    void afficher_jeu();

    Menu creer_menu_principal();
    Menu creer_menu_pause();
    void reconstruire_menu_sauvegarde();

    void lancer_jeu();
    void ouvrir_sauvegardes_depuis_menu();
    void fermer_jeu();
    void reprendre_jeu();
    void retour_menu();
    void ouvrir_editeur_niveau();
    void charger_sauvegarde(const std::string& nom);

    Menu* menu_actuel();

    bool en_cours_{true};
    EtatApp etat_{EtatApp::Menu};
    float dt_{0.0f};
    std::optional<std::chrono::steady_clock::time_point> lastframe_{};

    Niveau level_actuel_{};
    std::optional<Joueur> joueur_actuel_{};
    Graphisme graphisme_{};

    Menu menu_principal_{"menu principal", "fichier_jeux/menus/image de fond.jpg", "fichier_jeux/menus/logo.png"};
    Menu menu_pause_{"menu pause", "fichier_jeux/menus/image de fond.jpg"};
    Menu menu_sauvegarde_{"menus sauvegarde", "fichier_jeux/menus/image de fond.png"};

    std::unordered_map<std::string, std::filesystem::path> sauvegardes_{};
};

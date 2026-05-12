#include "app.hpp"

#include <SDL.h>

void App::run() {
    const Options options = charger_options();
    if (!graphisme_.ouvrir_fenetre(false, options.largeur, options.hauteur)) {
        return;
    }

    sauvegardes_ = peupler_sauvegardes();
    menu_principal_ = creer_menu_principal();
    menu_pause_ = creer_menu_pause();
    reconstruire_menu_sauvegarde();

    mainloop();

    graphisme_.fermer();
}

void App::mainloop() {
    using clock = std::chrono::steady_clock;

    while (en_cours_) {
        SDL_Event ev{};
        while (SDL_PollEvent(&ev)) {
            if (ev.type == SDL_QUIT) {
                en_cours_ = false;
            }

            if (Menu* menu = menu_actuel()) {
                menu->gerer_evenement(ev, graphisme_);
            }
        }

        if (Menu* menu = menu_actuel()) {
            menu->mettre_a_jour_hover(graphisme_);
        }

        graphisme_.effacer_tout();

        switch (etat_) {
            case EtatApp::Menu:
                menu_principal_.afficher(graphisme_);
                break;
            case EtatApp::Jeu:
                afficher_jeu();
                break;
            case EtatApp::Pause:
                menu_pause_.afficher(graphisme_);
                break;
            case EtatApp::Sauvegardes:
                menu_sauvegarde_.afficher(graphisme_);
                break;
            case EtatApp::EditeurNiveau:
                ouvrir_editeur_niveau();
                break;
        }

        graphisme_.swapbuffer();

        const auto now = clock::now();
        if (lastframe_) {
            dt_ = std::chrono::duration<float>(now - *lastframe_).count();
        } else {
            dt_ = 0.0f;
        }
        lastframe_ = now;
    }
}

void App::afficher_jeu() {
    level_actuel_.afficher(graphisme_);
    if (joueur_actuel_) {
        joueur_actuel_->afficher(graphisme_);
    }
}

Menu App::creer_menu_principal() {
    Menu menu{"menu principal", "fichier_jeux/menus/image de fond.jpg", "fichier_jeux/menus/logo.png"};
    menu.ajouter_bouton(Vec2{0.5f, 0.43f}, Vec2{0.2f, 0.1f}, [this]() { lancer_jeu(); }, "jouer");
    menu.ajouter_bouton(Vec2{0.5f, 0.57f}, Vec2{0.2f, 0.1f}, [this]() { ouvrir_sauvegardes_depuis_menu(); }, "sauvegardes");
    menu.ajouter_bouton(Vec2{0.5f, 0.85f}, Vec2{0.2f, 0.1f}, [this]() { ouvrir_editeur_niveau(); }, "editeur de niveau");
    menu.ajouter_bouton(Vec2{0.5f, 0.7f}, Vec2{0.2f, 0.1f}, [this]() { fermer_jeu(); }, "quitter");
    return menu;
}

Menu App::creer_menu_pause() {
    Menu menu{"menu pause", "fichier_jeux/menus/image de fond.jpg"};
    menu.ajouter_bouton(Vec2{0.5f, 0.5f}, Vec2{0.2f, 0.1f}, [this]() { reprendre_jeu(); }, "reprendre");
    return menu;
}

void App::reconstruire_menu_sauvegarde() {
    menu_sauvegarde_ = Menu{"menus sauvegarde", "fichier_jeux/menus/image de fond.png"};
    float y = 0.2f;
    for (const auto& [nom, chemin] : sauvegardes_) {
        menu_sauvegarde_.ajouter_bouton(Vec2{0.5f, y}, Vec2{0.08f, 0.05f}, [this, nom]() { charger_sauvegarde(nom); }, nom);
        y += 0.08f;
    }

    menu_sauvegarde_.ajouter_bouton(Vec2{0.05f, 0.17f}, Vec2{0.08f, 0.05f}, [this]() { retour_menu(); }, "quitter");
}

void App::lancer_jeu() {
    etat_ = EtatApp::Jeu;
    if (!joueur_actuel_) {
        joueur_actuel_.emplace(level_actuel_.debut);
    }
}

void App::ouvrir_sauvegardes_depuis_menu() {
    etat_ = EtatApp::Sauvegardes;
    reconstruire_menu_sauvegarde();
}

void App::fermer_jeu() {
    en_cours_ = false;
}

void App::reprendre_jeu() {
    etat_ = EtatApp::Jeu;
}

void App::retour_menu() {
    etat_ = EtatApp::Menu;
}

void App::ouvrir_editeur_niveau() {
    SDL_Log("app : ouverture de l'éditeur de niveau (non implémenté)");
    etat_ = EtatApp::Menu;
}

void App::charger_sauvegarde(const std::string& nom) {
    const auto it = sauvegardes_.find(nom);
    if (it == sauvegardes_.end()) {
        return;
    }

    level_actuel_ = charger_niveau(it->second);
    joueur_actuel_.emplace(level_actuel_.debut);
    etat_ = EtatApp::Jeu;
}

Menu* App::menu_actuel() {
    switch (etat_) {
        case EtatApp::Menu:
            return &menu_principal_;
        case EtatApp::Pause:
            return &menu_pause_;
        case EtatApp::Sauvegardes:
            return &menu_sauvegarde_;
        default:
            return nullptr;
    }
}

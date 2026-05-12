#include "menus.hpp"

Bouton::Bouton(Vec2 pos, Vec2 dim, std::string texte, std::function<void()> action)
    : pos_(pos), dim_(dim), texte_(std::move(texte)), action_(std::move(action)) {}

void Bouton::afficher(Graphisme& graphisme) {
    const SDL_Color couleur = hover_ ? couleur_hover_ : couleur_;
    graphisme.dessiner_rect(pos_, dim_, couleur, true);
}

void Bouton::gerer_evenement(const SDL_Event& ev, const Graphisme& graphisme) {
    if (!actif_) {
        return;
    }

    if (ev.type == SDL_MOUSEBUTTONDOWN && ev.button.button == SDL_BUTTON_LEFT) {
        if (contient_point(ev.button.x, ev.button.y, graphisme)) {
            if (action_) {
                action_();
            }
        }
    }
}

void Bouton::mettre_a_jour_hover(const Graphisme& graphisme) {
    int x = 0;
    int y = 0;
    SDL_GetMouseState(&x, &y);
    hover_ = contient_point(x, y, graphisme);
}

bool Bouton::contient_point(int x, int y, const Graphisme& graphisme) const {
    const SDL_FRect rect = graphisme.rect_pixels(pos_, dim_);
    return x >= rect.x && x < rect.x + rect.w && y >= rect.y && y < rect.y + rect.h;
}

Menu::Menu(std::string name, std::string fond, std::optional<std::string> logo)
    : name_(std::move(name)), fond_(std::move(fond)), logo_(std::move(logo)) {}

void Menu::ajouter_bouton(Vec2 pos, Vec2 dim, std::function<void()> action, const std::string& texte) {
    boutons_.emplace_back(pos, dim, texte, std::move(action));
}

void Menu::afficher(Graphisme& graphisme) {
    if (!fond_.empty()) {
        graphisme.afficher_fond(fond_);
    }

    if (logo_) {
        const Sprite logo_sprite{pos_logo_, *logo_, dim_logo_};
        graphisme.afficher_sprite(logo_sprite);
    }

    for (auto& bouton : boutons_) {
        bouton.afficher(graphisme);
    }
}

void Menu::gerer_evenement(const SDL_Event& ev, const Graphisme& graphisme) {
    for (auto& bouton : boutons_) {
        bouton.gerer_evenement(ev, graphisme);
    }
}

void Menu::mettre_a_jour_hover(const Graphisme& graphisme) {
    for (auto& bouton : boutons_) {
        bouton.mettre_a_jour_hover(graphisme);
    }
}

void Menu::vider() {
    boutons_.clear();
}

#pragma once

#include "graphisme.hpp"
#include "vect.hpp"

#include <functional>
#include <optional>
#include <string>
#include <vector>

class Bouton {
public:
    Bouton(Vec2 pos, Vec2 dim, std::string texte, std::function<void()> action);

    void afficher(Graphisme& graphisme);
    void gerer_evenement(const SDL_Event& ev, const Graphisme& graphisme);
    void mettre_a_jour_hover(const Graphisme& graphisme);

private:
    bool contient_point(int x, int y, const Graphisme& graphisme) const;

    Vec2 pos_{};
    Vec2 dim_{};
    std::string texte_{};
    std::function<void()> action_{};
    SDL_Color couleur_{0, 120, 255, 255};
    SDL_Color couleur_hover_{130, 200, 255, 255};
    bool actif_{true};
    bool hover_{false};
};

class Menu {
public:
    Menu(std::string name, std::string fond, std::optional<std::string> logo = std::nullopt);

    void ajouter_bouton(Vec2 pos, Vec2 dim, std::function<void()> action, const std::string& texte);
    void afficher(Graphisme& graphisme);
    void gerer_evenement(const SDL_Event& ev, const Graphisme& graphisme);
    void mettre_a_jour_hover(const Graphisme& graphisme);
    void vider();

private:
    std::string name_{};
    std::vector<Bouton> boutons_{};
    std::string fond_{};
    std::optional<std::string> logo_{};
    Vec2 pos_logo_{0.5f, 0.12f};
    Vec2 dim_logo_{0.1f, 0.09f};
};

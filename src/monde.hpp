#pragma once

#include "graphisme.hpp"
#include "place_holder.hpp"
#include "vect.hpp"

#include <string>
#include <vector>

class Grille {
public:
    explicit Grille(float taille_tuile = 0.0f);

    void ajouter_tuile(const Tuile& tuile);
    void afficher(Graphisme& graphisme) const;

private:
    float taille_tuile_{0.0f};
    std::vector<Tuile> tuiles_{};
};

class Joueur {
public:
    explicit Joueur(const Vec2& pos);

    void afficher(Graphisme& graphisme) const;

    Vec2 position() const;
    void set_position(const Vec2& pos);

private:
    Sprite sprite_{};
    Vec2 vitesse_{};
    float poids_{12.0f};
    Vec2 direction_{};
    bool bouger_{true};
};

class Niveau {
public:
    Niveau();

    void afficher(Graphisme& graphisme) const;
    void afficher_fond(Graphisme& graphisme) const;
    void afficher_decor(Graphisme& graphisme) const;
    void afficher_terrain(Graphisme& graphisme) const;
    void afficher_devant(Graphisme& graphisme) const;

    Vec2 debut{0.06f, 0.9f};
    Vec2 point_fin{0.94f, 0.9f};
    std::string fond{};
    Grille avant{32.0f};
    Grille decor{16.0f};
    Grille terrain{16.0f};
    Grille objet{8.0f};
    std::vector<Sprite> devant{};
};

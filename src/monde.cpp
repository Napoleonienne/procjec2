#include "monde.hpp"

Grille::Grille(float taille_tuile) : taille_tuile_(taille_tuile) {}

void Grille::ajouter_tuile(const Tuile& tuile) {
    tuiles_.push_back(tuile);
}

void Grille::afficher(Graphisme& graphisme) const {
    for (const auto& tuile : tuiles_) {
        graphisme.afficher(tuile);
    }
}

Joueur::Joueur(const Vec2& pos) {
    const std::string texture = chemin_absolue("fichier_jeux/joueur/mouton.png").string();
    sprite_ = Sprite{pos, texture, Vec2{0.06f, 0.1f}};
}

void Joueur::afficher(Graphisme& graphisme) const {
    graphisme.afficher_sprite(sprite_);
}

Vec2 Joueur::position() const {
    return sprite_.pos;
}

void Joueur::set_position(const Vec2& pos) {
    sprite_.pos = pos;
}

Niveau::Niveau() = default;

void Niveau::afficher(Graphisme& graphisme) const {
    afficher_fond(graphisme);
    avant.afficher(graphisme);
    afficher_decor(graphisme);
    afficher_terrain(graphisme);
    objet.afficher(graphisme);
    afficher_devant(graphisme);
}

void Niveau::afficher_fond(Graphisme& graphisme) const {
    graphisme.afficher_fond(fond);
}

void Niveau::afficher_decor(Graphisme& graphisme) const {
    decor.afficher(graphisme);
}

void Niveau::afficher_terrain(Graphisme& graphisme) const {
    terrain.afficher(graphisme);
}

void Niveau::afficher_devant(Graphisme& graphisme) const {
    for (const auto& sprite : devant) {
        graphisme.afficher_sprite(sprite);
    }
}

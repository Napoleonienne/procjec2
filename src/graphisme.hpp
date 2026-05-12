#pragma once

#include "place_holder.hpp"
#include "vect.hpp"

#include <SDL.h>
#include <SDL_image.h>

#include <filesystem>
#include <string>
#include <unordered_map>

constexpr int HAUTEUR_BASE = 600;
constexpr int LARGEUR_BASE = 1067;

std::filesystem::path chemin_absolue(std::string_view relative_path);

class Graphisme {
public:
    bool ouvrir_fenetre(bool repere = false, int largeur = 0, int hauteur = 0);
    void fermer();

    void definir_fenetre(int largeur, int hauteur);

    void effacer_tout();
    void swapbuffer();

    Vec2 vers_pixels(const Vec2& vec) const;
    Vec2 vers_coordonnees(const Vec2& vec) const;
    float valeur_pixels(float val) const;
    SDL_FRect rect_pixels(const Vec2& pos, const Vec2& dim) const;

    void afficher_fond(const std::string& path);
    void afficher(const Object2d& objet);
    void afficher_sprite(const Sprite& sprite);
    void dessiner_rect(const Vec2& pos, const Vec2& dim, SDL_Color couleur, bool rempli = true);

    SDL_Renderer* renderer() const;
    int largeur() const;
    int hauteur() const;

private:
    SDL_Texture* charger_texture(const std::string& path);

    std::unordered_map<std::string, SDL_Texture*> textures_{};
    SDL_Window* window_{nullptr};
    SDL_Renderer* renderer_{nullptr};
    int fenetre_largeur_{LARGEUR_BASE};
    int fenetre_hauteur_{HAUTEUR_BASE};
};

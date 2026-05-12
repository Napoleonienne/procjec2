#pragma once

#include "vect.hpp"

#include <string>
#include <unordered_map>

struct Object2d {
    Vec2 pos{};
    Vec2 taille{};
    std::string texture{};
    std::unordered_map<std::string, bool> property{};

    Object2d() = default;

    Object2d(Vec2 pos_val, std::string texture_val, Vec2 taille_val)
        : pos(pos_val), taille(taille_val), texture(std::move(texture_val)) {}

    Vec2 coin_haut_gauche() const {
        return pos - (taille / 2.0f);
    }

    Vec2 coin_bas_droit() const {
        return pos + (taille / 2.0f);
    }
};

struct Sprite : public Object2d {
    Sprite() = default;

    Sprite(Vec2 pos_val, std::string texture_val, Vec2 taille_val)
        : Object2d(pos_val, std::move(texture_val), taille_val) {}
};

struct Tuile : public Object2d {
    Tuile() = default;

    Tuile(Vec2 pos_val, std::string texture_val, float taille_val)
        : Object2d(pos_val, std::move(texture_val), Vec2{taille_val, taille_val}) {
        property = {
            {"solide", false},
            {"rebondissante", false},
            {"glissante", false},
            {"amortissante", false},
            {"mortelle", false}
        };
    }
};

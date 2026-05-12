#include "graphisme.hpp"

#include <algorithm>
#include <utility>

std::filesystem::path chemin_absolue(std::string_view relative_path) {
    std::filesystem::path relative{relative_path};
    std::filesystem::path cwd = std::filesystem::current_path();

    std::filesystem::path candidate = cwd / relative;
    if (std::filesystem::exists(candidate)) {
        return candidate;
    }

    candidate = cwd.parent_path() / relative;
    if (std::filesystem::exists(candidate)) {
        return candidate;
    }

    return relative;
}

bool Graphisme::ouvrir_fenetre(bool repere, int largeur, int hauteur) {
    (void)repere;
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
        SDL_Log("graphisme : SDL_Init a échoué : %s", SDL_GetError());
        return false;
    }

    const int flags = IMG_INIT_PNG | IMG_INIT_JPG;
    if ((IMG_Init(flags) & flags) != flags) {
        SDL_Log("graphisme : IMG_Init a échoué : %s", IMG_GetError());
        SDL_Quit();
        return false;
    }

    definir_fenetre(largeur, hauteur);

    window_ = SDL_CreateWindow(
        "saute_mouton",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        fenetre_largeur_,
        fenetre_hauteur_,
        SDL_WINDOW_SHOWN
    );

    if (!window_) {
        SDL_Log("graphisme : SDL_CreateWindow a échoué : %s", SDL_GetError());
        IMG_Quit();
        SDL_Quit();
        return false;
    }

    renderer_ = SDL_CreateRenderer(window_, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (!renderer_) {
        SDL_Log("graphisme : SDL_CreateRenderer a échoué : %s", SDL_GetError());
        SDL_DestroyWindow(window_);
        window_ = nullptr;
        IMG_Quit();
        SDL_Quit();
        return false;
    }

    return true;
}

void Graphisme::fermer() {
    for (auto& [key, texture] : textures_) {
        if (texture) {
            SDL_DestroyTexture(texture);
        }
    }
    textures_.clear();

    if (renderer_) {
        SDL_DestroyRenderer(renderer_);
        renderer_ = nullptr;
    }

    if (window_) {
        SDL_DestroyWindow(window_);
        window_ = nullptr;
    }

    IMG_Quit();
    SDL_Quit();
}

void Graphisme::definir_fenetre(int largeur, int hauteur) {
    if (largeur > 0) {
        fenetre_largeur_ = largeur;
    }
    if (hauteur > 0) {
        fenetre_hauteur_ = hauteur;
    }
}

void Graphisme::effacer_tout() {
    if (!renderer_) {
        return;
    }
    SDL_SetRenderDrawColor(renderer_, 0, 0, 0, 255);
    SDL_RenderClear(renderer_);
}

void Graphisme::swapbuffer() {
    if (renderer_) {
        SDL_RenderPresent(renderer_);
    }
}

Vec2 Graphisme::vers_pixels(const Vec2& vec) const {
    return Vec2{vec.x * static_cast<float>(fenetre_largeur_), vec.y * static_cast<float>(fenetre_hauteur_)};
}

Vec2 Graphisme::vers_coordonnees(const Vec2& vec) const {
    return Vec2{vec.x / static_cast<float>(fenetre_largeur_), vec.y / static_cast<float>(fenetre_hauteur_)};
}

float Graphisme::valeur_pixels(float val) const {
    return val * static_cast<float>(std::min(fenetre_largeur_, fenetre_hauteur_));
}

SDL_FRect Graphisme::rect_pixels(const Vec2& pos, const Vec2& dim) const {
    const Vec2 pos_pixels = vers_pixels(pos);
    const Vec2 taille_pixels = vers_pixels(dim);
    return SDL_FRect{
        pos_pixels.x - taille_pixels.x / 2.0f,
        pos_pixels.y - taille_pixels.y / 2.0f,
        taille_pixels.x,
        taille_pixels.y
    };
}

void Graphisme::afficher_fond(const std::string& path) {
    if (path.empty()) {
        return;
    }
    const Sprite fond{Vec2{0.5f, 0.5f}, path, Vec2{1.0f, 1.0f}};
    afficher_sprite(fond);
}

void Graphisme::afficher(const Object2d& objet) {
    const Sprite sprite{objet.pos, objet.texture, objet.taille};
    afficher_sprite(sprite);
}

void Graphisme::afficher_sprite(const Sprite& sprite) {
    if (!renderer_) {
        return;
    }

    if (sprite.texture.empty()) {
        return;
    }

    SDL_Texture* texture = charger_texture(sprite.texture);
    if (!texture) {
        return;
    }

    const SDL_FRect rect = rect_pixels(sprite.pos, sprite.taille);
    SDL_RenderCopyF(renderer_, texture, nullptr, &rect);
}

void Graphisme::dessiner_rect(const Vec2& pos, const Vec2& dim, SDL_Color couleur, bool rempli) {
    if (!renderer_) {
        return;
    }

    const SDL_FRect rect = rect_pixels(pos, dim);
    SDL_SetRenderDrawColor(renderer_, couleur.r, couleur.g, couleur.b, couleur.a);

    if (rempli) {
        SDL_RenderFillRectF(renderer_, &rect);
    } else {
        SDL_RenderDrawRectF(renderer_, &rect);
    }
}

SDL_Renderer* Graphisme::renderer() const {
    return renderer_;
}

int Graphisme::largeur() const {
    return fenetre_largeur_;
}

int Graphisme::hauteur() const {
    return fenetre_hauteur_;
}

SDL_Texture* Graphisme::charger_texture(const std::string& path) {
    const std::filesystem::path full_path = chemin_absolue(path);
    const std::string key = full_path.string();

    const auto it = textures_.find(key);
    if (it != textures_.end()) {
        return it->second;
    }

    SDL_Surface* surface = IMG_Load(key.c_str());
    if (!surface) {
        SDL_Log("graphisme : IMG_Load a échoué pour %s : %s", key.c_str(), IMG_GetError());
        return nullptr;
    }

    SDL_Texture* texture = SDL_CreateTextureFromSurface(renderer_, surface);
    SDL_FreeSurface(surface);

    if (!texture) {
        SDL_Log("graphisme : SDL_CreateTextureFromSurface a échoué : %s", SDL_GetError());
        return nullptr;
    }

    textures_.emplace(key, texture);
    return texture;
}

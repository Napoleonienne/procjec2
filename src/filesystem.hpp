#pragma once

#include "monde.hpp"

#include <filesystem>
#include <string>
#include <unordered_map>

struct Options {
    int largeur{LARGEUR_BASE};
    int hauteur{HAUTEUR_BASE};
};

std::filesystem::path dossier_sauvegarde();

Options charger_options();

std::unordered_map<std::string, std::filesystem::path> peupler_sauvegardes();

Niveau charger_niveau(const std::filesystem::path& chemin);

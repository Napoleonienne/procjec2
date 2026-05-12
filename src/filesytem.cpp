#include "filesytem.hpp"

#include "graphisme.hpp"

#include <cstdlib>
#include <fstream>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

std::filesystem::path dossier_sauvegarde() {
    const char* home = std::getenv("HOME");
    std::filesystem::path base_path = home ? std::filesystem::path(home) : std::filesystem::current_path();
    std::filesystem::path chemin = base_path / ".saute_mouton" / "save";
    std::filesystem::create_directories(chemin);
    return chemin;
}

Options charger_options() {
    Options options{};
    const std::filesystem::path options_path = chemin_absolue("fichier_jeux/option jeux/option.json");

    std::ifstream fichier(options_path);
    if (!fichier.is_open()) {
        SDL_Log("filesystem : impossible d'ouvrir %s", options_path.string().c_str());
        return options;
    }

    json data;
    try {
        fichier >> data;
        if (data.contains("fenetre") && data["fenetre"].is_object()) {
            const auto& fenetre = data["fenetre"];
            options.largeur = fenetre.value("largeur", options.largeur);
            options.hauteur = fenetre.value("hauteur", options.hauteur);
        }
    } catch (const json::exception& exc) {
        SDL_Log("filesystem : erreur JSON %s", exc.what());
    }

    return options;
}

std::unordered_map<std::string, std::filesystem::path> peupler_sauvegardes() {
    std::unordered_map<std::string, std::filesystem::path> sauvegardes;
    const std::filesystem::path chemin = dossier_sauvegarde();

    if (!std::filesystem::exists(chemin)) {
        return sauvegardes;
    }

    for (const auto& entry : std::filesystem::directory_iterator(chemin)) {
        if (!entry.is_regular_file()) {
            continue;
        }
        if (entry.path().extension() == ".json") {
            sauvegardes.emplace(entry.path().stem().string(), entry.path());
        }
    }

    return sauvegardes;
}

static void charger_grille(const json& donne_niveau, const std::string& tranche, Grille& grille) {
    if (!donne_niveau.contains(tranche)) {
        return;
    }

    const auto& tranche_json = donne_niveau.at(tranche);
    if (!tranche_json.is_object()) {
        return;
    }

    for (const auto& [cle, tuile_data] : tranche_json.items()) {
        if (!tuile_data.is_object()) {
            continue;
        }

        const auto& pos_data = tuile_data.at("pos");
        Vec2 pos{pos_data.value("x", 0.0f), pos_data.value("y", 0.0f)};

        float taille = 0.0f;
        if (tuile_data.contains("taille")) {
            const auto& taille_data = tuile_data.at("taille");
            if (taille_data.is_object()) {
                taille = taille_data.value("x", 0.0f);
            } else if (taille_data.is_number()) {
                taille = taille_data.get<float>();
            }
        }

        std::string texture = tuile_data.value("texture", "");
        Tuile tuile{pos, texture, taille};
        if (tuile_data.contains("property") && tuile_data["property"].is_object()) {
            for (const auto& [nom, valeur] : tuile_data["property"].items()) {
                if (valeur.is_boolean()) {
                    tuile.property[nom] = valeur.get<bool>();
                }
            }
        }

        grille.ajouter_tuile(tuile);
    }
}

Niveau charger_niveau(const std::filesystem::path& chemin) {
    Niveau niveau_charger;

    std::ifstream fichier(chemin);
    if (!fichier.is_open()) {
        SDL_Log("filesystem : impossible de lire %s", chemin.string().c_str());
        return niveau_charger;
    }

    json data;
    try {
        fichier >> data;
    } catch (const json::exception& exc) {
        SDL_Log("filesystem : erreur JSON %s", exc.what());
        return niveau_charger;
    }

    if (data.contains("debut")) {
        const auto& debut = data.at("debut");
        niveau_charger.debut = Vec2{debut.value("x", niveau_charger.debut.x), debut.value("y", niveau_charger.debut.y)};
    }

    if (data.contains("point_fin")) {
        const auto& fin = data.at("point_fin");
        niveau_charger.point_fin = Vec2{fin.value("x", niveau_charger.point_fin.x), fin.value("y", niveau_charger.point_fin.y)};
    }

    niveau_charger.fond = data.value("fond", "");

    charger_grille(data, "avant", niveau_charger.avant);
    charger_grille(data, "decor", niveau_charger.decor);
    charger_grille(data, "terrain", niveau_charger.terrain);
    charger_grille(data, "objet", niveau_charger.objet);

    if (data.contains("devant") && data["devant"].is_array()) {
        for (const auto& sprite_data : data["devant"]) {
            if (!sprite_data.is_object()) {
                continue;
            }
            const auto& pos_data = sprite_data.at("pos");
            const auto& taille_data = sprite_data.at("taille");
            Vec2 pos{pos_data.value("x", 0.0f), pos_data.value("y", 0.0f)};
            Vec2 taille{taille_data.value("x", 0.0f), taille_data.value("y", 0.0f)};
            std::string texture = sprite_data.value("texture", "");
            niveau_charger.devant.emplace_back(pos, texture, taille);
        }
    }

    return niveau_charger;
}

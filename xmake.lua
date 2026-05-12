set_project("saute_mouton")
set_version("0.1.0")
set_languages("c++23")

add_rules("mode.debug", "mode.release")

add_requires("sdl2", "sdl2_image", "nlohmann_json")

target("saute_mouton")
    set_kind("binary")
    add_files("src/*.cpp")
    add_includedirs("src")
    add_packages("sdl2", "sdl2_image", "nlohmann_json")
    add_defines("SDL_MAIN_HANDLED")

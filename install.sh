#pour créer un executable
#sudo chmod +x NomProg est imperative pour autoriser le programme sur linux il faut les droits admin

SCRIPT_DIR="$( cd "$( dirname "$0" )" && pwd )"
cd "$SCRIPT_DIR"
VENV_NAME=".env_saute_mouton"
EXE_NAME="saute_mouton"

echo Démarrage de la compilation dans le repertoire : $SCRIPT_DIR


if [ -d build ]; then
    echo "Suppression du dossier build..."
    rm -r build
fi
if [ -d dist ]; then
    echo "Suppression du dossier dist..."
    rm -r dist
fi

if [ ! -d "$VENV_NAME" ]; then
    echo "Création de l'environnement virtuel $VENV_NAME..."
    python3 -m venv "$VENV_NAME"
fi
if [ -d PickTok.spec]; then
    echo "Suppression du fichier PickTok.spec..."
    rm PickTok.spec
fi




echo "Activation de l'environnement virtuel..."
source "$VENV_NAME/bin/activate"


pip install --upgrade pip


pip install nava PyInstaller pillow 




pyinstaller --onefile --noconsole \
    --name "$EXE_NAME" \
        app.py \
    --add-data "asset:asset" \
    --hidden-import nava \
    --hidden-import tkinter\
    --hidden-import PIL.ImageTk \
    --hidden-import PIL._tkinter_finder \
    --icon=icone.ico

echo "Désactivation de l'environnement virtuel..."
deactivate
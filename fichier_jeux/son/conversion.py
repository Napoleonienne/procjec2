import subprocess
from pathlib import Path



ch = Path("/home/guy/Bureau/procjec2/fichier_jeux/son")




for file in ch.glob(pattern="*.mp3"):
    print(file.suffix)

    if file.suffix in [".wav",".py"]:

        continue
    try:
        subprocess.run(["ffmpeg", "-i", str(file),"-map", "a:0", "-ac", "2", str(ch / (file.stem + ".wav"))])   
    except Exception as e:
        print(f"Erreur lors de la conversion de {file}: {e}")






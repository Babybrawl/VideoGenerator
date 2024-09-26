import os
import subprocess

# Dossier à vérifier
to_upload_folder = r"D:\test400\to_upload"

def check_and_run():
    # Vérifier si le dossier 'to_upload' contient des fichiers
    if any(os.path.isfile(os.path.join(to_upload_folder, f)) for f in os.listdir(to_upload_folder)):
        print("Des fichiers trouvés dans le dossier 'to_upload'. Lancement de run2.py...")
        try:
            subprocess.run(["python", "d:/test400/run2.py"], check=True)
            print("run2.py a été exécuté avec succès.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de run2.py: {e}")
    else:
        print("Aucun fichier trouvé dans le dossier 'to_upload'.")

# Exécution
check_and_run()

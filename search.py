import os
import fnmatch
import subprocess

def trouver_fichiers_tex(repertoire):
    """
    Cherche tous les fichiers .tex dans un répertoire donné.

    Args:
    repertoire (str): Le chemin du répertoire à parcourir.

    Returns:
    list: Une liste des chemins des fichiers .tex trouvés.
    """
    fichiers_tex = []

    # Parcourir tous les fichiers et dossiers dans le répertoire donné
    for root, dirnames, filenames in os.walk(repertoire):
        # Chercher tous les fichiers qui correspondent au motif '*.tex'
        for filename in fnmatch.filter(filenames, '*.tex'):
            if filename.lower() == "qcm.tex": continue
            # Ajouter le chemin complet du fichier .tex à la liste
            fichiers_tex.append(os.path.join(root, filename))

    return fichiers_tex

# Exemple d'utilisation
repertoire = '.'  # Répertoire courant
fichiers_tex = trouver_fichiers_tex(repertoire)
print(f"Fichiers .tex trouvés dans {repertoire} :")
for fichier in fichiers_tex:
    print(fichier.split("/")[1])
    try:
        result = subprocess.run("python3 render.py "+fichier + " ./"+fichier.split("/")[1]+"/", shell=True, check=True, text=True, capture_output=True)
        print(result.returncode, result.stdout, result.stderr)
    except subprocess.CalledProcessError as e:
        print(e.returncode, e.stdout, e.stderr)
print(fichiers_tex)
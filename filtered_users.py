import json
from datetime import datetime
import os

def load_users(filepath):
    """
    Fonction permettant de charger les données utilisateurs à partir d'un fichier

    Args:
        filepath: chemin vers le fichier duquel extraire les données utilisateurs

    Returns:
        users: liste de dictionnaires contenant les infos utilisateurs
    """

    with open(filepath, "r", encoding="utf-8") as f:
        users = json.load(f)    
    print(f"🔍 Nombre d'utilisateurs chargés : {len(users)}")
    return users



def remove_duplicates(users):
    """
    Fonction permettant de supprimer tous les doublons dans les utilisateurs
    en vérifiant l'ID

    Args:
        users (list): liste de dictionnaires contenant les infos utilisateur

    Returns:
        liste de dictionnaires filtrée
    """

    unique_users = {}
    for user in users:
        unique_users[user["id"]] = user
    print(f"♻️ Doublons supprimés : {len(users) - len(unique_users)}")
    return list(unique_users.values())



def filter_users(users):
    """
    Fonction fitrant les utilisateurs pour ne garder que ceux dont :
    - la bio n'est pas nulle
    - l'avatar n'est pas nul
    - le compte a été créé à partir de 2015

    Args:
        users (list): liste de dictionnaires contenant les infos utilisateur

    Returns:
        liste de dictionnaires filtrée
    """

    filtered = []
    for user in users:
        bio = user.get("bio")
        avatar_url = user.get("avatar_url")
        created_at_str = user.get("created_at")

        # Vérification bio
        if not bio or bio.strip() == "":
            continue

        # Vérification avatar
        if not avatar_url or avatar_url.strip() == "":
            continue

        # Vérification date de création
        # On ne garde que ceux créés à partir de 2015
        # En théorie notre BDD users.json ne contient déjà que des comptes de 2015 et + (voir extract_users.py)
        try:
            created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
            if created_at < datetime(2015, 1, 1):
                continue
        except Exception as e:
            continue

        filtered.append({
            "login": user["login"],
            "id": user["id"],
            "created_at": user["created_at"],
            "avatar_url": user["avatar_url"],
            "bio": user["bio"]
        })

    print(f"✅ Utilisateurs filtrés : {len(filtered)}")
    return filtered



def save_filtered_users(users, output_path):
    """
    Fonction enregistrant une liste d'utilisateurs dans un fichier

    Args:
        users (list): liste de dictionnaires contenant les infos utilisateur
        output_path (str): lien vers le fichier où enregistrer les informations
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    print(f"✅ {len(users)} utilisateurs sauvegardés dans {output_path}")



def main():
    """
    Porte d'entrée du script.
    - charge la liste d'utilisateurs avec load_users()
    - supprime les doublons avec remove_duplicates()
    - filtre les données avec filter_users()
    - enregistre les informations dans un fichier avec save_filtered_users()
    """

    input_path = "data/users.json"
    output_path = "data/filtered_users.json"

    users = load_users(input_path)
    users = remove_duplicates(users)
    users = filter_users(users)
    save_filtered_users(users, output_path=output_path)



if __name__ == "__main__":
    main()
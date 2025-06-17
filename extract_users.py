from dotenv import load_dotenv
import os
import requests
import time
import json
import argparse


def load_token():
    """ 
    Fonction permettant de charger le token depuis le fichier .env
    et de retourner le contenu du headers

    """

    load_dotenv()
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("⚠️ Absence du token GitHub")
    return {"Authorization": f"token {token}"}



def check_quota(response):
    """
    Vérification et gestion des quotas de l'API GitHub.
    Si le quota est atteint, le script se met en pause jusqu'à la réinitialiation.
    """

    remaining_time = int(response.headers.get("X-RateLimit-Remaining", 0))
    reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

    if remaining_time == 0:
        wait_time = reset_time - int(time.time()) + 5
        print(f"Quota de requêtes dépassé, temps d'attente avant de continuer : {wait_time} secondes")
        time.sleep(wait_time)



def get_user_info(headers: dict, user: dict) -> dict:
    """
    Récupère les info d'un utilisateur par son login.

    Args:
        headers (dict): En-tête contenant le token d'authentification
        user (dict): Un dictionnaire contenant au minimum "login" et "id".

    Returns:
        dict: Un dictionnaire avec login, id, avatar_url, created_at, bio.
    """

    login = user["login"]
    detailed_url = f"https://api.github.com/users/{login}"

    try:
        detail_response = requests.get(detailed_url, headers=headers)

        check_quota(detail_response)    # On appelle la fonction check_quota pour vérifier que le quota de requêtes n'est pas atteint
        
        if detail_response.status_code != 200:
            print(f"⚠️ Erreur lors de la récupération de {login}: {detail_response.status_code}")
            return None
        
        details = detail_response.json()

        return {
            "login": user["login"],
            "id": user["id"],
            "avatar_url": details.get("avatar_url"),
            "created_at": details.get("created_at"),
            "bio": details.get("bio")
        }
    
    except requests.RequestException as e:
        print(f"❌ Exception réseau pour {login}: {e}")
        return None



def fetch_users(max_users: int, headers: dict) -> list:
    """ Fonction permettant de récupérer les infos d'un nombre max d'utilisateurs
    avec vérification du quota

    Args:
        max_users (int): nombre d'users à récupérer
        headers (dict): En-tête contenant le token d'authentification

    Returns:
        list: liste de dictionnaire contenant les informations des utilisateurs
    """

    all_users = []
    since = 10367555    #ID permettant de récupérer uniquement les comptes à partir de 2015 (à partir de 0 -> 2008)

    while len(all_users) < max_users:
        url = f"https://api.github.com/users?since={since}"
        try:
            response = requests.get(url, headers=headers)
            check_quota(response)   # appel de la fonction pour check le quota de requêtes
            if response.status_code != 200:
                print(f"❌ Erreur {response.status_code} lors de la récupération des utilisateurs")
                break

            page_users = response.json()
            if not page_users:
                break

            for user in page_users:
                detailed = get_user_info(headers, user)
                if detailed:
                    all_users.append(detailed)
                if len(all_users) >= max_users :
                    break
                time.sleep(0.2)     # ajout d'une latence pour éviter blocage pour usage abusif

            since = page_users[-1]["id"]

        except Exception as e:
            print(f"🚨 Problème pendant l’extraction : {e}")
            time.sleep(5)   # si il y a un problème réseau ou autre, on attent 5 secondes avant de continuer
            continue

    return all_users    



def save_users(users, output_path="data/users.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    print(f"✅ {len(users)} utilisateurs sauvegardés dans {output_path}")



# EXECUTION PRINCIPALE

def main():
    """
    Point d'entrée du code :
    - crée un parser par ligne de commande avec définition de l'argument --max-users
    - lit les arguments
    - charge le token GitHub avec load_token()
    - extrait les utilisateurs avec fetch_users()
    - Sauvegarde les données dans data/users.json avec save_users()
    """

    parser = argparse.ArgumentParser(description="Extraction d'utilisateurs GiHub")
    parser.add_argument("--max-users", type=int, default=60, help="Nombre max d'utilisateurs à extraire")
    args = parser.parse_args()

    headers = load_token()
    users = fetch_users(max_users=args.max_users, headers=headers)
    save_users(users)



# Exécution de main() à l'exécution de ce fichier
if __name__ == "__main__":
    main()
    
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from api.main import app



# Création d'un client test pour simuler les appels d'API
client = TestClient(app)

# Identifiants valides (doivent être similaires à ceux du .env)
USERNAME = "admin"
PASSWORD = "admin123"

def test_get_users_auth():
    """
    Test de la route GET /users/
    """

    response = client.get("/users/", auth=(USERNAME, PASSWORD)) # envoie de requête GET avec authentification
    assert response.status_code == 200  # vérifie que la requête à réussie : code 200 = OK
    assert isinstance(response.json(), list)    # vérifie que la réponse est bien une liste JSON
    assert "login" in response.json()[0]


def test_get_user_by_login():
    """
    Test de récupération d'un utilisateur en particulier
    """

    login = "MatzeJ"
    response = client.get(f"/users/{login}", auth=(USERNAME, PASSWORD))
    assert response.status_code in [200, 404]   # retourne erreur 404 si l'utilisateur n'existe pas
    if response.status_code == 200:
        assert "login" in response.json()   # si trouvé on vérifie qu'il y a bien un login dans la réponse


def test_search_users():
    """
    Test de la recherche d'utilisateurs par mot-clé
    """

    response = client.get("/users/search?q=ma", auth=(USERNAME, PASSWORD))
    assert response.status_code == 200
    assert isinstance(response.json(), list)    # vérifie que la réponse est OK et renvoie une liste


def test_unauthorized_access():
    """
    Test qu'un accès sans authentification échoue
    """

    response = client.get("/users/")
    assert response.status_code == 401  # sans identifiant on attend erreur 401
    assert response.json()["detail"] == "Identifiants invalides"    # vérification du message d'erreur
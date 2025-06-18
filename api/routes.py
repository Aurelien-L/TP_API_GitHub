from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from typing import List
from .models import User
from .security import authenticate
import json

# Chargement des utilisateurs au démarrage
with open("data/filtered_users.json", encoding="utf-8") as f:
    USERS = json.load(f)

router = APIRouter()


# ROUTES

# Route permettant de récupérer la liste d'utilisateurs
@router.get("/users/", response_model=List[User], summary="Liste des utilisateurs", description="Route permettant de récupérer la liste de tous les utilisateurs")     
# crée route GET sur /users/ avec une réponse sous forme de liste d'objets User
def get_users(credentials: HTTPBasicCredentials = Depends(authenticate)):   # route protégée par auth
    return USERS


# Route permettant de trouver des utilisateurs par mot-clé :
@router.get("/users/search", response_model=List[User], summary="Recherche d'utilisateurs", description="Route permettant de trouver des utilisateurs par mot-clé")
def search_users(q: str, credentials: HTTPBasicCredentials = Depends(authenticate)):
    results = [user for user in USERS if q.lower() in user["login"].lower()]
    return results      # retourne tous les utilisateurs dont le login contient q


# Route permettant de récupérer les détails d'un utilisateur
@router.get("/users/{login}", response_model=User, summary="Détails d'un utilisateur", description="Route permettant de récupérer les détails d'un utilisateur")
def get_user(login: str, credentials: HTTPBasicCredentials = Depends(authenticate)):
    for user in USERS:
        if user["login"].lower() == login.lower():
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")



"""
ATTENTION :
Si le router @router.get("/users/search" ... ) est après le router @router.get("/users/{login}" ...) cela ne fonctionne pas :

- FastAPI essaie de faire correspondre l’URL demandée à la première route qui semble correspondre.
- FastAPI interprète toute URL après /users/ comme une variable dynamique appelée login.
- Donc si /users/search est appelée après cette route :
- FastAPI pense que search est une valeur de login
- Il appelle get_user(login="search")
- Et comme aucun utilisateur ne s'appelle "search" -> erreur 404


Astuce : Règle générale pour FastAPI
-> Toujours déclarer les routes les plus spécifiques (chemins fixes) avant les routes dynamiques ({param}) dans un même préfixe.

"""
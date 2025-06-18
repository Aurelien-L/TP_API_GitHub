from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from dotenv import load_dotenv

security = HTTPBasic()  # pour activer sécurité HTTP Basic

# Récupération des identifiants valides
load_dotenv()
VALID_USERS = {
    os.getenv("USERNAME"): os.getenv("PASSWORD")
}


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Fonction permettant de vérifier les identifiants :
    - si mauvais -> Erreur 401 (non autorisé)
    - sinon OK

    """

    correct_username = credentials.username
    correct_password = credentials.password

    if VALID_USERS.get(correct_username) != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Basic"}
        )
    
    return credentials
from pydantic import BaseModel

# Classe qui définit les champs obligatoires pour un utilisateur.
# Permet à FastAPI de valider les données automatiquement et de générer une doc Swagger propre
class User(BaseModel):
    login: str
    id: int
    created_at: str
    avatar_url: str
    bio: str


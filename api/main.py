from fastapi import FastAPI
from .routes import router


# Instance de l'application FastAPI
app = FastAPI(
    title="API utilisateurs GitHub",
    description="API permettant d'accéder à une liste d'utilisateurs GitHub filtrée.",
    version="1.0.0"
)

# Import des routes
app.include_router(router)
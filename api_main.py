# Fichier : api_main.py
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from accounts.api import router as accounts_router

# On utilise NinjaExtraAPI pour supporter les fonctionnalités de Token
api = NinjaExtraAPI(title="Food Spot API", version="1.0.0")

# Cette ligne magique crée les routes /api/token/pair (Login) 
# et /api/token/refresh (Rester connecté)
api.register_controllers(NinjaJWTDefaultController)

# On ajoute tes routes d'inscription et de profil
api.add_router("/auth/", accounts_router)
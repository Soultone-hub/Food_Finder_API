# Fichier : accounts/api.py
from ninja import Router
from ninja_jwt.authentication import JWTAuth
from .models import User, Seller
from .schemas import RegisterSchema, UpgradeSchema, LogoutSchema, ForgotPasswordSchema, ResetPasswordSchema, UpdateProfileSchema
from django.contrib.auth.hashers import make_password
from ninja_jwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


router = Router()

@router.post("/register")
def register(request, data: RegisterSchema):
    user = User.objects.create(
        email=data.email,
        password=make_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        num_phone=data.num_phone,
        sexe=data.sexe,
        role='client'
    )
    return {"message": "Utilisateur créé", "id": str(user.id)}

@router.post("/become-seller", auth=JWTAuth()) 
def become_seller(request, data: UpgradeSchema):
    # 'request.user' est automatiquement rempli grâce au Token
    user = request.user 
    
    if hasattr(user, 'seller'):
        return {"error": "Vous avez déjà un profil vendeur"}

    Seller.objects.create(
        user=user,
        brand_name=data.brand_name,
        siret_ou_id=data.siret_ou_id
    )
    user.role = 'owner'
    user.save()
    return {"message": "Profil vendeur activé avec succès"}

@router.post("/logout", auth=JWTAuth())
def logout(request, data: LogoutSchema):
    try:
        token = RefreshToken(data.refresh)
        token.blacklist()
        return {"message": "Déconnexion réussie"}
    except Exception:
        return {"error": "Token invalide ou déjà expiré"}
    


@router.post("/forgot-password")
def forgot_password(request, data: ForgotPasswordSchema):
    try:
        user = User.objects.get(email=data.email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # On affiche le lien dans la console (grâce au backend console)
        print(f"Lien de reset: UID={uid} / TOKEN={token}")
        
        return {"message": "Si l'email existe, un lien a été envoyé."}
    except User.DoesNotExist:
        return {"message": "Si l'email existe, un lien a été envoyé."} # Sécurité : ne pas dire si le mail existe ou non

# 2. Valider le nouveau mot de passe
@router.post("/reset-password-confirm")
def reset_password_confirm(request, data: ResetPasswordSchema):
    try:
        # 'token' ici dans notre exemple simplifié contiendra UID:TOKEN envoyé par Flutter
        uid_b64, token = data.token.split(':')
        uid = force_str(urlsafe_base64_decode(uid_b64))
        user = User.objects.get(pk=uid)
        
        if default_token_generator.check_token(user, token):
            user.set_password(data.new_password)
            user.save()
            return {"message": "Mot de passe modifié avec succès !"}
        return {"error": "Lien invalide ou expiré"}, 400
    except Exception:
        return {"error": "Une erreur est survenue"}, 400
    

@router.get("/me", auth=JWTAuth())
def get_me(request):
    user = request.user
    return {
        "id": user.id,
        "email": user.email,
        "num_phone": user.num_phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_seller": hasattr(user, 'seller')
    }


@router.patch("/me/update", auth=JWTAuth())
def update_me(request, data: UpdateProfileSchema):
    user = request.user
    # On met à jour les champs un par un
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.num_phone = data.num_phone
    user.save()
    return {"message": "Profil mis à jour avec succès"}



@router.delete("/me/delete", auth=JWTAuth())
def delete_me(request):
    user = request.user
    user.delete() # Cela supprimera aussi le profil Seller s'il existe (grâce au CASCADE)
    return {"message": "Compte supprimé définitivement"}
# Fichier : accounts/schemas.py
from ninja import Schema
from uuid import UUID
from datetime import datetime
from pydantic import EmailStr, Field # Ajoute Field si besoin

class RegisterSchema(Schema):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str
    num_phone: str
    sexe: str

class UpgradeSchema(Schema):
    brand_name: str
    siret_ou_id: str

class LogoutSchema(Schema):
    refresh: str # On a besoin du refresh token pour le bannir

class ForgotPasswordSchema(Schema):
    email: EmailStr

class ResetPasswordSchema(Schema):
    token: str
    new_password: str = Field(..., min_length=8)

class UpdateProfileSchema(Schema):
    first_name: str
    last_name: str
    num_phone: str
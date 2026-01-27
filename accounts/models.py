from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid

# 1. On crée un gestionnaire personnalisé
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# 2. Ton modèle User utilise maintenant ce gestionnaire
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    num_phone = models.CharField(max_length=20, unique=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'M'), ('F', 'F'), ('A', 'A')])
    role = models.CharField(max_length=20, default='client')
    created_at = models.DateTimeField(auto_now_add=True)
    
    username = None 
    email = models.EmailField(unique=True)
    
    # On branche le nouveau gestionnaire ici
    objects = UserManager() 
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    brand_name = models.CharField(max_length=150)
    siret_ou_id = models.CharField(max_length=50)
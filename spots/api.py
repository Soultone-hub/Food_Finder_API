from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from typing import List
from .models import Spot, Category
from .schemas import SpotIn, SpotOut, CategoryOut, CategoryIn
from uuid import UUID

router = Router(tags=["Spots"])

@router.post("/categories", response=CategoryOut, tags=["categorie"])
def create_category(request, data: CategoryIn):
    category = Category.objects.create(**data.dict())
    return category

@router.get("/categories", response=List[CategoryOut], tags=["categorie"])
def list_categories(request):
    """
    Retourne la liste de toutes les catégories disponibles 
    pour que le vendeur puisse choisir.
    """
    return Category.objects.all()

# 1. LISTER (Public)
@router.get("/", response=List[SpotOut])
def list_spots(request):
    return Spot.objects.all()

# 2. CRÉER (Authentifié)
@router.post("/", response=SpotOut, auth=JWTAuth())
def create_spot(request, data: SpotIn):
    category = get_object_or_404(Category, id=data.category_id)
    payload = data.dict()
    payload.pop('category_id')
    
    spot = Spot.objects.create(
        **payload,
        seller=request.user,
        category=category
    )
    return spot

# 3. MODIFIER (Authentifié + Propriétaire)
@router.patch("/{spot_id}", response=SpotOut, auth=JWTAuth())
def update_spot(request, spot_id: UUID, data: SpotIn):
    spot = get_object_or_404(Spot, id=spot_id, seller=request.user)
    for attr, value in data.dict(exclude_unset=True).items():
        if attr == 'category_id':
            spot.category = get_object_or_404(Category, id=value)
        else:
            setattr(spot, attr, value)
    spot.save()
    return spot

# 4. SUPPRIMER (Authentifié + Propriétaire)
@router.delete("/{spot_id}", auth=JWTAuth())
def delete_spot(request, spot_id: UUID):
    spot = get_object_or_404(Spot, id=spot_id, seller=request.user)
    spot.delete()
    return {"success": True}
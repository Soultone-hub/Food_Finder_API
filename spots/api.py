from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.shortcuts import get_object_or_404
from typing import List
from .models import Spot, Category, MenuItem, OpeningHour
from .schemas import SpotIn, SpotOut, CategoryOut, CategoryIn, MenuItemIn, MenuItemOut, OpeningHourIn, OpeningHourOut
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






@router.post("/{spot_id}/menu", response=MenuItemOut, auth=JWTAuth(), tags=["Menu"])
def add_menu_item(request, spot_id: UUID, data: MenuItemIn):
    # On vérifie que le stand appartient bien au vendeur connecté
    spot = get_object_or_404(Spot, id=spot_id, seller=request.user)
    item = MenuItem.objects.create(spot=spot, **data.dict())
    return item

@router.get("/{spot_id}/menu", response=List[MenuItemOut], tags=["Menu"])
def list_menu_items(request, spot_id: UUID):
    # Route publique pour que les clients voient la carte du stand
    return MenuItem.objects.filter(spot_id=spot_id, is_available=True)






@router.post("/{spot_id}/hours", response=OpeningHourOut, auth=JWTAuth(), tags=["Horaires"])
def add_opening_hour(request, spot_id: UUID, data: OpeningHourIn):
    spot = get_object_or_404(Spot, id=spot_id, seller=request.user)
    # Correction des noms : day -> day_of_week, opening_time -> open_time, etc.
    hour, created = OpeningHour.objects.update_or_create(
        spot=spot, 
        day_of_week=data.day_of_week, # <--- Corrigé
        defaults={
            'open_time': data.open_time, # <--- Corrigé
            'close_time': data.close_time # <--- Corrigé
        }
    )
    return hour

@router.get("/{spot_id}/hours", response=List[OpeningHourOut], tags=["Horaires"])
def list_spot_hours(request, spot_id: UUID):
    # Correction : .order_by('day') -> .order_by('day_of_week')
    return OpeningHour.objects.filter(spot_id=spot_id).order_by('day_of_week')
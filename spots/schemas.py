from ninja import Schema
from uuid import UUID
from typing import List, Optional

class CategoryOut(Schema):
    id: int
    label: str
    icon_url: Optional[str]

class SpotIn(Schema):
    name: str
    description: Optional[str] = None
    category_id: int
    address: str
    latitude: float
    longitude: float

class SpotOut(Schema):
    id: UUID
    name: str
    description: Optional[str]
    address: str
    latitude: float
    longitude: float
    is_active: bool
    category: Optional[CategoryOut]
    seller_id: UUID

class CategoryIn(Schema):
    label: str
    icon_url: Optional[str] = None
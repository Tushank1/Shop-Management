from fastapi import status,HTTPException,Depends,APIRouter
from typing import List
from .. import models
from sqlalchemy.orm import Session
from ..schemas import ShopResponse
from ..database import get_db
from ..utils import haversine

router = APIRouter(prefix="/search",tags=["Search"])

@router.get("/nearby_shops",response_model=List[ShopResponse])
def nearby_shops(latitude: float,longitude: float,radius: float = 50,db: Session = Depends(get_db)):
    shops = db.query(models.Shop).all()
    nearby_shops = []
    
    for shop in shops:
        distance = haversine(latitude,longitude,shop.latitude,shop.longitude)
        if distance <= radius:
            nearby_shops.append(shop)
    
    if not nearby_shops:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No nearby shops found")

    return [ShopResponse(**shop.__dict__) for shop in nearby_shops]
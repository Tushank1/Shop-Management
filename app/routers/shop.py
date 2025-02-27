from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import ShopCreate,ShopResponse,ShopUpdate
from ..auth import get_current_user

router = APIRouter(prefix="/shops",tags=["Shops"])

@router.post("/create",response_model=ShopResponse)
def create_shop(shop: ShopCreate,db: Session = Depends(get_db),current_vendor: models.Vendor = Depends(get_current_user)):
    if not current_vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    
    new_shop = models.Shop(name=shop.name,type=shop.type,latitude=shop.latitude,longitude=shop.longitude,vendor_id=current_vendor.id)
    db.add(new_shop)
    db.commit()
    db.refresh(new_shop)
    return new_shop

@router.get("/retrieve",response_model=list[ShopResponse])
def retrieve(db: Session = Depends(get_db),current_vendor: models.Vendor = Depends(get_current_user)):
    retrieve_data = db.query(models.Shop).filter(models.Shop.vendor_id == current_vendor.id).all()
    return retrieve_data
    
@router.put("/update/{shop_id}",response_model=ShopResponse)
def update_shop(shop_id: int,shop_data: ShopUpdate,db: Session = Depends(get_db),current_vendor: models.Vendor = Depends(get_current_user)):
    shop = db.query(models.Shop).filter(models.Shop.id == shop_id,models.Shop.vendor_id == current_vendor.id).first()

    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Shop not found or you don't have permission to update it.")
        
    shop_dict = shop_data.dict(exclude_unset=True)  # Keep only provided fields
    for field, value in shop_dict.items():
        setattr(shop, field, value)

    db.commit()
    db.refresh(shop)
    return shop

@router.delete("/delete/{shop_id}",status_code=status.HTTP_204_NO_CONTENT)
def destroy(shop_id: int,db: Session = Depends(get_db),current_vendor: models.Vendor = Depends(get_current_user)):
    shop = db.query(models.Shop).filter(models.Shop.id == shop_id,models.Shop.vendor_id == current_vendor.id).first()
    
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Shop not found or unauthorized to delete")

    db.delete(shop)
    db.commit()
    return {"message": "Shop deleted successfully"}
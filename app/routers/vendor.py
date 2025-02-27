from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas import VendorResponse,VendorCreate,TokenData
from ..auth import verify_password,create_access_token,hash_password

router = APIRouter(prefix="/vendors",tags=["Vendors"])

@router.post("/register",response_model=VendorResponse)
def register_vendor(vendor: VendorCreate,db: Session = Depends(get_db)):
    if db.query(models.Vendor).filter(models.Vendor.email == vendor.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")

    hashed_pwd = hash_password(vendor.password)
    new_vendor = models.Vendor(name=vendor.name,email=vendor.email,password=hashed_pwd)
    db.add(new_vendor)
    db.commit()
    return new_vendor

@router.get("/token", response_model=TokenData)
def login_vendor(email: str, password: str, db: Session = Depends(get_db)):
    vendor = db.query(models.Vendor).filter(models.Vendor.email == email).first()
    if not vendor or not verify_password(password, vendor.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": vendor.email})
    return {"access_token": access_token, "token_type": "bearer"}
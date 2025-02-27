from pydantic import BaseModel , EmailStr
from typing import List,Optional

class VendorCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
class VendorResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attribute = True
        
class TokenData(BaseModel):
    access_token: str
    token_type: str
    
    
class ShopCreate(BaseModel):
    name: str
    type: str
    latitude: float
    longitude: float
    
class ShopResponse(BaseModel):
    id: int
    name: str
    type: str
    latitude: float
    longitude: float
    
    class Config:
        from_attribute = True
        
class ShopUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
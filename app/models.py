from sqlalchemy import Column,Integer,String,ForeignKey,Float
from sqlalchemy.orm import relationship
from app.database import Base

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True,index=True)
    password = Column(String,nullable=False)
    
    shops = relationship("Shop", back_populates="owner", cascade="all, delete-orphan")
    
class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    type = Column(String,nullable=False)
    latitude = Column(Float,nullable=False)
    longitude = Column(Float,nullable=False)
    
    vendor_id = Column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False, index=True)
    owner = relationship("Vendor",back_populates="shops")
    

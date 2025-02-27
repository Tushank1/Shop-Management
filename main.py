from fastapi import FastAPI
from app.database import engine,Base,get_db
from app.routers import vendor,shop,search

app = FastAPI(title="Vendor Shop Management API")

Base.metadata.create_all(bind=engine)


app.include_router(vendor.router)
app.include_router(shop.router)
app.include_router(search.router)


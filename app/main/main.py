from fastapi import FastAPI
from app.infrastructure.database.sqlalchemy.session import Base, engine
from app.interfaces.api.fastapi.routes import parceiro_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    # Create tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

app.include_router(parceiro_router.router, prefix="/api", tags=["parceiros"])

from fastapi import FastAPI
from app.interfaces.api.fastapi.routes import parceiro_router

def get_app() -> FastAPI:
    app = FastAPI()
    app.include_router(parceiro_router.router, prefix="/api", tags=["parceiros"])
    return app

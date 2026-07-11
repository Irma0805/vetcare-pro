from fastapi import FastAPI

from app.routers import usuario

app = FastAPI(title="VetCare Pro API")

app.include_router(usuario.router)
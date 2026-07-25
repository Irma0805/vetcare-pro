from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import usuario, cita, veterinario, propietario, mascota, tratamiento

app = FastAPI(title="VetCare Pro API")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuario.router)
app.include_router(cita.router)
app.include_router(veterinario.router)
app.include_router(propietario.router)
app.include_router(mascota.router)
app.include_router(tratamiento.router)
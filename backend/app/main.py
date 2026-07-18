from fastapi import FastAPI

from app.routers import usuario, cita, veterinario, propietario, mascota

app = FastAPI(title="VetCare Pro API")

app.include_router(usuario.router)
app.include_router(cita.router)
app.include_router(veterinario.router)
app.include_router(propietario.router)
app.include_router(mascota.router)
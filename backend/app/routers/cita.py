from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controlador.cita import crear_cita as crear_cita_controlador
from app.database import get_db
from app.schemas.cita import CitaCreate, CitaResponse
from app.exceptions import (
    PropietarioNoEncontradoError,
    MascotaNoEncontradaError,
    VeterinarioNoDisponibleError,
)

router = APIRouter(tags=["Gestión de Citas"])


@router.post("/citas", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(datos: CitaCreate, db: Session = Depends(get_db)):
    """
    Endpoint de creación de cita (FUS-03/CU-04).
    Toda la orquestación (resolver propietario, mascota, veterinario,
    crear la cita) vive en controlador.cita.crear_cita — este
    endpoint solo traduce las excepciones de dominio a HTTP.
    """
    try:
        return crear_cita_controlador(db, datos)
    except PropietarioNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El propietario indicado no existe",
        )
    except MascotaNoEncontradaError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La mascota indicada no existe",
        )
    except VeterinarioNoDisponibleError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El veterinario no está disponible",
        )
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controlador.cita import crear_cita as crear_cita_controlador
from app.controlador.cita import listar_citas as listar_citas_controlador
from app.database import get_db
from app.schemas.cita import CitaCreate, CitaListItem, CitaResponse
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


@router.get("/citas", response_model=list[CitaListItem])
def listar_citas(
    pagina: int = Query(1, ge=1, description="Página del listado (10 citas por página)"),
    db: Session = Depends(get_db),
):
    """
    Endpoint de listado paginado de citas (FUS-06/CU-07).
    Sin excepciones que traducir: si la página solicitada excede el
    total disponible, el controlador ya la ajusta a la última válida
    (sin error visible, tal como exige el Gherkin) — este endpoint
    nunca lanza HTTPException.
    """
    return listar_citas_controlador(db, pagina)
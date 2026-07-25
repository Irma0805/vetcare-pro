from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controlador.tratamiento import listar_tratamientos as listar_tratamientos_controlador
from app.database import get_db
from app.schemas.tratamiento import TratamientoResponse

router = APIRouter(tags=["Tratamientos"])


@router.get("/tratamientos", response_model=list[TratamientoResponse])
def listar_tratamientos(db: Session = Depends(get_db)):
    """
    Endpoint de listado del catálogo de tratamientos (FUS-05/CU-06).

    Sin paginación ni filtros: alimenta el selector de tratamientos
    del formulario de asociación, sobre un catálogo pequeño y fijo
    sembrado en pgAdmin (decisión ya documentada). Sin excepciones
    que traducir: es una lectura simple, siempre devuelve 200 OK,
    con lista vacía si el catálogo estuviera vacío.
    """
    return listar_tratamientos_controlador(db)
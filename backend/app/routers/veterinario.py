from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.controlador.veterinario import crear_veterinario as crear_veterinario_controlador
from app.controlador.veterinario import listar_veterinarios as listar_veterinarios_controlador
from app.database import get_db
from app.schemas.veterinario import VeterinarioCreate, VeterinarioResponse

router = APIRouter(tags=["Veterinarios"])


@router.post("/veterinarios", response_model=VeterinarioResponse, status_code=status.HTTP_201_CREATED)
def crear_veterinario(datos: VeterinarioCreate, db: Session = Depends(get_db)):
    """
    Endpoint de alta de veterinario (FUS-19/CU-20).
    Sin excepciones de dominio que traducir: a diferencia de crear_cita,
    esta HU no depende de otras entidades ya existentes, así que
    Pydantic (422) cubre el único caso de error del Gherkin.
    """
    return crear_veterinario_controlador(db, datos)


@router.get("/veterinarios", response_model=list[VeterinarioResponse])
def listar_veterinarios(
    pagina: int = Query(1, ge=1, description="Página del listado (10 veterinarios por página)"),
    db: Session = Depends(get_db),
):
    """
    Endpoint de listado de veterinarios activos, paginado (FUS-20/CU-21).
    Devuelve lista vacía [] si no hay veterinarios activos (200 OK);
    el mensaje de "listado vacío" del Gherkin es responsabilidad del
    frontend, no de este endpoint.
    """
    return listar_veterinarios_controlador(db, pagina)
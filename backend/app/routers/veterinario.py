from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controlador.veterinario import crear_veterinario as crear_veterinario_controlador
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
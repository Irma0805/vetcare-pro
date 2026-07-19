"""
Orquestación de negocio para Veterinario (ADR-003).
"""

from sqlalchemy.orm import Session

from app.models.veterinario import Veterinario
from app.schemas.veterinario import VeterinarioCreate
from app.service.veterinario import create_veterinario as _create_veterinario
from app.service.veterinario import get_veterinarios_activos as _get_veterinarios_activos

TAMANO_PAGINA = 10


def crear_veterinario(db: Session, datos: VeterinarioCreate) -> Veterinario:
    """
    Da de alta un veterinario (FUS-19/CU-20).

    Un único commit: no hay otras entidades que resolver (a diferencia
    de CU-04), así que no hace falta db.flush() intermedio.

    No se llama a db.refresh() tras el commit: SessionLocal usa
    expire_on_commit=True (comportamiento por defecto de SQLAlchemy),
    así que el primer acceso a veterinario.id_veterinario tras el
    commit ya dispara la recarga automáticamente (verificado).
    """
    veterinario = _create_veterinario(db, datos)
    db.commit()
    return veterinario


def listar_veterinarios(db: Session, pagina: int) -> list[Veterinario]:
    """
    Lista veterinarios activos, paginados (FUS-20/CU-21).

    Operación de solo lectura: no hay commit. TAMANO_PAGINA fijo a 10,
    coherente con el Gherkin ("paginado, 10 por página") — no se
    expone como parámetro ajustable porque nadie lo ha pedido (YAGNI).
    """
    skip = (pagina - 1) * TAMANO_PAGINA
    return _get_veterinarios_activos(db, skip=skip, limit=TAMANO_PAGINA)
"""
Orquestación de negocio para Veterinario (ADR-003).
"""

from sqlalchemy.orm import Session

from app.models.veterinario import Veterinario
from app.schemas.veterinario import VeterinarioCreate
from app.service.veterinario import create_veterinario as _create_veterinario


def crear_veterinario(db: Session, datos: VeterinarioCreate) -> Veterinario:
    """
    Da de alta un veterinario (FUS-19/CU-20).

    Un único commit: no hay otras entidades que resolver (a diferencia
    de CU-04), así que no hace falta db.flush() intermedio.

    No se llama a db.refresh() tras el commit: SessionLocal usa
    expire_on_commit=True (comportamiento por defecto de SQLAlchemy),
    así que el primer acceso a veterinario.id_veterinario tras el
    commit ya dispara la recarga automáticamente.
    """
    veterinario = _create_veterinario(db, datos)
    db.commit()
    return veterinario
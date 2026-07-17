"""
Capa de acceso a datos para la entidad Veterinario (ADR-008).

Incluye create_veterinario (alta, FUS-19/CU-20) y get_veterinario_activo
(resolución de un veterinario ya existente, usada en CU-04) y
get_veterinarios_activos (listado paginado, FUS-20/CU-21)..
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.veterinario import Veterinario
from app.schemas.veterinario import VeterinarioCreate


def get_veterinario_activo(db: Session, veterinario_id: int) -> Veterinario | None:
    """
    Consulta un veterinario por su ID, exigiendo que esté activo.

    Devuelve None tanto si el veterinario no existe como si existe
    pero está inactivo — el Gherkin de CU-04 solo contempla un único
    mensaje de rechazo ("veterinario no disponible"), sin distinguir
    el motivo. El controlador traduce ese None al error HTTP
    correspondiente.
    """
    veterinario = db.get(Veterinario, veterinario_id)
    if veterinario is None or not veterinario.activo:
        return None
    return veterinario


def create_veterinario(db: Session, datos: VeterinarioCreate) -> Veterinario:
    """
    Crea un veterinario nuevo (FUS-19/CU-20).

    Solo hace db.add(): sin flush ni commit, control de transacción
    centralizado en el controlador (mismo patrón Unit of Work que
    propietario.py y mascota.py).
    """
    veterinario = Veterinario(
        nombre=datos.nombre,
        apellidos=datos.apellidos,
        especialidad=datos.especialidad,
    )
    db.add(veterinario)
    return veterinario

def get_veterinarios_activos(db: Session, skip: int, limit: int) -> list[Veterinario]:
    """
    Lista veterinarios activos, ordenados por apellidos (FUS-20/CU-21).

    Operación de solo lectura: no hace falta commit ni flush.
    """
    stmt = (
        select(Veterinario)
        .where(Veterinario.activo == True)  # noqa: E712 (comparación explícita, estilo SQLAlchemy)
        .order_by(Veterinario.apellidos)
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt).all())
"""
Capa de acceso a datos para la entidad Tratamiento (ADR-008).

Contiene únicamente operaciones directas de consulta sobre el
catálogo de tratamientos. No orquesta lógica de negocio ni gestiona
el ciclo de vida de la transacción.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tratamiento import Tratamiento


def get_tratamiento_by_id(db: Session, tratamiento_id: int) -> Tratamiento | None:
    """
    Consulta un tratamiento existente del catálogo por su ID.

    Devuelve None si no existe; es responsabilidad del controlador
    decidir qué error de negocio corresponde ante esa ausencia.
    """
    return db.get(Tratamiento, tratamiento_id)


def get_tratamientos(db: Session) -> list[Tratamiento]:
    """
    Lista el catálogo completo de tratamientos, ordenado por nombre
    (FUS-05/CU-06 — endpoint de lectura añadido como enmienda a la
    decisión original de "sin endpoint", al aparecer un consumidor
    real: el selector de tratamientos en el formulario de asociación).

    Sin paginación: el catálogo es un conjunto pequeño y fijo,
    sembrado directamente en pgAdmin, pensado para alimentar un
    <select> de un modal — no una tabla paginada. Decisión consciente
    de no replicar el patrón de get_veterinarios_activos.
    """
    stmt = select(Tratamiento).order_by(Tratamiento.nombre)
    return list(db.scalars(stmt).all())
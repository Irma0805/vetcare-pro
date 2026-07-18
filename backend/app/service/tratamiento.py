"""
Capa de acceso a datos para la entidad Tratamiento (ADR-008).

Contiene únicamente operaciones directas de consulta sobre el
catálogo de tratamientos. No orquesta lógica de negocio ni gestiona
el ciclo de vida de la transacción.
"""

from sqlalchemy.orm import Session

from app.models.tratamiento import Tratamiento


def get_tratamiento_by_id(db: Session, tratamiento_id: int) -> Tratamiento | None:
    """
    Consulta un tratamiento existente del catálogo por su ID.

    Devuelve None si no existe; es responsabilidad del controlador
    decidir qué error de negocio corresponde ante esa ausencia.
    """
    return db.get(Tratamiento, tratamiento_id)
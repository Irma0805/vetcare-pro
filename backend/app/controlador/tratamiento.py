"""
Orquestación de negocio para Tratamiento (ADR-008).

listar_tratamientos: FUS-05/CU-06 (lectura del catálogo para el
selector del formulario de asociación).
"""

from sqlalchemy.orm import Session

from app.models.tratamiento import Tratamiento
from app.service.tratamiento import get_tratamientos


def listar_tratamientos(db: Session) -> list[Tratamiento]:
    """
    Orquesta la lectura del catálogo completo de tratamientos.

    Sin excepciones de dominio que traducir ni combinación de varias
    fuentes de datos: delega directamente en el service. Se mantiene
    como capa propia, en vez de saltarla, por consistencia con la
    arquitectura de 5 capas ya exigida en el resto del proyecto
    (routers → controlador → service → validation → BD) — no porque
    esta HU concreta necesite orquestación real hoy.
    """
    return get_tratamientos(db)
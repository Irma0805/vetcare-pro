"""
Orquestación de negocio para Mascota (ADR-003).
"""

from sqlalchemy.orm import Session

from app.schemas.mascota import FichaMascotaResponse
from app.schemas.propietario import PropietarioResumen
from app.service.mascota import get_mascota_by_id
from app.service.propietario import get_propietario_by_id
from app.exceptions import MascotaNoEncontradaError


def obtener_ficha_mascota(db: Session, mascota_id: int) -> FichaMascotaResponse:
    """
    Construye la ficha de mascota (FUS-16/CU-17): datos identificativos +
    propietario en solo lectura.

    No hay relationship() ORM entre Mascota y Propietario, así que se
    combinan explícitamente aquí en vez de depender de serialización
    automática de un atributo anidado (mismo criterio ya aplicado en
    obtener_ficha_cliente, en sentido inverso).
    """
    mascota = get_mascota_by_id(db, mascota_id)
    if mascota is None:
        raise MascotaNoEncontradaError()

    propietario = get_propietario_by_id(db, mascota.id_propietario)

    return FichaMascotaResponse(
        id_mascota=mascota.id_mascota,
        nombre=mascota.nombre,
        especie=mascota.especie,
        raza=mascota.raza,
        fecha_nacimiento=mascota.fecha_nacimiento,
        peso=mascota.peso,
        activo=mascota.activo,
        propietario=PropietarioResumen.model_validate(propietario),
    )
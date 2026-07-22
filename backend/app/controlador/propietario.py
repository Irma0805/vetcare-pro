"""
Orquestación de negocio para Propietario (ADR-003).
"""

from sqlalchemy.orm import Session

from app.schemas.propietario import FichaClienteResponse, MascotaResumen
from app.service.propietario import get_propietario_by_id, get_propietario_by_dni
from app.service.mascota import get_mascotas_por_propietario
from app.exceptions import PropietarioNoEncontradoError
from app.models.propietario import Propietario


def obtener_ficha_cliente(db: Session, propietario_id: int) -> FichaClienteResponse:
    """
    Construye la ficha de cliente (FUS-13/CU-14): datos de contacto +
    listado de mascotas asociadas (activas e inactivas).

    No hay relationship() ORM entre Propietario y Mascota, así que se
    combinan explícitamente aquí en vez de depender de serialización
    automática de un atributo anidado (verificado: Pydantic v2 no
    recorre relaciones ORM anidadas de forma automática, solo lee
    atributos directos del objeto que recibe).
    """
    propietario = get_propietario_by_id(db, propietario_id)
    if propietario is None:
        raise PropietarioNoEncontradoError()

    mascotas = get_mascotas_por_propietario(db, propietario_id)

    return FichaClienteResponse(
        id_propietario=propietario.id_propietario,
        dni=propietario.dni,
        nombre=propietario.nombre,
        apellidos=propietario.apellidos,
        direccion=propietario.direccion,
        telefono=propietario.telefono,
        email=propietario.email,
        mascotas=[MascotaResumen.model_validate(m) for m in mascotas],
    )


def buscar_propietario_por_dni(db: Session, dni: str) -> Propietario | None:
    """
    Orquestación de la búsqueda de propietario por DNI (FUS-03/CU-04).

    Passthrough directo al service: no hay lógica de negocio que
    aplicar aquí, pero se mantiene la capa de controlador por
    consistencia arquitectónica (todos los endpoints pasan por
    controlador, sin excepciones caso por caso).

    Devuelve None si no existe; no es un error de negocio, así que el
    router no debe traducirlo a una excepción HTTP — es un resultado
    válido de búsqueda (candidato a "cliente nuevo").
    """
    return get_propietario_by_dni(db, dni)
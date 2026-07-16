"""
Orquestación de la creación de cita (FUS-03/CU-04, ADR-008).

Resuelve propietario, mascota y veterinario a través de service/,
sin tocar la base de datos directamente. No lanza HTTPException (eso
es responsabilidad de routers/): lanza excepciones de dominio
(app/exceptions.py) que el router traduce al código HTTP adecuado.

Único punto de control de la transacción: un solo db.commit() al
final, tras resolver los tres pasos previos, para garantizar
atomicidad (verificado contra el patrón Unit of Work de SQLAlchemy).
"""

from sqlalchemy.orm import Session

from app.schemas.cita import CitaCreate
from app.models.cita import Cita
from app.service.propietario import get_propietario_by_id, create_propietario
from app.service.mascota import get_mascota_by_id, create_mascota
from app.service.veterinario import get_veterinario_activo
from app.service.cita import create_cita
from app.exceptions import (
    PropietarioNoEncontradoError,
    MascotaNoEncontradaError,
    VeterinarioNoDisponibleError,
)


def crear_cita(db: Session, datos: CitaCreate) -> Cita:
    """
    Orquesta CU-04: resuelve propietario, mascota y veterinario, y
    crea la cita. La combinación propietario_nuevo + mascota_id ya
    está bloqueada a nivel de schema (CitaCreate), así que si el
    propietario es nuevo, la mascota es siempre nueva también — por
    eso el flush tras crear el propietario es siempre necesario en
    esa rama, nunca superfluo.
    """
    if datos.propietario_id is not None:
        propietario = get_propietario_by_id(db, datos.propietario_id)
        if propietario is None:
            raise PropietarioNoEncontradoError()
    else:
        propietario = create_propietario(db, datos.propietario_nuevo)
        db.flush()

    if datos.mascota_id is not None:
        mascota = get_mascota_by_id(db, datos.mascota_id)
        if mascota is None:
            raise MascotaNoEncontradaError()
    else:
        mascota = create_mascota(db, datos.mascota_nueva, propietario.id_propietario)

    veterinario = get_veterinario_activo(db, datos.veterinario_id)
    if veterinario is None:
        raise VeterinarioNoDisponibleError()

    cita = create_cita(
        db,
        fecha_hora=datos.fecha_hora,
        motivo_consulta=datos.motivo_consulta,
        id_mascota=mascota.id_mascota,
        id_veterinario=veterinario.id_veterinario,
    )

    db.commit()

    return cita
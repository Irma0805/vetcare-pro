"""
Orquestación de negocio para Cita (ADR-008).

crear_cita: FUS-03/CU-04. listar_citas: FUS-06/CU-07.
"""

import math

from sqlalchemy import Row
from sqlalchemy.orm import Session

from app.schemas.cita import CitaCreate
from app.models.cita import Cita
from app.service.propietario import get_propietario_by_id, create_propietario
from app.service.mascota import get_mascota_by_id, create_mascota
from app.service.veterinario import get_veterinario_activo
from app.service.cita import create_cita, contar_citas, get_citas_paginadas
from app.exceptions import (
    PropietarioNoEncontradoError,
    MascotaNoEncontradaError,
    VeterinarioNoDisponibleError,
)

TAMANO_PAGINA = 10


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
        db.flush()

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


def listar_citas(db: Session, pagina: int) -> list[Row]:
    """
    Lista citas paginadas (FUS-06/CU-07).

    Si `pagina` excede el total de páginas disponibles, se ajusta
    ("clampea") a la última página válida en vez de devolver una
    lista vacía o un error — así lo exige el Gherkin ("no produce
    ningún error visible y muestra la última página válida").

    Con 0 citas registradas, total_paginas queda en 1 (no en 0):
    así pagina_efectiva siempre es un entero válido >= 1, y el
    resultado es una lista vacía de forma natural, sin caso especial.
    """
    total = contar_citas(db)
    total_paginas = max(1, math.ceil(total / TAMANO_PAGINA))
    pagina_efectiva = min(pagina, total_paginas)

    skip = (pagina_efectiva - 1) * TAMANO_PAGINA
    return get_citas_paginadas(db, skip=skip, limit=TAMANO_PAGINA)
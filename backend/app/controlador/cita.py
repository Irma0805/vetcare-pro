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
    CitaNoEncontradaError,
    TratamientoNoEncontradoError,
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

def asociar_tratamiento(
    db: Session, cita_id: int, datos: AsociarTratamientoCreate
) -> CitasTratamientos:
    """
    Orquesta CU-06: comprueba que la cita y el tratamiento existen,
    calcula valor_tratamiento y crea el registro en Citas_Tratamientos.

    valor_tratamiento = peso de la mascota × tarifa_por_kg del
    tratamiento. Si la mascota no tiene peso registrado, queda en
    None (no bloquea la asociación, tal como exige el Gherkin).

    Este cálculo vive aquí, no en service/, porque combina datos de
    dos entidades distintas (Mascota y Tratamiento) — es orquestación
    de negocio, no acceso a datos puro.
    """
    cita = get_cita_by_id(db, cita_id)
    if cita is None:
        raise CitaNoEncontradaError()

    tratamiento = get_tratamiento_by_id(db, datos.id_tratamiento)
    if tratamiento is None:
        raise TratamientoNoEncontradoError()

    mascota = get_mascota_by_id(db, cita.id_mascota)

    if mascota.peso is not None:
        valor_tratamiento = mascota.peso * tratamiento.tarifa_por_kg
    else:
        valor_tratamiento = None

    registro = create_cita_tratamiento(
        db,
        id_cita=cita.id_cita,
        id_tratamiento=tratamiento.id_tratamiento,
        fecha_inicio=datos.fecha_inicio,
        fecha_fin=datos.fecha_fin,
        dosis=datos.dosis,
        seguimiento=datos.seguimiento,
        valor_tratamiento=valor_tratamiento,
    )

    db.commit()

    return registro
"""
Tests de FUS-06/CU-07 — Consultar listado paginado de citas.
Un test por escenario Gherkin con implementación actual.

El Escenario 5 ("Acceder al detalle de una cita desde el listado")
queda sin test: depende de un endpoint de detalle individual de cita
que no existe todavía, sin HU propia identificada — documentado como
pendiente, no como olvido.
"""

from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def _crear_15_citas(db, crear_propietario, crear_mascota, crear_veterinario, crear_cita):
    propietario = crear_propietario(db, dni="12345678Z", nombre="Juan", apellidos="Pérez")
    mascota = crear_mascota(db, nombre="Rex", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Ana", apellidos="Martín Ruiz")

    base = datetime(2026, 7, 1, 9, 0)
    for i in range(15):
        crear_cita(
            db,
            fecha_hora=base + timedelta(hours=i),
            id_mascota=mascota.id_mascota,
            id_veterinario=veterinario.id_veterinario,
        )


def test_listado_primera_pagina_ordenado_descendente(
    client: TestClient, db: Session, crear_propietario, crear_mascota, crear_veterinario, crear_cita
):
    """Escenario: Consultar el listado de citas con resultados."""
    _crear_15_citas(db, crear_propietario, crear_mascota, crear_veterinario, crear_cita)

    response = client.get("/citas")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    fechas = [item["fecha_hora"] for item in data]
    assert fechas == sorted(fechas, reverse=True)


def test_listado_segunda_pagina(
    client: TestClient, db: Session, crear_propietario, crear_mascota, crear_veterinario, crear_cita
):
    """Escenario: Navegar a la siguiente página del listado."""
    _crear_15_citas(db, crear_propietario, crear_mascota, crear_veterinario, crear_cita)

    response = client.get("/citas", params={"pagina": 2})

    assert response.status_code == 200
    assert len(response.json()) == 5


def test_listado_vacio_sin_citas(client: TestClient):
    """Escenario: Consultar el listado sin citas registradas."""
    response = client.get("/citas")

    assert response.status_code == 200
    assert response.json() == []


def test_pagina_fuera_de_rango_devuelve_ultima_pagina_valida(
    client: TestClient, db: Session, crear_propietario, crear_mascota, crear_veterinario, crear_cita
):
    """Escenario: Solicitar una página fuera de rango."""
    _crear_15_citas(db, crear_propietario, crear_mascota, crear_veterinario, crear_cita)

    response = client.get("/citas", params={"pagina": 5})

    assert response.status_code == 200
    # con 15 citas y 10/página, la última página válida es la 2, con 5 citas
    assert len(response.json()) == 5
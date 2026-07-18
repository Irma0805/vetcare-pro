"""
Tests de FUS-08/CU-09 — Cancelar cita.
Un test por escenario Gherkin testable con la implementación actual.

El escenario "El horario de una cita cancelada queda disponible para
otra cita" está marcado @sujeto_a_disponibilidad en el Gherkin: no
existe todavía validación de solapamiento de horarios implementada
(decisión ya documentada, fuera de alcance por ahora), así que no
tiene test aquí.
"""

from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_cancelar_cita_futura_en_estado_agendada(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """
    Escenario: Cancelar correctamente una cita futura en estado agendada.
    Verifica también que la cita sigue visible en el listado con su
    nuevo estado (segunda aserción del Gherkin), no se elimina.
    """
    propietario = crear_propietario(db, dni="12345678Z", nombre="María", apellidos="López")
    mascota = crear_mascota(db, nombre="Toby", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    response = client.post(f"/citas/{cita.id_cita}/cancelar")

    assert response.status_code == 200
    assert response.json()["estado"] == "cancelada"

    listado = client.get("/citas")
    citas_en_listado = [c["id_cita"] for c in listado.json()]
    assert cita.id_cita in citas_en_listado


def test_cancelar_cita_ya_realizada(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """Escenario: Intento de cancelar una cita ya realizada."""
    propietario = crear_propietario(db, dni="87654321X", nombre="Carlos", apellidos="Pérez")
    mascota = crear_mascota(db, nombre="Rocky", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2020, 1, 1, 10, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    response = client.post(f"/citas/{cita.id_cita}/cancelar")

    assert response.status_code == 422


def test_cancelar_cita_ya_cancelada(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """Escenario: Intento de cancelar una cita ya cancelada."""
    propietario = crear_propietario(db, dni="11223344B", nombre="Ana", apellidos="Ruiz")
    mascota = crear_mascota(db, nombre="Luna", especie="Gata", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 25, 10, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
        estado="cancelada",
    )

    response = client.post(f"/citas/{cita.id_cita}/cancelar")

    assert response.status_code == 422


def test_cancelar_cita_no_encontrada(client: TestClient):
    """
    Caso no cubierto explícitamente por el Gherkin, pero manejado:
    cita_id inexistente -> 404 (mismo criterio que otros CU).
    """
    response = client.post("/citas/99999/cancelar")

    assert response.status_code == 404
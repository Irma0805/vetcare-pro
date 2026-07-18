"""
Tests de FUS-04/CU-05 — Registrar diagnóstico sobre una cita.
Un test por escenario Gherkin.
"""

from datetime import datetime, timezone

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_registrar_diagnostico_en_cita_ya_realizada(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """Escenario: Registrar diagnóstico en una cita ya realizada."""
    propietario = crear_propietario(db, dni="12345678Z", nombre="María", apellidos="López")
    mascota = crear_mascota(db, nombre="Toby", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 1, 10, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    payload = {"diagnostico": "Otitis leve en oído derecho, se pauta tratamiento tópico"}
    response = client.patch(f"/citas/{cita.id_cita}/diagnostico", json=payload)

    assert response.status_code == 200
    assert response.json()["diagnostico"] == "Otitis leve en oído derecho, se pauta tratamiento tópico"


def test_registrar_diagnostico_en_cita_futura(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """Escenario: Intento de registrar diagnóstico en una cita futura."""
    propietario = crear_propietario(db, dni="87654321X", nombre="Carlos", apellidos="Pérez")
    mascota = crear_mascota(db, nombre="Luna", especie="Gata", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 9, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    payload = {"diagnostico": "Intento sobre cita futura"}
    response = client.patch(f"/citas/{cita.id_cita}/diagnostico", json=payload)

    assert response.status_code == 422


def test_editar_diagnostico_ya_registrado(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """Escenario: Editar un diagnóstico ya registrado."""
    propietario = crear_propietario(db, dni="11223344B", nombre="Ana", apellidos="Ruiz")
    mascota = crear_mascota(db, nombre="Rocky", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 1, 10, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )
    cita.diagnostico = "Revisión rutinaria sin hallazgos"
    db.flush()

    payload = {"diagnostico": "Revisión rutinaria, se detecta sobrepeso leve, se recomienda ajuste de dieta"}
    response = client.patch(f"/citas/{cita.id_cita}/diagnostico", json=payload)

    assert response.status_code == 200
    assert response.json()["diagnostico"] == "Revisión rutinaria, se detecta sobrepeso leve, se recomienda ajuste de dieta"


def test_guardar_diagnostico_vacio(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """
    Escenario: Intento de guardar un diagnóstico vacío.
    Bloqueado a nivel de schema (Field(min_length=1)) -> 422
    automático de Pydantic, equivalente al bloqueo de formulario
    descrito en el Gherkin (verificado aquí a nivel de API).
    """
    propietario = crear_propietario(db, dni="99887766P", nombre="Sofía", apellidos="Torres")
    mascota = crear_mascota(db, nombre="Max", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 1, 10, 0, tzinfo=timezone.utc),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    payload = {"diagnostico": ""}
    response = client.patch(f"/citas/{cita.id_cita}/diagnostico", json=payload)

    assert response.status_code == 422
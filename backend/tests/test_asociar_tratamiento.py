"""
Tests de FUS-05/CU-06 — Asociar tratamiento a una cita.
Un test por escenario Gherkin con implementación actual.
"""

from datetime import date, datetime
from decimal import Decimal

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_asociar_tratamiento_con_peso_registrado(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita, crear_tratamiento,
):
    """Escenario: Asociar un tratamiento a una cita cuya mascota tiene peso registrado."""
    propietario = crear_propietario(db, dni="12345678Z", nombre="María", apellidos="López")
    mascota = crear_mascota(
        db, nombre="Toby", especie="Perro", id_propietario=propietario.id_propietario,
        peso=Decimal("8.00"),
    )
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )
    tratamiento = crear_tratamiento(
        db, nombre="Antiparasitario", tipo_tratamiento="Preventivo",
        descripcion="Tratamiento antiparasitario", tarifa_por_kg=Decimal("2.00"),
    )

    payload = {
        "id_tratamiento": tratamiento.id_tratamiento,
        "fecha_inicio": "2026-07-05",
        "fecha_fin": "2026-07-19",
        "dosis": "1 comprimido",
        "seguimiento": "revisión en 15 días",
    }
    response = client.post(f"/citas/{cita.id_cita}/tratamientos", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["id_cita"] == cita.id_cita
    assert data["id_tratamiento"] == tratamiento.id_tratamiento
    assert data["valor_tratamiento"] == "16.00"


def test_asociar_tratamiento_sin_peso_registrado(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita, crear_tratamiento,
):
    """Escenario: Asociar un tratamiento a una cita cuya mascota no tiene peso registrado."""
    propietario = crear_propietario(db, dni="87654321X", nombre="Carlos", apellidos="Pérez")
    mascota = crear_mascota(db, nombre="Rocky", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )
    tratamiento = crear_tratamiento(
        db, nombre="Cura de herida", tipo_tratamiento="Curativo",
        descripcion="Cura de herida superficial", tarifa_por_kg=Decimal("3.00"),
    )

    payload = {
        "id_tratamiento": tratamiento.id_tratamiento,
        "fecha_inicio": "2026-07-05",
        "fecha_fin": "2026-07-19",
        "dosis": "Aplicación tópica",
        "seguimiento": None,
    }
    response = client.post(f"/citas/{cita.id_cita}/tratamientos", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["valor_tratamiento"] is None


def test_asociar_varios_tratamientos_a_la_misma_cita(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita, crear_tratamiento,
):
    """Escenario: Asociar varios tratamientos distintos a la misma cita."""
    propietario = crear_propietario(db, dni="11223344B", nombre="Ana", apellidos="Ruiz")
    mascota = crear_mascota(
        db, nombre="Luna", especie="Gata", id_propietario=propietario.id_propietario,
        peso=Decimal("4.00"),
    )
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )
    cura = crear_tratamiento(
        db, nombre="Cura de herida", tipo_tratamiento="Curativo",
        descripcion="Cura de herida superficial", tarifa_por_kg=Decimal("3.00"),
    )
    antiparasitario = crear_tratamiento(
        db, nombre="Antiparasitario", tipo_tratamiento="Preventivo",
        descripcion="Tratamiento antiparasitario", tarifa_por_kg=Decimal("2.00"),
    )

    payload_base = {
        "fecha_inicio": "2026-07-05", "fecha_fin": "2026-07-19",
        "dosis": "según indicación", "seguimiento": None,
    }

    respuesta_1 = client.post(
        f"/citas/{cita.id_cita}/tratamientos",
        json={**payload_base, "id_tratamiento": cura.id_tratamiento},
    )
    respuesta_2 = client.post(
        f"/citas/{cita.id_cita}/tratamientos",
        json={**payload_base, "id_tratamiento": antiparasitario.id_tratamiento},
    )

    assert respuesta_1.status_code == 201
    assert respuesta_2.status_code == 201
    assert respuesta_1.json()["id_citas_tratamientos"] != respuesta_2.json()["id_citas_tratamientos"]


def test_asociar_tratamiento_sin_seleccionarlo(
    client: TestClient, db: Session, crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """
    Escenario: Intento de asociar un tratamiento sin seleccionarlo del catálogo.
    id_tratamiento es un campo obligatorio del schema: su ausencia produce
    un 422 automático de Pydantic, equivalente al bloqueo de formulario
    descrito en el Gherkin (aquí verificado a nivel de API, no de UI).
    """
    propietario = crear_propietario(db, dni="55667788Z", nombre="Pedro", apellidos="Gómez")
    mascota = crear_mascota(db, nombre="Nube", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    payload = {
        "fecha_inicio": "2026-07-05", "fecha_fin": "2026-07-19",
        "dosis": "1 comprimido", "seguimiento": None,
    }
    response = client.post(f"/citas/{cita.id_cita}/tratamientos", json=payload)

    assert response.status_code == 422


def test_asociar_tratamiento_fecha_fin_anterior_a_inicio(
    client: TestClient, db: Session,
    crear_propietario, crear_mascota, crear_veterinario, crear_cita, crear_tratamiento,
):
    """Escenario: Intento de asociar un tratamiento con fecha de fin anterior a la fecha de inicio."""
    propietario = crear_propietario(db, dni="99887766P", nombre="Sofía", apellidos="Torres")
    mascota = crear_mascota(db, nombre="Max", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )
    tratamiento = crear_tratamiento(
        db, nombre="Antiparasitario", tipo_tratamiento="Preventivo",
        descripcion="Tratamiento antiparasitario", tarifa_por_kg=Decimal("2.00"),
    )

    payload = {
        "id_tratamiento": tratamiento.id_tratamiento,
        "fecha_inicio": "2026-07-20", "fecha_fin": "2026-07-15",
        "dosis": "1 comprimido", "seguimiento": None,
    }
    response = client.post(f"/citas/{cita.id_cita}/tratamientos", json=payload)

    assert response.status_code == 422


def test_asociar_tratamiento_cita_no_encontrada(client: TestClient, db: Session, crear_tratamiento):
    """
    Caso no cubierto explícitamente por el Gherkin, pero manejado:
    cita_id inexistente -> 404 (mismo criterio que fichas de cliente/mascota).
    """
    tratamiento = crear_tratamiento(
        db, nombre="Antiparasitario", tipo_tratamiento="Preventivo",
        descripcion="Tratamiento antiparasitario", tarifa_por_kg=Decimal("2.00"),
    )
    payload = {
        "id_tratamiento": tratamiento.id_tratamiento,
        "fecha_inicio": "2026-07-05", "fecha_fin": "2026-07-19",
        "dosis": "1 comprimido", "seguimiento": None,
    }
    response = client.post("/citas/99999/tratamientos", json=payload)

    assert response.status_code == 404


def test_asociar_tratamiento_no_encontrado(
    client: TestClient, db: Session, crear_propietario, crear_mascota, crear_veterinario, crear_cita,
):
    """
    Caso no cubierto explícitamente por el Gherkin, pero manejado:
    id_tratamiento inexistente -> 404.
    """
    propietario = crear_propietario(db, dni="66778899D", nombre="Elena", apellidos="Vidal")
    mascota = crear_mascota(db, nombre="Coco", especie="Ave", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Laura", apellidos="Fernández")
    cita = crear_cita(
        db, fecha_hora=datetime(2026, 7, 20, 10, 0),
        id_mascota=mascota.id_mascota, id_veterinario=veterinario.id_veterinario,
    )

    payload = {
        "id_tratamiento": 99999,
        "fecha_inicio": "2026-07-05", "fecha_fin": "2026-07-19",
        "dosis": "1 comprimido", "seguimiento": None,
    }
    response = client.post(f"/citas/{cita.id_cita}/tratamientos", json=payload)

    assert response.status_code == 404
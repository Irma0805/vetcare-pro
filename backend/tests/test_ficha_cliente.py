"""
Tests de FUS-13/CU-14 — Consultar ficha de cliente.
Un test por escenario Gherkin con implementación actual.

El Escenario 3 ("Acceder a la ficha de una mascota desde la ficha del
cliente") queda sin test: depende de GET /mascotas/{id} (FUS-16),
todavía no implementado — documentado como pendiente, no como olvido.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_ficha_cliente_con_mascotas_activas_e_inactivas(
    client: TestClient, db: Session, crear_propietario, crear_mascota
):
    """Escenario: Consultar la ficha de un cliente con mascotas asociadas."""
    propietario = crear_propietario(
        db, dni="12345678Z", nombre="María", apellidos="López",
        direccion="Calle Falsa 123", telefono="600111222", email="maria@test.com",
    )
    crear_mascota(db, nombre="Toby", especie="Perro", id_propietario=propietario.id_propietario)
    crear_mascota(db, nombre="Rocky", especie="Gato", id_propietario=propietario.id_propietario, activo=False)

    response = client.get(f"/propietarios/{propietario.id_propietario}")

    assert response.status_code == 200
    data = response.json()
    assert data["dni"] == "12345678Z"
    assert data["nombre"] == "María"
    assert data["apellidos"] == "López"
    assert data["direccion"] == "Calle Falsa 123"
    assert data["telefono"] == "600111222"
    assert data["email"] == "maria@test.com"

    nombres_mascotas = [m["nombre"] for m in data["mascotas"]]
    assert set(nombres_mascotas) == {"Toby", "Rocky"}  # activa e inactiva, ambas visibles


def test_ficha_cliente_sin_mascotas(client: TestClient, db: Session, crear_propietario):
    """Escenario: Consultar la ficha de un cliente sin mascotas asociadas."""
    propietario = crear_propietario(db, dni="87654321X", nombre="Carlos", apellidos="Pérez")

    response = client.get(f"/propietarios/{propietario.id_propietario}")

    assert response.status_code == 200
    data = response.json()
    assert data["mascotas"] == []


def test_ficha_cliente_no_encontrado(client: TestClient):
    """
    Caso no cubierto explícitamente por el Gherkin, pero manejado:
    id_propietario inexistente -> 404.
    """
    response = client.get("/propietarios/99999")

    assert response.status_code == 404
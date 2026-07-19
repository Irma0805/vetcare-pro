"""
Tests de FUS-20/CU-21 — Consultar/listar veterinarios.
Un test por escenario Gherkin con implementación actual.

El Escenario 4 ("Acceder a la ficha de un veterinario desde el
listado") queda sin test: depende de FUS-21/CU-22 (ficha individual),
todavía no implementada — documentado como pendiente, no como olvido.
"""

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient


def test_listado_ordenado_alfabeticamente_por_apellidos(
    client: TestClient, db: Session, crear_veterinario
):
    """Escenario: Consultar el listado de veterinarios activos."""
    crear_veterinario(db, nombre="Ana", apellidos="Martín Ruiz")
    crear_veterinario(db, nombre="Luis", apellidos="Gómez Díaz")

    response = client.get("/veterinarios")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    # "Gómez Díaz" va antes que "Martín Ruiz" alfabéticamente
    assert data[0]["apellidos"] == "Gómez Díaz"
    assert data[1]["apellidos"] == "Martín Ruiz"


def test_listado_excluye_veterinarios_dados_de_baja(
    client: TestClient, db: Session, crear_veterinario
):
    """Escenario: El listado no muestra veterinarios dados de baja."""
    crear_veterinario(db, nombre="Pedro", apellidos="Sánchez", activo=False)

    response = client.get("/veterinarios")

    assert response.status_code == 200
    data = response.json()
    apellidos_listados = [v["apellidos"] for v in data]
    assert "Sánchez" not in apellidos_listados


def test_listado_vacio_sin_veterinarios_activos(client: TestClient):
    """Escenario: Consultar el listado sin veterinarios activos."""
    response = client.get("/veterinarios")

    assert response.status_code == 200
    assert response.json() == []
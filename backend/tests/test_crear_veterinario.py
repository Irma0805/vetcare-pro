"""
Tests de FUS-19/CU-20 — Crear veterinario.
Un test por escenario Gherkin (fase 6 del ciclo BDD, nunca aplazada).
"""

from fastapi.testclient import TestClient


def test_crear_veterinario_con_especialidad(client: TestClient):
    """Escenario: Crear un veterinario con especialidad."""
    payload = {"nombre": "Ana", "apellidos": "Martín Ruiz", "especialidad": "Cirugía"}

    response = client.post("/veterinarios", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Ana"
    assert data["apellidos"] == "Martín Ruiz"
    assert data["especialidad"] == "Cirugía"
    assert data["activo"] is True
    assert "id_veterinario" in data


def test_crear_veterinario_sin_especialidad(client: TestClient):
    """Escenario: Crear un veterinario sin especialidad (medicina general)."""
    payload = {"nombre": "Luis", "apellidos": "Gómez Díaz"}

    response = client.post("/veterinarios", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Luis"
    assert data["apellidos"] == "Gómez Díaz"
    assert data["especialidad"] is None
    assert data["activo"] is True


def test_crear_veterinario_sin_apellidos(client: TestClient):
    """Escenario: Intentar crear un veterinario sin apellidos."""
    payload = {"nombre": "Marta", "apellidos": ""}

    response = client.post("/veterinarios", json=payload)

    assert response.status_code == 422
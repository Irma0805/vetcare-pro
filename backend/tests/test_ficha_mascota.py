"""
Tests de FUS-16/CU-17 — Consultar ficha de mascota.
Un test por escenario Gherkin con implementación actual.

El Escenario 3 solo cubre la primera aserción (indicador de
inactiva en la propia ficha). La segunda parte del escenario
("Michi" no aparece como opción seleccionable en la creación de
cita) es responsabilidad de CU-04, no de CU-17 — se documenta como
pendiente de test cruzado, no como olvido.

El Escenario 4 (acceso al historial clínico) no requiere test aquí:
es una decisión de navegación en frontend (enlace a un endpoint
propio de FUS-11), no un dato que FichaMascotaResponse deba exponer.
"""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_ficha_mascota_activa_con_peso_registrado(
    client: TestClient, db: Session, crear_propietario, crear_mascota
):
    """Escenario: Consultar la ficha de una mascota activa con peso registrado."""
    propietario = crear_propietario(
        db, dni="12345678Z", nombre="María", apellidos="López García",
    )
    mascota = crear_mascota(
        db, nombre="Toby", especie="Perro", id_propietario=propietario.id_propietario,
        raza="Labrador", peso=12.5,
    )

    response = client.get(f"/mascotas/{mascota.id_mascota}")

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Toby"
    assert data["especie"] == "Perro"
    assert data["raza"] == "Labrador"
    assert data["peso"] == "12.50"
    assert data["activo"] is True
    assert data["propietario"]["id_propietario"] == propietario.id_propietario
    assert data["propietario"]["nombre"] == "María"
    assert data["propietario"]["apellidos"] == "López García"


def test_ficha_mascota_sin_peso_registrado(
    client: TestClient, db: Session, crear_propietario, crear_mascota
):
    """Escenario: Consultar la ficha de una mascota sin peso registrado."""
    propietario = crear_propietario(db, dni="87654321X", nombre="Carlos", apellidos="Pérez")
    mascota = crear_mascota(
        db, nombre="Rocky", especie="Perro", id_propietario=propietario.id_propietario,
    )

    response = client.get(f"/mascotas/{mascota.id_mascota}")

    assert response.status_code == 200
    data = response.json()
    assert data["peso"] is None


def test_ficha_mascota_dada_de_baja(
    client: TestClient, db: Session, crear_propietario, crear_mascota
):
    """Escenario: Consultar la ficha de una mascota dada de baja."""
    propietario = crear_propietario(db, dni="11223344B", nombre="Ana", apellidos="Ruiz")
    mascota = crear_mascota(
        db, nombre="Michi", especie="Gato", id_propietario=propietario.id_propietario,
        activo=False,
    )

    response = client.get(f"/mascotas/{mascota.id_mascota}")

    assert response.status_code == 200
    data = response.json()
    assert data["activo"] is False


def test_ficha_mascota_no_encontrada(client: TestClient):
    """
    Caso no cubierto explícitamente por el Gherkin, pero manejado:
    mascota_id inexistente -> 404 (mismo criterio que ficha de
    cliente, FUS-13).
    """
    response = client.get("/mascotas/99999")

    assert response.status_code == 404
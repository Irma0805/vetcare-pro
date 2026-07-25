"""
Tests para la búsqueda de Propietario por DNI (FUS-03/CU-04).
"""


def test_buscar_propietario_dni_existente(client, db, crear_propietario):
    """DNI existente y activo → 200 con los datos del propietario."""
    crear_propietario(db, dni="12345678Z", nombre="Ana", apellidos="García Ruiz")

    response = client.get("/propietarios", params={"dni": "12345678Z"})

    assert response.status_code == 200
    body = response.json()
    assert body["dni"] == "12345678Z"
    assert body["nombre"] == "Ana"
    assert body["activo"] is True


def test_buscar_propietario_dni_inexistente(client, db):
    """DNI que no existe en la base de datos → 200 con cuerpo null."""
    response = client.get("/propietarios", params={"dni": "00000000A"})

    assert response.status_code == 200
    assert response.json() is None


def test_buscar_propietario_sin_dni(client, db):
    """Sin el parámetro dni → 422, el campo es obligatorio."""
    response = client.get("/propietarios")

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "dni"]


def test_buscar_propietario_dni_inactivo(client, db, crear_propietario):
    """
    Propietario dado de baja → sigue siendo encontrado por su DNI,
    con activo=False en la respuesta (no se oculta como si no
    existiera, mismo criterio ya aplicado a Mascota en FUS-18).
    """
    crear_propietario(
        db, dni="87654321X", nombre="Luis", apellidos="Pérez Sanz", activo=False,
    )

    response = client.get("/propietarios", params={"dni": "87654321X"})

    assert response.status_code == 200
    body = response.json()
    assert body["dni"] == "87654321X"
    assert body["activo"] is False
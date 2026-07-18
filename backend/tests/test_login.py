def test_login_exitoso_con_credenciales_validas(client, db, crear_usuario):
    """Gherkin: Login exitoso con credenciales válidas."""
    crear_usuario(db, "admin", "clave123")

    response = client.post("/login", json={"username": "admin", "password": "clave123"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fallido_por_contrasena_incorrecta(client, db, crear_usuario):
    """Gherkin: Login fallido por contraseña incorrecta."""
    crear_usuario(db, "admin", "clave123")

    response = client.post("/login", json={"username": "admin", "password": "incorrecta"})

    assert response.status_code == 401
    assert response.json()["detail"] == "usuario o contraseña incorrectos"


def test_login_fallido_por_usuario_inexistente(client):
    """Gherkin: Login fallido por usuario inexistente."""
    response = client.post("/login", json={"username": "desconocido", "password": "cualquiera"})

    assert response.status_code == 401
    assert response.json()["detail"] == "usuario o contraseña incorrectos"


def test_login_fallido_por_usuario_desactivado(client, db, crear_usuario):
    """Gherkin: Login fallido por usuario desactivado."""
    crear_usuario(db, "admin", "clave123", activo=False)

    response = client.post("/login", json={"username": "admin", "password": "clave123"})

    assert response.status_code == 401
    assert response.json()["detail"] == "usuario o contraseña incorrectos"


def test_login_con_campos_vacios(client):
    """
    Gherkin: Intento de login con campos vacíos.
    El Gherkin describe el bloqueo en el FRONTEND (no llega petición al
    backend). Este test verifica la defensa en profundidad del backend:
    si la petición llegara igualmente, debe rechazarse con un error de
    validación (422), nunca aceptarse ni tratarse como credenciales
    válidas o inválidas de negocio (401).
    """
    response = client.post("/login", json={"username": "", "password": ""})

    assert response.status_code == 422
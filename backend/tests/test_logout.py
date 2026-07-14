import uuid
from app.service.usuario import create_session, update_last_activity, verify_active_session
from datetime import datetime, timedelta, timezone
from freezegun import freeze_time


def test_logout_exitoso(client, db, crear_usuario):
    """Gherkin: Cierre de sesión exitoso."""
    crear_usuario(db, "admin", "clave123")
    login_response = client.post("/login", json={"username": "admin", "password": "clave123"})
    token = login_response.json()["access_token"]

    response = client.post("/logout", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["message"] == "Sesión cerrada correctamente"


def test_uso_de_token_ya_invalidado(client, db, crear_usuario):
    """Gherkin: Uso de un token ya invalidado."""
    crear_usuario(db, "admin", "clave123")
    login_response = client.post("/login", json={"username": "admin", "password": "clave123"})
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post("/logout", headers=headers)

    response = client.post("/logout", headers=headers)

    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudo validar la sesión"


def test_sesion_expira_por_inactividad(client, db, crear_usuario):
    """
    Gherkin: Sesión expira tras superar el tiempo de inactividad.
    También cubre "Mensaje de sesión expirada diferenciado del error
    de login" (mismo detail, ya distinto del de login) — no se separa
    en otro test por no aportar cobertura nueva (YAGNI).
    """
    inicio = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with freeze_time(inicio) as tiempo_congelado:
        crear_usuario(db, "admin", "clave123")
        login_response = client.post("/login", json={"username": "admin", "password": "clave123"})
        token = login_response.json()["access_token"]

        tiempo_congelado.move_to(inicio + timedelta(minutes=16))

        response = client.post("/logout", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json()["detail"] == "No se pudo validar la sesión"


def test_sesion_no_expira_con_actividad_continua(db):
    """
    Gherkin: La sesión no expira si hay actividad continua.

    Test a nivel de service (Opción A): no existe hoy ningún
    endpoint protegido no-destructivo con el que simular "una petición
    válida cada 10 minutos" vía HTTP sin invalidar la sesión de paso
    (el único endpoint protegido, /logout, invalidaría la sesión en la
    primera llamada). Se prueba directamente el mecanismo de sliding
    expiration: verify_active_session() + update_last_activity(), que
    es lo que get_current_user() invoca en cada petición real.
    """
    jti = str(uuid.uuid4())
    inicio = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

    with freeze_time(inicio) as tiempo_congelado:
        create_session(db, jti)

        tiempo_congelado.move_to(inicio + timedelta(minutes=10))
        assert verify_active_session(db, jti) is True
        update_last_activity(db, jti)

        tiempo_congelado.move_to(inicio + timedelta(minutes=20))
        assert verify_active_session(db, jti) is True
        update_last_activity(db, jti)

        tiempo_congelado.move_to(inicio + timedelta(minutes=28))
        assert verify_active_session(db, jti) is True
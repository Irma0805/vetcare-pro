from sqlalchemy.orm import Session

from app.service.usuario import (
    authenticate_user,
    create_session,
    invalidate_session,
    verify_active_session,
    update_last_activity,
)
from app.validation.security import create_access_token, decode_access_token
from app.schemas.usuario import TokenResponse, LogoutResponse


def login(db: Session, username: str, password: str) -> TokenResponse | None:
    """
    Orquesta el login (FUS-01/CU-01): verifica credenciales a través
    del service, genera el JWT (validation/security.py) y registra la
    sesión nueva. Devuelve None ante credenciales inválidas — es el
    router quien decide el código HTTP 401, no esta función.
    """
    usuario = authenticate_user(db, username, password)

    if usuario is None:
        return None

    access_token, jti = create_access_token(usuario.username)
    create_session(db, jti)

    return TokenResponse(access_token=access_token)


def logout(db: Session, jti: str) -> LogoutResponse:
    """
    Orquesta el logout (FUS-02/CU-02): invalida la sesión actual a
    través del service.
    """
    invalidate_session(db, jti)
    return LogoutResponse()


def obtener_usuario_actual(db: Session, token: str) -> dict | None:
    """
    Orquesta la verificación de sesión en cada petición protegida
    (invocada desde get_current_user en dependencies.py): decodifica
    el JWT (validation/security.py), comprueba que la sesión sigue
    activa y renueva la última actividad (sliding expiration, ADR-006).
    Devuelve None ante CUALQUIER motivo de rechazo — es dependencies.py
    quien decide lanzar el 401, con el mismo mensaje genérico de
    siempre, sin distinguir el motivo real.
    """
    datos_token = decode_access_token(token)

    if datos_token is None:
        return None

    jti = datos_token["jti"]

    if not verify_active_session(db, jti):
        return None

    update_last_activity(db, jti)

    return datos_token
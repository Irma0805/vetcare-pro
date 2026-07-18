import uuid
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError

from app.config import settings


def create_access_token(username: str) -> tuple[str, str]:
    """
    Genera un JWT firmado para el usuario autenticado, con expiración
    a los settings.jwt_access_token_expire_minutes minutos (ADR-006).
    Devuelve una tupla (token, jti): el jti se expone hacia fuera para
    que el controlador pueda registrar la sesión en sesiones_invalidadas
    justo después del login (FUS-02/TUS-01).
    """
    now = datetime.now(timezone.utc)
    jti = str(uuid.uuid4())
    payload = {
        "sub": username,
        "jti": jti,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, jti


def decode_access_token(token: str) -> dict | None:
    """
    Decodifica y valida un JWT (verificado contra el tutorial oficial
    de FastAPI, "OAuth2 with Password and Bearer with JWT tokens").
    Devuelve {"username": ..., "jti": ...} si el token es válido y
    contiene los claims esperados, o None ante CUALQUIER motivo de
    rechazo (firma inválida, token expirado, o claims ausentes) —
    mismo criterio de no distinguir el motivo que ya usan
    authenticate_user() y verify_active_session() en el resto del
    proyecto. Es la capa de arriba (controlador) quien decide qué
    código HTTP corresponde a un None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except InvalidTokenError:
        return None

    username = payload.get("sub")
    jti = payload.get("jti")

    if username is None or jti is None:
        return None

    return {"username": username, "jti": jti}
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.usuario import Usuario
from app.validation.password import verify_password


def authenticate_user(db: Session, username: str, password: str) -> Usuario | None:
    """
    Verifica las credenciales de login (CU-01).
    Devuelve el Usuario si son válidas, o None ante CUALQUIER motivo de
    rechazo (no existe, inactivo, contraseña incorrecta) — nunca se
    distingue el motivo aquí, para no filtrar esa información más arriba.
    """
    usuario = db.execute(
        select(Usuario).where(Usuario.username == username)
    ).scalar_one_or_none()

    if usuario is None:
        return None

    if not usuario.activo:
        return None

    if not verify_password(password, usuario.password_hash):
        return None

    return usuario


def create_access_token(username: str) -> str:
    """
    Genera un JWT firmado para el usuario autenticado, con expiración
    a los settings.jwt_access_token_expire_minutes minutos (ADR-006).
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
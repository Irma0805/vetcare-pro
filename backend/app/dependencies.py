from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
import jwt

from app.config import settings
from app.controlador.usuario import verify_active_session, update_last_activity
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> dict:
    """
    Dependencia de FastAPI que protege endpoints autenticados.
    Decodifica el JWT (verificado contra el tutorial oficial de FastAPI,
    OAuth2 with Password and Bearer with JWT tokens), comprueba la
    sesión contra sesiones_invalidadas (ADR-006) y renueva la última
    actividad si sigue siendo válida.

    Devuelve un diccionario mínimo {username, jti} — no consulta la
    tabla Usuario completa (YAGNI: administrador único, sin roles,
    ADR-002).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar la sesión",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        username = payload.get("sub")
        jti = payload.get("jti")

        if username is None or jti is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    if not verify_active_session(db, jti):
        raise credentials_exception

    update_last_activity(db, jti)

    return {"username": username, "jti": jti}
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.controlador.usuario import obtener_usuario_actual
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> dict:
    """
    Dependencia de FastAPI que protege endpoints autenticados.
    Delega toda la lógica (decodificar JWT, verificar sesión, renovar
    actividad) en controlador.obtener_usuario_actual — esta función
    solo traduce el resultado a HTTP: 401 genérico si es None, o
    {"username", "jti"} si la sesión es válida (YAGNI: administrador
    único, sin roles, ADR-002, no se consulta la tabla Usuario completa).
    """
    resultado = obtener_usuario_actual(db, token)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar la sesión",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return resultado
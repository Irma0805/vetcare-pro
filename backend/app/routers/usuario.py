from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controlador.usuario import (
    authenticate_user,
    create_access_token,
    create_session,
    invalidate_session,
)
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas.usuario import LoginRequest, TokenResponse, LogoutResponse

router = APIRouter(tags=["Acceso al sistema"])


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login (FUS-01/CU-01).
    Devuelve un token JWT si las credenciales son válidas; si no,
    responde 401 con un mensaje genérico, sin distinguir el motivo.
    Registra la sesión nueva en sesiones_invalidadas (ADR-006), base
    para el logout (FUS-02) y la expiración por inactividad (TUS-01).
    """
    usuario = authenticate_user(db, credentials.username, credentials.password)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="usuario o contraseña incorrectos",
        )

    access_token, jti = create_access_token(usuario.username)
    create_session(db, jti)

    return TokenResponse(access_token=access_token)


@router.post("/logout", response_model=LogoutResponse)
def logout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Endpoint de logout (FUS-02/CU-02).
    Requiere sesión activa (protegido por get_current_user). Invalida
    la sesión actual en sesiones_invalidadas — cualquier petición
    posterior con ese mismo token será rechazada (ADR-006).
    """
    invalidate_session(db, current_user["jti"])
    return LogoutResponse()
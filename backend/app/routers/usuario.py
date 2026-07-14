from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controlador.usuario import login as login_controlador, logout as logout_controlador
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
    Toda la lógica (verificar credenciales, generar token, registrar
    la sesión) vive en controlador.usuario.login — este endpoint solo
    traduce el resultado a HTTP.
    """
    resultado = login_controlador(db, credentials.username, credentials.password)

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="usuario o contraseña incorrectos",
        )

    return resultado


@router.post("/logout", response_model=LogoutResponse)
def logout(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Endpoint de logout (FUS-02/CU-02).
    Requiere sesión activa (protegido por get_current_user). Toda la
    lógica de invalidar la sesión vive en controlador.usuario.logout.
    """
    return logout_controlador(db, current_user["jti"])
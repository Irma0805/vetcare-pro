from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controlador.usuario import authenticate_user, create_access_token
from app.database import get_db
from app.schemas.usuario import LoginRequest, TokenResponse

router = APIRouter(tags=["Acceso al sistema"])


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Endpoint de login (FUS-01/CU-01).
    Devuelve un token JWT si las credenciales son válidas; si no,
    responde 401 con un mensaje genérico, sin distinguir el motivo.
    """
    usuario = authenticate_user(db, credentials.username, credentials.password)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="usuario o contraseña incorrectos",
        )

    access_token = create_access_token(usuario.username)
    return TokenResponse(access_token=access_token)
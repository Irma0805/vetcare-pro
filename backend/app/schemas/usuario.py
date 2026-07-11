from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    Datos que el frontend envía al intentar iniciar sesión (FUS-01/CU-01).
    """
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """
    Respuesta que el backend devuelve tras un login exitoso.
    Nunca incluye el password_hash ni ningún otro dato sensible del Usuario.
    """
    access_token: str
    token_type: str = "bearer"
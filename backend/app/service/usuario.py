from datetime import datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models.usuario import Usuario
from app.models.sesion_invalidada import SesionInvalidada
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


def create_session(db: Session, jti: str) -> None:
    """
    Crea el registro inicial de una sesión nueva en sesiones_invalidadas
    (ADR-006). Se invoca justo después de generar el JWT en el login,
    con invalidado=False y la fecha de última actividad en el momento
    de creación — necesario para que la primera petición protegida
    posterior encuentre una fila con la que comparar (CU-02, CU-03).
    """
    sesion = SesionInvalidada(
        jti=jti,
        fecha_ultima_actividad=datetime.now(timezone.utc),
    )
    db.add(sesion)
    db.commit()


def invalidate_session(db: Session, jti: str) -> None:
    """
    Marca una sesión como invalidada (FUS-02/CU-02, logout explícito).
    No borra la fila — la conserva marcada como invalidado=True, para
    que cualquier petición posterior con ese jti sea rechazada de forma
    permanente, sin posibilidad de reactivarla (mismo criterio que el
    resto de bajas lógicas del proyecto: sin reactivación en el MVP).
    """
    sesion = db.get(SesionInvalidada, jti)

    if sesion is not None:
        sesion.invalidado = True
        db.commit()


def update_last_activity(db: Session, jti: str) -> None:
    """
    Actualiza la fecha de última actividad de una sesión (ADR-006).
    Se invoca justo después de que verify_active_session confirme que
    la sesión sigue siendo válida — es el mecanismo real de "sliding
    expiration": cada petición autenticada renueva el contador de
    inactividad de 15 minutos.
    """
    sesion = db.get(SesionInvalidada, jti)

    if sesion is not None:
        sesion.fecha_ultima_actividad = datetime.now(timezone.utc)
        db.commit()


def verify_active_session(db: Session, jti: str) -> bool:
    """
    Comprueba si una sesión sigue siendo válida (usado en cada petición
    protegida, dentro de la orquestación del controlador).

    Devuelve False ante CUALQUIER motivo de rechazo (no existe, ya
    invalidada, o expirada por inactividad) — mismo criterio de no
    distinguir el motivo que ya usa authenticate_user() en el login.

    Si detecta expiración por inactividad, marca la sesión como
    invalidada de paso (TUS-01/CU-03), para que quede registrado y no
    haya que volver a calcularlo en la siguiente petición.
    """
    sesion = db.get(SesionInvalidada, jti)

    if sesion is None:
        return False

    if sesion.invalidado:
        return False

    limite_inactividad = timedelta(minutes=settings.session_inactivity_timeout_minutes)
    ahora = datetime.now(timezone.utc)

    if ahora - sesion.fecha_ultima_actividad > limite_inactividad:
        sesion.invalidado = True
        db.commit()
        return False

    return True
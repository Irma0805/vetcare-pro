from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SesionInvalidada(Base):
    """
    Registro de sesiones (JWT) que el sistema debe rechazar.

    No almacena todas las sesiones activas — solo aquellas que han sido
    invalidadas explícitamente (logout, CU-02) o cuya última actividad
    ha superado el tiempo de inactividad permitido (expiración deslizante,
    CU-03). Ver ADR-006.
    """

    __tablename__ = "sesiones_invalidadas"

    jti: Mapped[str] = mapped_column(String(36), primary_key=True)
    fecha_ultima_actividad: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    invalidado: Mapped[bool] = mapped_column(Boolean, default=False)
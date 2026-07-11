from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Usuario(Base):
    """
    Representa al administrador único del sistema (ADR-002).
    No existe tabla Rol ni relación con Veterinario: la autenticación
    está completamente desacoplada del personal clínico.
    """
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
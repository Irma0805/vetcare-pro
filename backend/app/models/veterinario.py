from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Veterinario(Base):
    __tablename__ = "veterinarios"

    id_veterinario: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    apellidos: Mapped[str] = mapped_column(String(50))
    especialidad: Mapped[Optional[str]] = mapped_column(String(50))
    activo: Mapped[bool] = mapped_column(default=True)

    def __repr__(self) -> str:
        return f"Veterinario(id={self.id_veterinario!r}, nombre={self.nombre!r}, apellidos={self.apellidos!r})"
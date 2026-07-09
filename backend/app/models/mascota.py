from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Mascota(Base):
    __tablename__ = "mascotas"

    id_mascota: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
    especie: Mapped[str] = mapped_column(String(50))
    raza: Mapped[Optional[str]] = mapped_column(String(50))
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date)
    peso: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    activo: Mapped[bool] = mapped_column(default=True)
    id_propietario: Mapped[int] = mapped_column(ForeignKey("propietarios.id_propietario"))

    def __repr__(self) -> str:
        return f"Mascota(id={self.id_mascota!r}, nombre={self.nombre!r}, especie={self.especie!r})"
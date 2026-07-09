from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, Date, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CitasTratamientos(Base):
    __tablename__ = "citas_tratamientos"

    id_citas_tratamientos: Mapped[int] = mapped_column(primary_key=True)
    id_tratamiento: Mapped[int] = mapped_column(ForeignKey("tratamientos.id_tratamiento"))
    id_cita: Mapped[int] = mapped_column(ForeignKey("citas.id_cita"))
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_fin: Mapped[date] = mapped_column(Date)
    dosis: Mapped[str] = mapped_column(String(100))
    seguimiento: Mapped[Optional[str]] = mapped_column(Text)
    valor_tratamiento: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))

    def __repr__(self) -> str:
        return f"CitasTratamientos(id={self.id_citas_tratamientos!r}, id_cita={self.id_cita!r}, id_tratamiento={self.id_tratamiento!r})"
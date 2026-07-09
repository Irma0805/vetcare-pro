from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, DateTime, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Cita(Base):
    __tablename__ = "citas"

    id_cita: Mapped[int] = mapped_column(primary_key=True)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[str] = mapped_column(String(20), default="agendada")
    valor_consulta: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    diagnostico: Mapped[Optional[str]] = mapped_column(Text)
    id_mascota: Mapped[int] = mapped_column(ForeignKey("mascotas.id_mascota"))
    id_veterinario: Mapped[int] = mapped_column(ForeignKey("veterinarios.id_veterinario"))

    def __repr__(self) -> str:
        return f"Cita(id={self.id_cita!r}, fecha_hora={self.fecha_hora!r}, estado={self.estado!r})"
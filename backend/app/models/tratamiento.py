from decimal import Decimal
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Tratamiento(Base):
    __tablename__ = "tratamientos"

    id_tratamiento: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    tarifa_por_kg: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    def __repr__(self) -> str:
        return f"Tratamiento(id={self.id_tratamiento!r}, nombre={self.nombre!r}, tarifa_por_kg={self.tarifa_por_kg!r})"
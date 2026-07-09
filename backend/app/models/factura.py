# app/models/factura.py

from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Factura(Base):
    __tablename__ = "facturas"

    id_factura: Mapped[int] = mapped_column(primary_key=True)
    id_cita: Mapped[int] = mapped_column(ForeignKey("citas.id_cita"), unique=True)
    seguro: Mapped[Optional[str]] = mapped_column(String(100))
    forma_pago: Mapped[str] = mapped_column(String(20))
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    importe_total: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    def __repr__(self) -> str:
        return f"Factura(id={self.id_factura!r}, id_cita={self.id_cita!r}, importe_total={self.importe_total!r})"
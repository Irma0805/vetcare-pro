from datetime import date
from decimal import Decimal
from typing import Optional, Self

from pydantic import BaseModel, Field, model_validator


class AsociarTratamientoCreate(BaseModel):
    """
    Payload para asociar un tratamiento a una cita (CU-06).

    No incluye id_cita ni id_tratamiento como parte del body: el
    tratamiento se selecciona vía path (id_tratamiento) o se decide
    a nivel de router; aquí solo van los datos propios del registro
    en Citas_Tratamientos.
    """
    id_tratamiento: int
    fecha_inicio: date
    fecha_fin: date
    dosis: str = Field(max_length=100)
    seguimiento: Optional[str] = None

    @model_validator(mode="after")
    def validar_rango_fechas(self) -> Self:
        if self.fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha de fin no puede ser anterior a la fecha de inicio."
            )
        return self


class CitaTratamientoResponse(BaseModel):
    """Registro creado en Citas_Tratamientos, devuelto tras la asociación (CU-06)."""
    id_citas_tratamientos: int
    id_cita: int
    id_tratamiento: int
    fecha_inicio: date
    fecha_fin: date
    dosis: str
    seguimiento: Optional[str] = None
    valor_tratamiento: Optional[Decimal] = None

    model_config = {"from_attributes": True}
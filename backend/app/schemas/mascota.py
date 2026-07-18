from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.schemas.propietario import PropietarioResumen


class MascotaCreate(BaseModel):
    """
    Payload de alta de mascota (CU-04, alta automática dentro del
    flujo de creación de cita, o asociada a un propietario ya
    existente). No incluye id_propietario: esa asociación la resuelve
    el controlador según el propietario ya creado/seleccionado en la
    misma petición, nunca la decide el cliente directamente.
    """
    nombre: str = Field(max_length=50)
    especie: str = Field(max_length=50)
    raza: str | None = Field(default=None, max_length=50)
    fecha_nacimiento: date | None = None
    peso: Decimal | None = Field(default=None, ge=0)

class FichaMascotaResponse(BaseModel):
    """Ficha completa de mascota: datos identificativos + propietario en solo lectura (CU-17)."""
    id_mascota: int
    nombre: str
    especie: str
    raza: str | None = None
    fecha_nacimiento: date | None = None
    peso: Decimal | None = None
    activo: bool
    propietario: PropietarioResumen

    model_config = {"from_attributes": True}
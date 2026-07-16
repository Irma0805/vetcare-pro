from datetime import datetime
from typing_extensions import Self

from pydantic import BaseModel, model_validator

from app.schemas.propietario import PropietarioCreate
from app.schemas.mascota import MascotaCreate


class CitaCreate(BaseModel):
    """
    Payload de creación de cita (CU-04). Admite tres combinaciones
    válidas: propietario y mascota ya existentes (por ID), propietario
    nuevo con mascota nueva, o propietario existente con mascota
    nueva — nunca ambos (ID y objeto nuevo) para el mismo par, ni
    ninguno de los dos.

    Queda excluida explícitamente la combinación propietario_nuevo +
    mascota_id: implicaría reasignar el propietario de una mascota ya
    existente, decisión fuera de alcance del MVP (YAGNI, documentado
    en el checkpoint de la épica Clientes).
    """
    propietario_id: int | None = None
    propietario_nuevo: PropietarioCreate | None = None

    mascota_id: int | None = None
    mascota_nueva: MascotaCreate | None = None

    veterinario_id: int
    fecha_hora: datetime
    motivo_consulta: str

    @model_validator(mode="after")
    def validar_propietario_xor(self) -> Self:
        if (self.propietario_id is None) == (self.propietario_nuevo is None):
            raise ValueError(
                "Debe indicarse exactamente uno: propietario_id o propietario_nuevo, no ambos ni ninguno."
            )
        return self

    @model_validator(mode="after")
    def validar_mascota_xor(self) -> Self:
        if (self.mascota_id is None) == (self.mascota_nueva is None):
            raise ValueError(
                "Debe indicarse exactamente uno: mascota_id o mascota_nueva, no ambos ni ninguno."
            )
        return self

    @model_validator(mode="after")
    def validar_no_reasignacion_propietario(self) -> Self:
        if self.propietario_nuevo is not None and self.mascota_id is not None:
            raise ValueError(
                "No se puede crear un propietario nuevo para una mascota ya existente: "
                "la reasignación de propietario está fuera de alcance del MVP."
            )
        return self

class CitaResponse(BaseModel):
    """Datos devueltos tras crear una cita (CU-04)."""
    id_cita: int
    fecha_hora: datetime
    motivo_consulta: str
    estado: str
    id_mascota: int
    id_veterinario: int

    model_config = {"from_attributes": True}
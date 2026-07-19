from pydantic import BaseModel, Field, field_validator

from app.validation.document_validation import validate_document


class PropietarioCreate(BaseModel):
    """
    Payload de alta de propietario (CU-04, alta automática dentro del
    flujo de creación de cita). Los límites de longitud replican las
    columnas SQLAlchemy ya migradas en app/models/propietario.py.
    """
    dni: str = Field(max_length=20)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=150)
    direccion: str | None = Field(default=None, max_length=200)
    telefono: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=150)

    @field_validator("dni")
    @classmethod
    def validar_dni(cls, valor: str) -> str:
        return validate_document(valor)

class MascotaResumen(BaseModel):
    """Mascota resumida dentro de la ficha de cliente (CU-14)."""
    id_mascota: int
    nombre: str
    especie: str

    model_config = {"from_attributes": True}


class FichaClienteResponse(BaseModel):
    """Ficha completa de cliente: datos de contacto + mascotas asociadas (CU-14)."""
    id_propietario: int
    dni: str
    nombre: str
    apellidos: str
    direccion: str | None = None
    telefono: str | None = None
    email: str | None = None
    mascotas: list[MascotaResumen]

    model_config = {"from_attributes": True}

class PropietarioResumen(BaseModel):
    """Propietario resumido dentro de la ficha de mascota (CU-17)."""
    id_propietario: int
    nombre: str
    apellidos: str

    model_config = {"from_attributes": True}
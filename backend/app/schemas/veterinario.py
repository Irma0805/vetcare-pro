from pydantic import BaseModel, ConfigDict, Field


class VeterinarioCreate(BaseModel):
    """Datos de entrada para dar de alta un veterinario (CU-20)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    nombre: str = Field(min_length=1)
    apellidos: str = Field(min_length=1)
    especialidad: str | None = None


class VeterinarioResponse(BaseModel):
    """Ficha de veterinario devuelta tras el alta (CU-20, paso 5)."""

    model_config = ConfigDict(from_attributes=True)

    id_veterinario: int
    nombre: str
    apellidos: str
    especialidad: str | None = None
    activo: bool
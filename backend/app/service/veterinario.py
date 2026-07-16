"""
Capa de acceso a datos para la entidad Veterinario (ADR-008).

A diferencia de propietario.py y mascota.py, no incluye create_*: el
alta de veterinario no ocurre dentro de CU-04 (tiene su propia HU,
FUS-19). Solo se necesita resolver un veterinario_id ya existente.
"""

from sqlalchemy.orm import Session

from app.models.veterinario import Veterinario


def get_veterinario_activo(db: Session, veterinario_id: int) -> Veterinario | None:
    """
    Consulta un veterinario por su ID, exigiendo que esté activo.

    Devuelve None tanto si el veterinario no existe como si existe
    pero está inactivo — el Gherkin de CU-04 solo contempla un único
    mensaje de rechazo ("veterinario no disponible"), sin distinguir
    el motivo. El controlador traduce ese None al error HTTP
    correspondiente.
    """
    veterinario = db.get(Veterinario, veterinario_id)
    if veterinario is None or not veterinario.activo:
        return None
    return veterinario
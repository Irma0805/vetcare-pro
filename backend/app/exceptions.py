"""
Excepciones de dominio compartidas (independientes de FastAPI).

No heredan de HTTPException a propósito: son excepciones de negocio
puras, agnósticas del framework web (patrón confirmado en la
documentación de FastAPI y en guías de referencia de la comunidad).
Es el router quien las captura y decide el código HTTP y el mensaje
correspondientes — el controlador nunca conoce HTTPException.
"""


class PropietarioNoEncontradoError(Exception):
    """El propietario_id indicado no corresponde a ningún propietario existente."""


class MascotaNoEncontradaError(Exception):
    """El mascota_id indicado no corresponde a ninguna mascota existente."""


class VeterinarioNoDisponibleError(Exception):
    """
    El veterinario_id indicado no existe o está inactivo.

    Un único tipo de excepción para ambos motivos, coherente con
    get_veterinario_activo() en service/: el Gherkin de CU-04 solo
    define un mensaje de rechazo, sin distinguir la causa.
    """

class CitaNoEncontradaError(Exception):
    """El cita_id indicado no corresponde a ninguna cita existente."""


class TratamientoNoEncontradoError(Exception):
    """El tratamiento_id indicado no corresponde a ningún tratamiento existente."""

class CitaYaRealizadaError(Exception):
    """La cita indicada ya tiene fecha y hora pasadas; no puede cancelarse."""


class CitaYaCanceladaError(Exception):
    """La cita indicada ya está en estado 'cancelada'."""
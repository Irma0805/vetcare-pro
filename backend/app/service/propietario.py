"""
Capa de acceso a datos para la entidad Propietario (ADR-008).

Contiene únicamente operaciones directas sobre la base de datos
(consulta y creación). No orquesta lógica de negocio ni gestiona el
ciclo de vida de la transacción (add/flush/commit): esa responsabilidad
vive en controlador/, que decide cuándo confirmar los cambios.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.propietario import Propietario
from app.schemas.propietario import PropietarioCreate


def get_propietario_by_id(db: Session, propietario_id: int) -> Propietario | None:
    """
    Consulta un propietario existente por su ID.

    Devuelve None si no existe; es responsabilidad del controlador
    decidir qué error de negocio corresponde ante esa ausencia.
    """
    return db.get(Propietario, propietario_id)


def create_propietario(db: Session, datos: PropietarioCreate) -> Propietario:
    """
    Crea un nuevo Propietario a partir de un PropietarioCreate ya validado.

    Solo añade el objeto a la sesión (db.add); no hace flush ni commit.
    El controlador decide cuándo confirmar la transacción, para
    mantener un único punto de control atómico (ver ADR-008).
    """
    nuevo_propietario = Propietario(
        dni=datos.dni,
        nombre=datos.nombre,
        apellidos=datos.apellidos,
        direccion=datos.direccion,
        telefono=datos.telefono,
        email=datos.email,
    )
    db.add(nuevo_propietario)
    return nuevo_propietario


def get_propietario_by_dni(db: Session, dni: str) -> Propietario | None:
    """
    Busca un propietario existente por coincidencia exacta de DNI.

    Devuelve None si no hay ningún propietario con ese DNI; no es un
    error de negocio (es el caso esperado para un cliente nuevo), así
    que el controlador no debe traducir esta ausencia a una excepción.

    No filtra por `activo`: un propietario dado de baja debe seguir
    siendo encontrado por su DNI (igual que Mascota en FUS-18), para
    que el flujo de Crear Cita pueda avisar de que está inactivo en
    vez de tratarlo como si no existiera y arriesgar un DNI duplicado.
    """
    return db.execute(
        select(Propietario).where(Propietario.dni == dni)
    ).scalar_one_or_none()
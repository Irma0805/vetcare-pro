"""
Capa de acceso a datos para la entidad Mascota (ADR-008).

Contiene únicamente operaciones directas sobre la base de datos
(consulta y creación). No orquesta lógica de negocio ni gestiona el
ciclo de vida de la transacción (add/flush/commit): esa responsabilidad
vive en controlador/, que decide cuándo confirmar los cambios.

Incluye get_mascotas_por_propietario (listado para la ficha de
cliente, FUS-13/CU-14).
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate


def get_mascota_by_id(db: Session, mascota_id: int) -> Mascota | None:
    """
    Consulta una mascota existente por su ID.

    Devuelve None si no existe; es responsabilidad del controlador
    decidir qué error de negocio corresponde ante esa ausencia.
    """
    return db.get(Mascota, mascota_id)


def create_mascota(db: Session, datos: MascotaCreate, id_propietario: int) -> Mascota:
    """
    Crea una nueva Mascota a partir de un MascotaCreate ya validado.

    MascotaCreate no incluye id_propietario (lo resuelve el
    controlador, según el propietario existente o recién creado), por
    lo que se recibe como parámetro independiente.

    Solo añade el objeto a la sesión (db.add); no hace flush ni commit.
    El controlador decide cuándo confirmar la transacción, para
    mantener un único punto de control atómico (ver ADR-008).
    """
    nueva_mascota = Mascota(
        nombre=datos.nombre,
        especie=datos.especie,
        raza=datos.raza,
        fecha_nacimiento=datos.fecha_nacimiento,
        peso=datos.peso,
        id_propietario=id_propietario,
    )
    db.add(nueva_mascota)
    return nueva_mascota


def get_mascotas_por_propietario(db: Session, id_propietario: int) -> list[Mascota]:
    """
    Lista todas las mascotas de un propietario, activas e inactivas
    (FUS-13/CU-14): una mascota dada de baja sigue siendo consultable
    desde la ficha de su cliente, no se oculta del listado (decisión
    ya documentada en la épica Mascotas).
    """
    stmt = select(Mascota).where(Mascota.id_propietario == id_propietario)
    return list(db.scalars(stmt).all())
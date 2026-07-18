"""
Capa de acceso a datos para la entidad Cita (ADR-008).

Incluye create_cita (alta, FUS-03/CU-04), contar_citas y
get_citas_paginadas (listado paginado, FUS-06/CU-07).
"""

from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models.mascota import Mascota
from app.models.veterinario import Veterinario
from app.models.cita import Cita, EstadoCita


def create_cita(
    db: Session,
    fecha_hora: datetime,
    motivo_consulta: str,
    id_mascota: int,
    id_veterinario: int,
) -> Cita:
    """
    Crea una nueva Cita con estado "agendada".

    estado se asigna explícitamente en vez de depender del default
    del modelo: mapped_column(default=...) es un default a nivel de
    INSERT, no visible en el objeto Python hasta el flush/commit
    (verificado contra la documentación oficial de SQLAlchemy 2.0).

    No incluye diagnostico ni valor_consulta: se rellenan en FUS-04 y
    FUS-05/FUS-09 respectivamente, no en la creación de la cita.

    Solo añade el objeto a la sesión (db.add); no hace flush ni
    commit. El controlador decide cuándo confirmar la transacción,
    para mantener un único punto de control atómico (ver ADR-008).
    """
    nueva_cita = Cita(
        fecha_hora=fecha_hora,
        motivo_consulta=motivo_consulta,
        estado=EstadoCita.AGENDADA.value,
        id_mascota=id_mascota,
        id_veterinario=id_veterinario,
    )
    db.add(nueva_cita)
    return nueva_cita


def contar_citas(db: Session) -> int:
    """Total de citas registradas (FUS-06/CU-07), para calcular la última página válida."""
    stmt = select(func.count()).select_from(Cita)
    return db.scalar(stmt)


def get_citas_paginadas(db: Session, skip: int, limit: int):
    """
    Lista citas con nombre de mascota y veterinario ya resueltos (join),
    ordenadas por fecha_hora descendente (FUS-06/CU-07).

    Devuelve filas (Row), no objetos Cita completos: la consulta
    selecciona columnas sueltas de tres tablas, no instancias mapeadas
    de una sola. Pydantic (from_attributes=True) lee estas filas igual
    que un objeto ORM, verificado con evidencia real.
    """
    stmt = (
        select(
            Cita.id_cita,
            Cita.fecha_hora,
            Cita.estado,
            Mascota.nombre.label("mascota_nombre"),
            Veterinario.nombre.label("veterinario_nombre"),
            Veterinario.apellidos.label("veterinario_apellidos"),
        )
        .join(Mascota, Cita.id_mascota == Mascota.id_mascota)
        .join(Veterinario, Cita.id_veterinario == Veterinario.id_veterinario)
        .order_by(Cita.fecha_hora.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.execute(stmt).all()

def get_cita_by_id(db: Session, cita_id: int) -> Cita | None:
    """
    Consulta una cita existente por su ID.

    Devuelve None si no existe; es responsabilidad del controlador
    decidir qué error de negocio corresponde ante esa ausencia
    (mismo patrón ya aplicado en get_mascota_by_id / get_propietario_by_id).
    """
    return db.get(Cita, cita_id)

def cancelar_cita_bd(db: Session, cita: Cita) -> Cita:
    """
    Cambia el estado de una cita a "cancelada" (FUS-08/CU-09).

    Recibe el objeto Cita ya cargado y validado por el controlador
    (existe, está en estado agendada, fecha futura) — esta función
    no valida nada, solo aplica el cambio de estado.

    No requiere db.add(): cita ya está adjunto a la sesión (se cargó
    con db.get() dentro de la misma sesión), así que SQLAlchemy
    detecta la mutación del atributo automáticamente y genera el
    UPDATE en el próximo flush/commit (verificado contra la
    documentación oficial de SQLAlchemy 2.0, Session Basics). No hace
    flush ni commit aquí: el controlador decide cuándo confirmar la
    transacción (ADR-008).
    """
    cita.estado = EstadoCita.CANCELADA.value
    return cita
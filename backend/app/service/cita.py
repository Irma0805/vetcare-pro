"""
Capa de acceso a datos para la entidad Cita (ADR-008).

Contiene únicamente la creación de la cita, con los IDs de mascota y
veterinario ya resueltos por el controlador. No incluye lectura por
ID: CU-04 no contempla ningún escenario de búsqueda de cita existente.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.cita import Cita


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
        estado="agendada",
        id_mascota=id_mascota,
        id_veterinario=id_veterinario,
    )
    db.add(nueva_cita)
    return nueva_cita
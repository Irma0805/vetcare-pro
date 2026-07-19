"""
Capa de acceso a datos para la tabla puente CitasTratamientos (ADR-008).

Contiene únicamente la creación del registro que asocia un tratamiento
a una cita. No calcula valor_tratamiento (eso es orquestación, vive en
controlador/) ni gestiona el ciclo de vida de la transacción.
"""

from datetime import date
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app.models.citas_tratamientos import CitasTratamientos


def create_cita_tratamiento(
    db: Session,
    id_cita: int,
    id_tratamiento: int,
    fecha_inicio: date,
    fecha_fin: date,
    dosis: str,
    seguimiento: Optional[str],
    valor_tratamiento: Optional[Decimal],
) -> CitasTratamientos:
    """
    Crea un nuevo registro en Citas_Tratamientos.

    valor_tratamiento se recibe ya calculado (o None) desde el
    controlador: esta función no conoce el peso de la mascota ni la
    tarifa del tratamiento, solo persiste el resultado (CU-06).

    Solo añade el objeto a la sesión (db.add); no hace flush ni
    commit. El controlador decide cuándo confirmar la transacción.
    """
    nuevo_registro = CitasTratamientos(
        id_cita=id_cita,
        id_tratamiento=id_tratamiento,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        dosis=dosis,
        seguimiento=seguimiento,
        valor_tratamiento=valor_tratamiento,
    )
    db.add(nuevo_registro)
    return nuevo_registro
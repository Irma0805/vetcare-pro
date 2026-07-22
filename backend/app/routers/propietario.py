"""
Endpoints HTTP para Propietario (ADR-003).
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controlador.propietario import (
    obtener_ficha_cliente as obtener_ficha_cliente_controlador,
    buscar_propietario_por_dni as buscar_propietario_por_dni_controlador,
)
from app.schemas.propietario import FichaClienteResponse, PropietarioBusqueda
from app.database import get_db
from app.exceptions import PropietarioNoEncontradoError

router = APIRouter(tags=["Clientes"])


@router.get("/propietarios/{propietario_id}", response_model=FichaClienteResponse)
def obtener_ficha_cliente(propietario_id: int, db: Session = Depends(get_db)):
    """
    Endpoint de ficha de cliente (FUS-13/CU-14).
    Traduce PropietarioNoEncontradoError a 404 — caso no exigido
    explícitamente por el Gherkin, pero cubierto por ser el resultado
    obvio de pedir un id_propietario inexistente.
    """
    try:
        return obtener_ficha_cliente_controlador(db, propietario_id)
    except PropietarioNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El cliente indicado no existe",
        )


@router.get("/propietarios", response_model=PropietarioBusqueda | None)
def buscar_propietario(
    dni: str = Query(..., description="DNI exacto del propietario a buscar"),
    db: Session = Depends(get_db),
):
    """
    Busca un propietario existente por DNI exacto (FUS-03/CU-04).

    Devuelve 200 con cuerpo null si no hay coincidencia — es un
    resultado válido de búsqueda (candidato a cliente nuevo), no un
    error 404: a diferencia de /propietarios/{id}, aquí "no encontrado"
    es el caso esperado más frecuente, no una referencia rota.
    """
    return buscar_propietario_por_dni_controlador(db, dni)
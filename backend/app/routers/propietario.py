"""
Endpoints HTTP para Propietario (ADR-003).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controlador.propietario import obtener_ficha_cliente as obtener_ficha_cliente_controlador
from app.database import get_db
from app.schemas.propietario import FichaClienteResponse
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
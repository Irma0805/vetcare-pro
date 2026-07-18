"""
Endpoints HTTP para Mascota (ADR-003).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.controlador.mascota import obtener_ficha_mascota as obtener_ficha_mascota_controlador
from app.database import get_db
from app.schemas.mascota import FichaMascotaResponse
from app.exceptions import MascotaNoEncontradaError

router = APIRouter(tags=["Mascotas"])


@router.get("/mascotas/{mascota_id}", response_model=FichaMascotaResponse)
def obtener_ficha_mascota(mascota_id: int, db: Session = Depends(get_db)):
    """
    Endpoint de ficha de mascota (FUS-16/CU-17).
    Traduce MascotaNoEncontradaError a 404 — caso no exigido
    explícitamente por el Gherkin, pero cubierto por ser el resultado
    obvio de pedir un mascota_id inexistente (mismo criterio ya
    aplicado en el endpoint gemelo de ficha de cliente, FUS-13).
    """
    try:
        return obtener_ficha_mascota_controlador(db, mascota_id)
    except MascotaNoEncontradaError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La mascota indicada no existe",
        )
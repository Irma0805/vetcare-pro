from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.controlador.cita import crear_cita as crear_cita_controlador
from app.controlador.cita import listar_citas as listar_citas_controlador
from app.controlador.cita import asociar_tratamiento as asociar_tratamiento_controlador
from app.controlador.cita import cancelar_cita as cancelar_cita_controlador
from app.controlador.cita import registrar_diagnostico as registrar_diagnostico_controlador
from app.database import get_db
from app.schemas.cita import CitaCreate, CitaListItem, CitaResponse, DiagnosticoUpdate
from app.schemas.tratamiento import AsociarTratamientoCreate, CitaTratamientoResponse
from app.exceptions import (
    PropietarioNoEncontradoError,
    MascotaNoEncontradaError,
    VeterinarioNoDisponibleError,
    CitaNoEncontradaError,
    TratamientoNoEncontradoError,
    CitaYaRealizadaError,
    CitaYaCanceladaError,
    CitaNoRealizadaAunError,
)

router = APIRouter(tags=["Gestión de Citas"])


@router.post("/citas", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(datos: CitaCreate, db: Session = Depends(get_db)):
    """
    Endpoint de creación de cita (FUS-03/CU-04).
    Toda la orquestación (resolver propietario, mascota, veterinario,
    crear la cita) vive en controlador.cita.crear_cita — este
    endpoint solo traduce las excepciones de dominio a HTTP.
    """
    try:
        return crear_cita_controlador(db, datos)
    except PropietarioNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El propietario indicado no existe",
        )
    except MascotaNoEncontradaError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La mascota indicada no existe",
        )
    except VeterinarioNoDisponibleError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El veterinario no está disponible",
        )


@router.get("/citas", response_model=list[CitaListItem])
def listar_citas(
    pagina: int = Query(1, ge=1, description="Página del listado (10 citas por página)"),
    db: Session = Depends(get_db),
):
    """
    Endpoint de listado paginado de citas (FUS-06/CU-07).
    Sin excepciones que traducir: si la página solicitada excede el
    total disponible, el controlador ya la ajusta a la última válida
    (sin error visible, tal como exige el Gherkin) — este endpoint
    nunca lanza HTTPException.
    """
    return listar_citas_controlador(db, pagina)


@router.post(
    "/citas/{cita_id}/tratamientos",
    response_model=CitaTratamientoResponse,
    status_code=status.HTTP_201_CREATED,
)
def asociar_tratamiento(cita_id: int, datos: AsociarTratamientoCreate, db: Session = Depends(get_db)):
    """
    Endpoint de asociación de tratamiento a cita (FUS-05/CU-06).
    La validación de rango de fechas (fecha_fin >= fecha_inicio) ya
    la resuelve AsociarTratamientoCreate a nivel de schema (422
    automático de Pydantic); este endpoint solo traduce las
    excepciones de dominio de existencia a HTTP.
    """
    try:
        return asociar_tratamiento_controlador(db, cita_id, datos)
    except CitaNoEncontradaError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cita indicada no existe",
        )
    except TratamientoNoEncontradoError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El tratamiento indicado no existe",
        )
    

@router.post("/citas/{cita_id}/cancelar", response_model=CitaResponse)
def cancelar_cita(cita_id: int, db: Session = Depends(get_db)):
    """
    Endpoint de cancelación de cita (FUS-08/CU-09).
    Reutiliza CitaResponse (mismo schema que crear_cita) para
    devolver la cita con su estado ya actualizado a "cancelada".
    """
    try:
        return cancelar_cita_controlador(db, cita_id)
    except CitaNoEncontradaError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cita indicada no existe",
        )
    except CitaYaCanceladaError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La cita ya está cancelada",
        )
    except CitaYaRealizadaError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La cita ya se ha realizado y no puede cancelarse",
        )

@router.patch("/citas/{cita_id}/diagnostico", response_model=CitaResponse)
def registrar_diagnostico(cita_id: int, datos: DiagnosticoUpdate, db: Session = Depends(get_db)):
    """
    Endpoint de registro/edición de diagnóstico (FUS-04/CU-05).
    PATCH, no POST: a diferencia de cancelar_cita (acción con efectos
    colaterales de negocio), esto es la actualización parcial de un
    único campo de un recurso ya existente — el caso canónico de
    PATCH según convención REST (verificado contra Azure API Design
    Guide y consenso de comunidad).
    """
    try:
        return registrar_diagnostico_controlador(db, cita_id, datos)
    except CitaNoEncontradaError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La cita indicada no existe",
        )
    except CitaNoRealizadaAunError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La cita aún no se ha realizado",
        )
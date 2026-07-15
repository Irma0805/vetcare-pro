from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=280,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Dependencia de FastAPI (Depends(get_db)) que abre una sesión de
    base de datos nueva por cada petición HTTP y la cierra siempre al
    finalizar, incluso si la petición termina en error. No hace commit
    ni rollback por sí misma — esa decisión es responsabilidad de cada
    función de servicio/controlador que reciba la sesión.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
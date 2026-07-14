from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models.usuario import Usuario
from app.validation.password import hash_password


class TestSettings(BaseSettings):
    """
    Configuración exclusiva para la suite de tests (ADR-007).
    Separada de app.config.Settings a propósito: la aplicación real
    no debe depender de una variable que solo existe para pytest.
    """
    test_database_url: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


test_settings = TestSettings()

engine = create_engine(test_settings.test_database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Crea el esquema completo en vetcare_pro_test una vez por sesión de
    tests, y lo destruye al terminar. Usa Base.metadata directamente,
    no Alembic (ADR-007) — es un esquema desechable, no versionado.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """
    Sesión de base de datos envuelta en una transacción que se revierte
    al terminar cada test, para que ningún test deje rastro al siguiente.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    TestClient de FastAPI, con get_db sustituido por la sesión de test
    vía dependency_overrides — así cada petición del test usa la
    transacción aislada, no la base de datos real.
    """
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def crear_usuario():
    """
    Factory fixture (patrón "Factories as fixtures" de pytest): en vez de
    devolver un dato fijo, devuelve una función que cada test puede
    llamar tantas veces como necesite, con los parámetros propios de
    cada escenario Gherkin.

    La función devuelta inserta un Usuario directamente en la base de
    datos de test, sin pasar por el endpoint (sirve para preparar el
    estado previo de cada escenario, no para probar la creación de
    usuarios).
    """
    def _crear_usuario(db: Session, username: str, password: str, activo: bool = True) -> Usuario:
        usuario = Usuario(
            username=username,
            password_hash=hash_password(password),
            activo=activo,
        )
        db.add(usuario)
        db.flush()
        db.refresh(usuario)
        return usuario

    return _crear_usuario
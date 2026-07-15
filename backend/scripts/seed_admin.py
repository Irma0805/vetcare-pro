"""
Script de mantenimiento para crear el usuario administrador único (ADR-002).
No forma parte de la aplicación FastAPI: se ejecuta manualmente contra el
entorno indicado por DATABASE_URL en ese momento (local o Neon).

Uso:
    $env:ADMIN_USERNAME = "admin"
    $env:ADMIN_PASSWORD = "una_contraseña_segura"
    python scripts/seed_admin.py
"""
import os
import sys

from sqlalchemy import select

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.validation.password import hash_password


def seed_admin() -> None:
    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")

    if not username or not password:
        print("Error: define ADMIN_USERNAME y ADMIN_PASSWORD como variables de entorno.")
        sys.exit(1)

    db = SessionLocal()
    try:
        usuario_existente = db.execute(
            select(Usuario).where(Usuario.username == username)
        ).scalar_one_or_none()

        if usuario_existente:
            print(f"El usuario '{username}' ya existe. No se ha creado nada.")
            return

        nuevo_usuario = Usuario(
            username=username,
            password_hash=hash_password(password),
            activo=True,
        )
        db.add(nuevo_usuario)
        db.commit()
        print(f"Usuario '{username}' creado correctamente.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
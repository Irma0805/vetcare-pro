"""
Script de mantenimiento para cargar datos de ejemplo (propietarios,
mascotas, veterinarios) y poder probar CU-04 manualmente en Swagger
sin rellenar formularios uno a uno.
No forma parte de la aplicación FastAPI: se ejecuta manualmente contra
el entorno indicado por DATABASE_URL en ese momento (normalmente local,
nunca contra Neon).

Uso:
    python scripts/seed_datos_ejemplo.py
"""
from sqlalchemy import select

from app.database import SessionLocal
from app.models.propietario import Propietario
from app.models.mascota import Mascota
from app.models.veterinario import Veterinario


PROPIETARIOS_CON_MASCOTA = [
    {"dni": "11111111A", "nombre": "María", "apellidos": "López", "mascota": "Toby", "especie": "Perro"},
    {"dni": "22222222B", "nombre": "Carlos", "apellidos": "Pérez", "mascota": "Luna", "especie": "Gato"},
    {"dni": "33333333C", "nombre": "Ana", "apellidos": "García", "mascota": "Rocky", "especie": "Perro"},
    {"dni": "44444444D", "nombre": "Jorge", "apellidos": "Martín", "mascota": "Mia", "especie": "Gato"},
]

VETERINARIOS = [
    {"nombre": "Dr.", "apellidos": "Ruiz", "activo": True},
    {"nombre": "Dr.", "apellidos": "Gómez", "activo": False},
]


def seed_datos_ejemplo() -> None:
    db = SessionLocal()
    try:
        for datos in PROPIETARIOS_CON_MASCOTA:
            propietario_existente = db.execute(
                select(Propietario).where(Propietario.dni == datos["dni"])
            ).scalar_one_or_none()

            if propietario_existente:
                print(f"Propietario con DNI '{datos['dni']}' ya existe. No se ha creado nada.")
                continue

            nuevo_propietario = Propietario(
                dni=datos["dni"],
                nombre=datos["nombre"],
                apellidos=datos["apellidos"],
            )
            db.add(nuevo_propietario)
            db.flush()

            nueva_mascota = Mascota(
                nombre=datos["mascota"],
                especie=datos["especie"],
                id_propietario=nuevo_propietario.id_propietario,
            )
            db.add(nueva_mascota)
            print(f"Propietario '{datos['nombre']} {datos['apellidos']}' y mascota '{datos['mascota']}' creados.")

        for datos in VETERINARIOS:
            veterinario_existente = db.execute(
                select(Veterinario).where(
                    Veterinario.nombre == datos["nombre"],
                    Veterinario.apellidos == datos["apellidos"],
                )
            ).scalar_one_or_none()

            if veterinario_existente:
                print(f"Veterinario '{datos['nombre']} {datos['apellidos']}' ya existe. No se ha creado nada.")
                continue

            nuevo_veterinario = Veterinario(
                nombre=datos["nombre"],
                apellidos=datos["apellidos"],
                activo=datos["activo"],
            )
            db.add(nuevo_veterinario)
            print(f"Veterinario '{datos['nombre']} {datos['apellidos']}' creado.")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_datos_ejemplo()
def test_crear_cita_con_cliente_y_mascota_existentes(client, db, crear_propietario, crear_mascota, crear_veterinario):
    """Gherkin: Crear cita con cliente y mascota ya existentes."""
    propietario = crear_propietario(db, dni="11111111A", nombre="María", apellidos="López")
    mascota = crear_mascota(db, nombre="Toby", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Dr.", apellidos="Ruiz")

    response = client.post("/citas", json={
        "propietario_id": propietario.id_propietario,
        "mascota_id": mascota.id_mascota,
        "veterinario_id": veterinario.id_veterinario,
        "fecha_hora": "2026-08-01T10:00:00Z",
        "motivo_consulta": "Revisión anual",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "agendada"
    assert data["id_mascota"] == mascota.id_mascota
    assert data["id_veterinario"] == veterinario.id_veterinario


def test_crear_cita_con_alta_automatica_de_cliente_nuevo(client, db, crear_veterinario):
    """Gherkin: Crear cita con alta automática de cliente nuevo."""
    veterinario = crear_veterinario(db, nombre="Dr.", apellidos="Ruiz")

    response = client.post("/citas", json={
        "propietario_nuevo": {
            "dni": "22222222J",
            "nombre": "Carlos",
            "apellidos": "Pérez",
        },
        "mascota_nueva": {
            "nombre": "Luna",
            "especie": "Gato",
        },
        "veterinario_id": veterinario.id_veterinario,
        "fecha_hora": "2026-08-01T10:00:00Z",
        "motivo_consulta": "Primera consulta",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "agendada"


def test_crear_cita_con_mascota_nueva_para_cliente_existente(client, db, crear_propietario, crear_veterinario):
    """Gherkin: Crear cita con mascota nueva para un cliente ya existente."""
    propietario = crear_propietario(db, dni="33333333C", nombre="María", apellidos="López")
    veterinario = crear_veterinario(db, nombre="Dr.", apellidos="Ruiz")

    response = client.post("/citas", json={
        "propietario_id": propietario.id_propietario,
        "mascota_nueva": {
            "nombre": "Rocky",
            "especie": "Perro",
        },
        "veterinario_id": veterinario.id_veterinario,
        "fecha_hora": "2026-08-01T11:00:00Z",
        "motivo_consulta": "Vacunación",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["estado"] == "agendada"


def test_crear_cita_sin_fecha_hora(client, db, crear_propietario, crear_mascota, crear_veterinario):
    """
    Gherkin: Intento de crear cita sin fecha y hora.
    El Gherkin describe el bloqueo en el FRONTEND (no llega petición al
    backend). Este test verifica la defensa en profundidad del backend,
    mismo criterio que test_login_con_campos_vacios.
    """
    propietario = crear_propietario(db, dni="44444444D", nombre="Ana", apellidos="García")
    mascota = crear_mascota(db, nombre="Mia", especie="Gato", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Dr.", apellidos="Ruiz")

    response = client.post("/citas", json={
        "propietario_id": propietario.id_propietario,
        "mascota_id": mascota.id_mascota,
        "veterinario_id": veterinario.id_veterinario,
        "motivo_consulta": "Revisión",
    })

    assert response.status_code == 422


def test_crear_cita_sin_veterinario(client, db, crear_propietario, crear_mascota):
    """
    Gherkin: Intento de crear cita sin seleccionar veterinario.
    Defensa en profundidad del backend (mismo criterio que arriba).
    """
    propietario = crear_propietario(db, dni="55555555E", nombre="Jorge", apellidos="Martín")
    mascota = crear_mascota(db, nombre="Nube", especie="Perro", id_propietario=propietario.id_propietario)

    response = client.post("/citas", json={
        "propietario_id": propietario.id_propietario,
        "mascota_id": mascota.id_mascota,
        "fecha_hora": "2026-08-01T12:00:00Z",
        "motivo_consulta": "Revisión",
    })

    assert response.status_code == 422


def test_crear_cita_con_veterinario_inactivo(client, db, crear_propietario, crear_mascota, crear_veterinario):
    """Gherkin: Intento de crear cita con un veterinario inactivo."""
    propietario = crear_propietario(db, dni="66666666F", nombre="Elena", apellidos="Ruiz")
    mascota = crear_mascota(db, nombre="Zeus", especie="Perro", id_propietario=propietario.id_propietario)
    veterinario = crear_veterinario(db, nombre="Dr.", apellidos="Gómez", activo=False)

    response = client.post("/citas", json={
        "propietario_id": propietario.id_propietario,
        "mascota_id": mascota.id_mascota,
        "veterinario_id": veterinario.id_veterinario,
        "fecha_hora": "2026-08-01T13:00:00Z",
        "motivo_consulta": "Revisión",
    })

    assert response.status_code == 422
    assert response.json()["detail"] == "El veterinario no está disponible"
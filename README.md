# VetCare Pro

Sistema integral de gestión para clínicas veterinarias — Proyecto final del Bootcamp Full Stack, **Factoría F5**.

Digitaliza y centraliza la gestión de clientes, mascotas, veterinarios y citas de una clínica veterinaria pequeña, sustituyendo la gestión en papel por un flujo real de trabajo: **crear cita → diagnosticar → tratar**.

## Índice

- [Alcance del proyecto](#alcance-del-proyecto)
- [Stack tecnológico](#stack-tecnológico)
- [Arquitectura](#arquitectura)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Puesta en marcha](#puesta-en-marcha)
- [Tests](#tests)
- [Documentación](#documentación)

## Alcance del proyecto

**MVP — 5 épicas núcleo:**
- Acceso al sistema (login, sesión con expiración por inactividad)
- Clientes (ficha, alta vía creación de cita, edición, baja lógica)
- Mascotas (ficha, edición, baja lógica)
- Veterinarios (alta, listado, ficha)
- Gestión de Citas (crear, diagnosticar, asociar tratamiento, cancelar)

**Fuera de alcance en esta versión** (recorte consciente, no deuda oculta): facturación completa, historial clínico como vista propia, calendario visual de citas, roles múltiples de usuario, edición/baja de veterinario, listado general de clientes, validación de solapamiento de horarios.

## Stack tecnológico

**Backend**
- FastAPI · SQLAlchemy 2.0 · Alembic (migraciones) · Pydantic v2
- PostgreSQL · PyJWT · pwdlib (Argon2) · pytest

**Frontend**
- React 19 + Vite (JavaScript) · React Router 8 (declarative) · React-Bootstrap + Bootstrap 5
- Axios · Vitest + React Testing Library · oxlint

## Arquitectura

**Backend — 5 capas:**

```
routers → controlador → service → validation → BD (PostgreSQL)
```

`controlador/` se mantiene en español de forma consciente (petición explícita de la tutora del bootcamp) — única excepción al inglés del resto del proyecto. `service/` combina acceso a datos y lógica de negocio; no existe una capa `repository` independiente (decisión documentada, YAGNI).

**Frontend — Atomic Design (adaptado):**

```
Pages → Organisms → Molecules → (Atoms = componentes de React-Bootstrap)
```

Solo las Pages se conectan a `Context` o hacen llamadas a la API; `molecules`/`organisms` reciben siempre sus datos por props. No existe una carpeta `atoms/` propia: ese nivel lo cubren directamente los componentes de React-Bootstrap (`Button`, `Form`, `Card`...).

## Estructura del repositorio

Monorepo con dos carpetas independientes:

```
vetcare-pro/
├── backend/     # API FastAPI
└── frontend/    # SPA React + Vite
```

Cada una con su propio `package.json`/`requirements.txt`, entorno y ciclo de vida independiente.

## Puesta en marcha

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows (PowerShell)
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Crea un archivo `.env` dentro de `backend/` con:

```
DATABASE_URL=postgresql+psycopg2://usuario:contraseña@localhost:5432/vetcare_pro
JWT_SECRET_KEY=una-clave-secreta-propia
```

(`JWT_ALGORITHM`, `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` y `SESSION_INACTIVITY_TIMEOUT_MINUTES` son opcionales — tienen valores por defecto en `app/config.py`.)

```bash
alembic upgrade head          # aplica las migraciones
python -m scripts.seed_admin  # crea el usuario administrador único

uvicorn app.main:app --reload # arranca la API en http://localhost:8000
```

La documentación interactiva (Swagger) queda disponible en `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # ya trae VITE_API_URL=http://localhost:8000

npm run dev             # arranca en http://localhost:5173
```

## Tests

```bash
# Backend — requiere una base de datos vetcare_pro_test aparte
cd backend
pytest

# Frontend
cd frontend
npm run test
```

Cada pantalla/caso de uso incluye su propia tríada de tests: validación, error de API y éxito.

## Documentación

Historias de Usuario, Casos de Uso, criterios de aceptación, escenarios Gherkin y Architecture Decision Records (ADRs) están documentados en Notion, no en este repositorio.

---

Proyecto individual — Factoría F5, Madrid.
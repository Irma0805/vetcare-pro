# VetCare Pro — Frontend

SPA de React que consume la API de VetCare Pro. Ver el [README de la raíz](../README.md) para la visión general del proyecto y cómo levantar el backend.

## Stack

- **React 19** + **Vite** (JavaScript, sin TypeScript)
- **React Router 8** en modo *declarative*
- **React-Bootstrap** + **Bootstrap 5** (componentes de UI)
- **Axios** (cliente HTTP, con interceptores JWT)
- **Sass (SCSS)** — personalización de variables de Bootstrap
- **vite-plugin-svgr** — importar SVG como componentes React
- **Vitest** + **React Testing Library** — testing
- **oxlint** — linter (basado en Rust)

## Puesta en marcha

Requiere el backend corriendo en `http://localhost:8000` (ver [README de la raíz](../README.md)).

```bash
npm install
cp .env.example .env    # ya trae VITE_API_URL=http://localhost:8000
npm run dev             # http://localhost:5173
```

## Scripts disponibles

| Comando | Qué hace |
|---|---|
| `npm run dev` | Arranca el servidor de desarrollo (Vite) |
| `npm run build` | Genera la build de producción |
| `npm run preview` | Sirve la build de producción en local |
| `npm run lint` | Ejecuta oxlint |
| `npm run test` | Ejecuta los tests con Vitest |

## Estructura de `src/`

```
src/
├── main.jsx          # Punto de entrada: BrowserRouter + AuthProvider
├── App.jsx           # Monta AppRoutes
├── routes/           # Mapeo URL → página
├── config/            # Lectura de variables de entorno
├── context/           # Estado global (sesión del administrador)
├── layout/             # Layout compartido (navbar)
├── api/                # Llamadas HTTP a la API (axiosClient + una función por entidad)
├── components/
│   ├── molecules/      # Combinaciones pequeñas de componentes de Bootstrap
│   └── organisms/      # Bloques compuestos (modales, formularios completos)
├── pages/              # Una carpeta por pantalla
├── styles/             # Variables de Bootstrap personalizadas (SCSS)
├── assets/             # Iconos SVG
└── test/               # Configuración global de Vitest
```

No existe una carpeta `components/atoms/`: ese nivel de Atomic Design lo cubren directamente los componentes de React-Bootstrap (`Button`, `Form.Control`, `Card`...), importados sin envoltorio propio.

## Convenciones

- **Solo las Pages** se conectan a `Context` o llaman a la API — `molecules`/`organisms` reciben siempre sus datos por props.
- **CSS propio solo cuando Bootstrap no llega**: casi toda la interfaz usa clases de utilidad de Bootstrap directamente en el JSX; el único `.css` del proyecto es `LoginPage.module.css`, para los dos ajustes puntuales que Bootstrap no resuelve.
- **Tests co-localizados**: cada componente/página vive junto a su propio `*.test.jsx`, siguiendo el patrón recomendado por React Testing Library — no hay una carpeta `tests/` separada, a diferencia del backend.
- **Tríada obligatoria por pantalla**: validación de campos, error de API (mock 4xx) y éxito (mock 2xx), antes de dar una pantalla por cerrada.

## Tests

```bash
npm run test
```

Axios se mockea en todos los tests — nunca se prueba contra el backend ni la base de datos real.
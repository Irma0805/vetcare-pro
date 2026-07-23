import { useState, useEffect } from 'react'
import { Link } from 'react-router'
import { Table, Spinner, Alert, Button, Badge } from 'react-bootstrap'
import { getCitas } from '../../api/citas'

const TAMANO_PAGINA = 10

const VARIANTE_POR_ESTADO = {
  agendada: 'primary',
  cancelada: 'secondary',
  realizada: 'success',
}

function formatearFechaHora(fechaISO) {
  return new Date(fechaISO).toLocaleString('es-ES', {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

function CitasPage() {
  const [citas, setCitas] = useState([])
  const [pagina, setPagina] = useState(1)
  const [loading, setLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    let ignore = false

    async function cargarCitas() {
      setLoading(true)
      setErrorMessage('')
      try {
        const datos = await getCitas(pagina)
        if (!ignore) {
          setCitas(datos)
        }
      } catch (error) {
        if (!ignore) {
          setErrorMessage(
            error.response?.data?.detail || 'No se pudo cargar el listado de citas.'
          )
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    cargarCitas()

    return () => {
      ignore = true
    }
  }, [pagina])

  const hayPaginaSiguiente = citas.length === TAMANO_PAGINA

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h1>Citas</h1>
        <Button as={Link} to="/citas/nueva" variant="primary">
          Nueva cita
        </Button>
      </div>

      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

      {loading ? (
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      ) : citas.length === 0 ? (
        <p>No hay citas que mostrar.</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Fecha y hora</th>
              <th>Mascota</th>
              <th>Veterinario</th>
              <th>Estado</th>
            </tr>
          </thead>
          <tbody>
            {citas.map((cita) => (
              <tr key={cita.id_cita}>
                <td>{formatearFechaHora(cita.fecha_hora)}</td>
                <td>{cita.mascota_nombre}</td>
                <td>{cita.veterinario_nombre} {cita.veterinario_apellidos}</td>
                <td>
                  <Badge bg={VARIANTE_POR_ESTADO[cita.estado] || 'dark'}>
                    {cita.estado}
                  </Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}

      <div className="d-flex justify-content-between">
        <Button
          variant="secondary"
          disabled={pagina === 1}
          onClick={() => setPagina((p) => p - 1)}
        >
          Anterior
        </Button>
        <Button
          variant="secondary"
          disabled={!hayPaginaSiguiente}
          onClick={() => setPagina((p) => p + 1)}
        >
          Siguiente
        </Button>
      </div>
    </>
  )
}

export default CitasPage
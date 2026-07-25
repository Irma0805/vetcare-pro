import { useState, useEffect } from 'react'
import { Link } from 'react-router'
import { Table, Spinner, Alert, Button, Badge, Dropdown, Modal } from 'react-bootstrap'
import { getCitas, cancelarCita } from '../../api/citas'

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

  const [citaACancelar, setCitaACancelar] = useState(null)
  const [cancelando, setCancelando] = useState(false)
  const [errorCancelar, setErrorCancelar] = useState('')


  useEffect(() => {
    let ignore = false

    async function cargarCitasEfecto() {
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

    cargarCitasEfecto()

    return () => {
      ignore = true
    }
  }, [pagina])

  
  async function recargarCitasTrasCancelar() {
    setLoading(true)
    setErrorMessage('')
    try {
      const datos = await getCitas(pagina)
      setCitas(datos)
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail || 'No se pudo cargar el listado de citas.'
      )
    } finally {
      setLoading(false)
    }
  }

  const hayPaginaSiguiente = citas.length === TAMANO_PAGINA

  function handleAbrirModalCancelar(cita) {
    setErrorCancelar('')
    setCitaACancelar(cita)
  }

  function handleCerrarModalCancelar() {
    setCitaACancelar(null)
    setErrorCancelar('')
  }

  async function handleConfirmarCancelar() {
    setCancelando(true)
    setErrorCancelar('')
    try {
      await cancelarCita(citaACancelar.id_cita)
      setCitaACancelar(null)
      await recargarCitasTrasCancelar()
    } catch (error) {
      setErrorCancelar(
        error.response?.data?.detail || 'No se pudo cancelar la cita.'
      )
    } finally {
      setCancelando(false)
    }
  }

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
              <th>Acciones</th>
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
                <td>
                  {cita.estado === 'agendada' && (
                    <Dropdown>
                      <Dropdown.Toggle variant="outline-secondary" size="sm">
                        Acciones
                      </Dropdown.Toggle>
                      <Dropdown.Menu>
                        <Dropdown.Item onClick={() => handleAbrirModalCancelar(cita)}>
                          Cancelar cita
                        </Dropdown.Item>
                      </Dropdown.Menu>
                    </Dropdown>
                  )}
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

      <Modal show={citaACancelar !== null} onHide={handleCerrarModalCancelar}>
        <Modal.Header closeButton>
          <Modal.Title>Cancelar cita</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {errorCancelar && <Alert variant="danger">{errorCancelar}</Alert>}
          {citaACancelar && (
            <p>
              ¿Seguro que quieres cancelar la cita del{' '}
              {formatearFechaHora(citaACancelar.fecha_hora)} con{' '}
              {citaACancelar.mascota_nombre}? Esta acción no se puede deshacer.
            </p>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCerrarModalCancelar} disabled={cancelando}>
            Volver
          </Button>
          <Button variant="danger" onClick={handleConfirmarCancelar} disabled={cancelando}>
            {cancelando ? 'Cancelando...' : 'Sí, cancelar cita'}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  )
}

export default CitasPage
import { useState, useEffect } from 'react'
import { Link } from 'react-router'
import { Table, Spinner, Alert, Button, Badge, Dropdown, Modal, Form } from 'react-bootstrap'
import { getCitas, cancelarCita, registrarDiagnostico, asociarTratamiento } from '../../api/citas'
import AsociarTratamientoModal from '../../components/organisms/AsociarTratamientoModal/AsociarTratamientoModal'

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

function esCitaPasada(fechaISO) {
  return new Date(fechaISO) < new Date()
}

function CitasPage() {
  const [citas, setCitas] = useState([])
  const [pagina, setPagina] = useState(1)
  const [loading, setLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  const [citaACancelar, setCitaACancelar] = useState(null)
  const [cancelando, setCancelando] = useState(false)
  const [errorCancelar, setErrorCancelar] = useState('')

  const [citaADiagnosticar, setCitaADiagnosticar] = useState(null)
  const [diagnosticoTexto, setDiagnosticoTexto] = useState('')
  const [guardandoDiagnostico, setGuardandoDiagnostico] = useState(false)
  const [errorDiagnostico, setErrorDiagnostico] = useState('')

  const [citaATratar, setCitaATratar] = useState(null)

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

  async function recargarCitas() {
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
      await recargarCitas()
    } catch (error) {
      setErrorCancelar(
        error.response?.data?.detail || 'No se pudo cancelar la cita.'
      )
    } finally {
      setCancelando(false)
    }
  }

  function handleAbrirModalDiagnostico(cita) {
    setErrorDiagnostico('')
    setDiagnosticoTexto('')
    setCitaADiagnosticar(cita)
  }

  function handleCerrarModalDiagnostico() {
    setCitaADiagnosticar(null)
    setDiagnosticoTexto('')
    setErrorDiagnostico('')
  }

  async function handleGuardarDiagnostico() {
    setGuardandoDiagnostico(true)
    setErrorDiagnostico('')
    try {
      await registrarDiagnostico(citaADiagnosticar.id_cita, diagnosticoTexto)
      handleCerrarModalDiagnostico()
      await recargarCitas()
    } catch (error) {
      setErrorDiagnostico(
        error.response?.data?.detail || 'No se pudo registrar el diagnóstico.'
      )
    } finally {
      setGuardandoDiagnostico(false)
    }
  }

  function handleAbrirModalTratamiento(cita) {
    setCitaATratar(cita)
  }

  function handleCerrarModalTratamiento() {
    setCitaATratar(null)
  }

 async function handleAsociarTratamiento(datos) {
    const resultado = await asociarTratamiento(citaATratar.id_cita, datos)
    await recargarCitas()
    return resultado
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
            {citas.map((cita) => {
              const esAgendada = cita.estado === 'agendada'
              const esPasada = esCitaPasada(cita.fecha_hora)
              const puedeCancelar = esAgendada && !esPasada
              const puedeDiagnosticar = esAgendada && esPasada

              return (
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
                    {(puedeCancelar || puedeDiagnosticar) && (
                      <Dropdown>
                        <Dropdown.Toggle variant="outline-secondary" size="sm">
                          Acciones
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                          {puedeCancelar && (
                            <Dropdown.Item onClick={() => handleAbrirModalCancelar(cita)}>
                              Cancelar cita
                            </Dropdown.Item>
                          )}
                          {puedeDiagnosticar && (
                            <Dropdown.Item onClick={() => handleAbrirModalDiagnostico(cita)}>
                              Registrar diagnóstico
                            </Dropdown.Item>
                          )}
                          {puedeDiagnosticar && (
                            <Dropdown.Item onClick={() => handleAbrirModalTratamiento(cita)}>
                              Asociar tratamiento
                            </Dropdown.Item>
                          )}
                        </Dropdown.Menu>
                      </Dropdown>
                    )}
                  </td>
                </tr>
              )
            })}
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

      <Modal show={citaADiagnosticar !== null} onHide={handleCerrarModalDiagnostico}>
        <Modal.Header closeButton>
          <Modal.Title>Registrar diagnóstico</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {errorDiagnostico && <Alert variant="danger">{errorDiagnostico}</Alert>}
          {citaADiagnosticar && (
            <p>
              Cita del {formatearFechaHora(citaADiagnosticar.fecha_hora)} con{' '}
              {citaADiagnosticar.mascota_nombre}.
            </p>
          )}
          <Form.Group controlId="diagnosticoTexto">
            <Form.Label>Diagnóstico</Form.Label>
            <Form.Control
              as="textarea"
              rows={4}
              value={diagnosticoTexto}
              onChange={(e) => setDiagnosticoTexto(e.target.value)}
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCerrarModalDiagnostico} disabled={guardandoDiagnostico}>
            Cancelar
          </Button>
          <Button
            variant="primary"
            onClick={handleGuardarDiagnostico}
            disabled={guardandoDiagnostico || diagnosticoTexto.trim().length === 0}
          >
            {guardandoDiagnostico ? 'Guardando...' : 'Guardar diagnóstico'}
          </Button>
        </Modal.Footer>
      </Modal>

      <AsociarTratamientoModal
        show={citaATratar !== null}
        onHide={handleCerrarModalTratamiento}
        cita={citaATratar}
        onAsociar={handleAsociarTratamiento}
      />
    </>
  )
}

export default CitasPage
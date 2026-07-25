import { useState, useEffect } from 'react'
import { Modal, Form, Button, Alert } from 'react-bootstrap'
import { getTratamientos } from '../../../api/tratamientos'

function AsociarTratamientoModal({ show, onHide, cita, onAsociar }) {
  const [tratamientos, setTratamientos] = useState([])
  const [cargandoTratamientos, setCargandoTratamientos] = useState(false)
  const [errorCarga, setErrorCarga] = useState('')

  const [idTratamiento, setIdTratamiento] = useState('')
  const [fechaInicio, setFechaInicio] = useState('')
  const [fechaFin, setFechaFin] = useState('')
  const [dosis, setDosis] = useState('')
  const [seguimiento, setSeguimiento] = useState('')

  const [validated, setValidated] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const [tratamientoAsociado, setTratamientoAsociado] = useState(null)

  useEffect(() => {
    if (!show) return

    let ignore = false

    async function cargarTratamientos() {
      setCargandoTratamientos(true)
      setErrorCarga('')
      try {
        const datos = await getTratamientos()
        if (!ignore) setTratamientos(datos)
      } catch {
        if (!ignore) {
          setErrorCarga('No se pudo cargar el catálogo de tratamientos.')
        }
      } finally {
        if (!ignore) setCargandoTratamientos(false)
      }
    }

    cargarTratamientos()

    return () => {
      ignore = true
    }
  }, [show])

  const resetFormulario = () => {
    setIdTratamiento('')
    setFechaInicio('')
    setFechaFin('')
    setDosis('')
    setSeguimiento('')
    setValidated(false)
    setErrorMessage('')
    setTratamientoAsociado(null)
  }

  const handleClose = () => {
    resetFormulario()
    onHide()
  }

  const handleSubmit = async (event) => {
    const form = event.currentTarget
    event.preventDefault()

    if (form.checkValidity() === false) {
      event.stopPropagation()
      setValidated(true)
      return
    }

    const datos = {
      id_tratamiento: Number(idTratamiento),
      fecha_inicio: fechaInicio,
      fecha_fin: fechaFin,
      dosis,
      seguimiento: seguimiento.trim() === '' ? null : seguimiento,
    }

    setErrorMessage('')
    setLoading(true)
    try {
      const resultado = await onAsociar(datos)
      setTratamientoAsociado(resultado)
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail || 'No se pudo asociar el tratamiento. Inténtalo de nuevo.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Asociar tratamiento</Modal.Title>
      </Modal.Header>

      {tratamientoAsociado ? (
        <>
          <Modal.Body>
            <Alert variant="success">
              Tratamiento asociado correctamente.
            </Alert>
            <p>
              <strong>Valor del tratamiento:</strong>{' '}
              {tratamientoAsociado.valor_tratamiento !== null
                ? `${tratamientoAsociado.valor_tratamiento} €`
                : 'No calculado (la mascota no tiene peso registrado)'}
            </p>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="primary" onClick={handleClose}>
              Cerrar
            </Button>
          </Modal.Footer>
        </>
      ) : (
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
          <Modal.Body>
            {cita && (
              <p className="text-muted">
                Cita con {cita.mascota_nombre}.
              </p>
            )}

            {errorCarga && <Alert variant="danger">{errorCarga}</Alert>}
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

            <Form.Group className="mb-3" controlId="idTratamiento">
              <Form.Label>Tratamiento</Form.Label>
              <Form.Select
                value={idTratamiento}
                onChange={(e) => setIdTratamiento(e.target.value)}
                disabled={cargandoTratamientos}
                required
              >
                <option value="">
                  {cargandoTratamientos ? 'Cargando tratamientos...' : 'Selecciona un tratamiento'}
                </option>
                {tratamientos.map((t) => (
                  <option key={t.id_tratamiento} value={t.id_tratamiento}>
                    {t.nombre} — {t.tarifa_por_kg} €/kg
                  </option>
                ))}
              </Form.Select>
              <Form.Control.Feedback type="invalid">
                Debes seleccionar un tratamiento.
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="fechaInicio">
              <Form.Label>Fecha de inicio</Form.Label>
              <Form.Control
                type="date"
                value={fechaInicio}
                onChange={(e) => setFechaInicio(e.target.value)}
                required
              />
              <Form.Control.Feedback type="invalid">
                La fecha de inicio es obligatoria.
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="fechaFin">
              <Form.Label>Fecha de fin</Form.Label>
              <Form.Control
                type="date"
                value={fechaFin}
                {...(fechaInicio ? { min: fechaInicio } : {})}
                onChange={(e) => setFechaFin(e.target.value)}
                required
              />
              <Form.Control.Feedback type="invalid">
                La fecha de fin es obligatoria y no puede ser anterior a la de inicio.
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group className="mb-3" controlId="dosis">
              <Form.Label>Dosis</Form.Label>
              <Form.Control
                type="text"
                value={dosis}
                maxLength={100}
                onChange={(e) => setDosis(e.target.value)}
                required
              />
              <Form.Control.Feedback type="invalid">
                La dosis es obligatoria.
              </Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="seguimiento">
              <Form.Label>Seguimiento</Form.Label>
              <Form.Control
                as="textarea"
                placeholder="Opcional"
                value={seguimiento}
                onChange={(e) => setSeguimiento(e.target.value)}
              />
            </Form.Group>
          </Modal.Body>

          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Cancelar
            </Button>
            <Button variant="primary" type="submit" disabled={loading || cargandoTratamientos}>
              {loading ? 'Asociando...' : 'Asociar tratamiento'}
            </Button>
          </Modal.Footer>
        </Form>
      )}
    </Modal>
  )
}

export default AsociarTratamientoModal
import { useState } from 'react'
import { Modal, Form, Button, Alert } from 'react-bootstrap'

function CrearVeterinarioModal({ show, onHide, onCrear }) {
  const [nombre, setNombre] = useState('')
  const [apellidos, setApellidos] = useState('')
  const [especialidad, setEspecialidad] = useState('')
  const [validated, setValidated] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const resetFormulario = () => {
    setNombre('')
    setApellidos('')
    setEspecialidad('')
    setValidated(false)
    setErrorMessage('')
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

    setErrorMessage('')
    setLoading(true)
    try {
      await onCrear({ nombre, apellidos, especialidad })
      resetFormulario()
      onHide()
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail || 'No se pudo crear el veterinario. Inténtalo de nuevo.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <Modal show={show} onHide={handleClose} centered>
      <Modal.Header closeButton>
        <Modal.Title>Nuevo veterinario</Modal.Title>
      </Modal.Header>

      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <Modal.Body>
          {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

          <Form.Group className="mb-3" controlId="nombre">
            <Form.Label>Nombre</Form.Label>
            <Form.Control
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
            />
            <Form.Control.Feedback type="invalid">
              El nombre es obligatorio.
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group className="mb-3" controlId="apellidos">
            <Form.Label>Apellidos</Form.Label>
            <Form.Control
              type="text"
              value={apellidos}
              onChange={(e) => setApellidos(e.target.value)}
              required
            />
            <Form.Control.Feedback type="invalid">
              Los apellidos son obligatorios.
            </Form.Control.Feedback>
          </Form.Group>

          <Form.Group controlId="especialidad">
            <Form.Label>Especialidad</Form.Label>
            <Form.Control
              type="text"
              placeholder="Opcional"
              value={especialidad}
              onChange={(e) => setEspecialidad(e.target.value)}
            />
          </Form.Group>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Cancelar
          </Button>
          <Button variant="primary" type="submit" disabled={loading}>
            {loading ? 'Creando...' : 'Crear veterinario'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  )
}

export default CrearVeterinarioModal
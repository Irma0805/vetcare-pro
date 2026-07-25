import { Link } from 'react-router'
import { Card, Row, Col, Badge, Button } from 'react-bootstrap'

function formatearFechaNacimiento(fechaISO) {
  return new Date(fechaISO).toLocaleDateString('es-ES', { dateStyle: 'medium' })
}

function DatosMascotaCard({ mascota }) {
  const {
    nombre,
    especie,
    raza,
    fecha_nacimiento,
    peso,
    activo,
    propietario,
  } = mascota

  return (
    <Card>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <span>Información de la Mascota</span>
        <Button variant="primary" size="sm" disabled>
          Editar
        </Button>
      </Card.Header>
      <Card.Body>
        <Row className="mb-3">
          <Col>
            <Badge bg={activo ? 'success' : 'secondary'}>
              {activo ? 'Activo' : 'Inactivo'}
            </Badge>
          </Col>
        </Row>
        <Row className="mb-3">
          <Col md={4}>
            <strong>Nombre:</strong> {nombre}
          </Col>
          <Col md={4}>
            <strong>Especie:</strong> {especie}
          </Col>
          <Col md={4}>
            <strong>Raza:</strong> {raza ?? 'No especificada'}
          </Col>
        </Row>
        <Row className="mb-3">
          <Col md={4}>
            <strong>Fecha de nacimiento:</strong>{' '}
            {fecha_nacimiento ? formatearFechaNacimiento(fecha_nacimiento) : 'No registrada'}
          </Col>
          <Col md={4}>
            <strong>Peso (kg):</strong> {peso ?? 'no registrado'}
          </Col>
          <Col md={4}>
            <strong>Propietario:</strong>{' '}
            <Link to={`/clientes/${propietario.id_propietario}`}>
              {propietario.nombre} {propietario.apellidos}
            </Link>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  )
}

export default DatosMascotaCard
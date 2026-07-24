import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';


function InformacionContactoCard({ propietario }) {
  const { nombre, apellidos, dni, telefono, email, direccion } = propietario;

  return (
    <Card className="mb-4">
      <Card.Body>
        <div className="d-flex justify-content-between align-items-center mb-3">
          <Card.Title>Información de Contacto</Card.Title>
          <Button variant="outline-secondary" size="sm" disabled>
            Editar Ficha
          </Button>
        </div>

        <Row className="mb-3">
          <Col md={4}>
            <div className="text-uppercase text-secondary small fw-bold">
              Nombre
            </div>
            <div>{nombre}</div>
          </Col>
          <Col md={4}>
            <div className="text-uppercase text-secondary small fw-bold">
              Apellidos
            </div>
            <div>{apellidos}</div>
          </Col>
          <Col md={4}>
            <div className="text-uppercase text-secondary small fw-bold">
              DNI
            </div>
            <div>{dni}</div>
          </Col>
        </Row>

        <Row>
          <Col md={4}>
            <div className="text-uppercase text-secondary small fw-bold">
              Teléfono
            </div>
            <div>{telefono || '—'}</div>
          </Col>
          <Col md={4}>
            <div className="text-uppercase text-secondary small fw-bold">
              Email
            </div>
            <div>{email || '—'}</div>
          </Col>
          <Col md={4}>
            <div className="text-uppercase text-secondary small fw-bold">
              Dirección
            </div>
            <div>{direccion || '—'}</div>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
}

export default InformacionContactoCard;
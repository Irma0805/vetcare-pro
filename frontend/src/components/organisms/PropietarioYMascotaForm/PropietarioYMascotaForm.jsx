import { useState } from 'react';
import { Link } from 'react-router';
import { Form, Button, Alert, ListGroup, Spinner } from 'react-bootstrap';


function PropietarioYMascotaForm({
  resultadoBusqueda,
  buscando,
  mascotasDelPropietario,
  modoMascota,
  onModoMascotaChange,
  onBuscarDni,
  onPropietarioNuevoChange,
  onMascotaSeleccionada,
  onMascotaNuevaChange,
}) {
  const [dniInput, setDniInput] = useState('');

  const handleBuscarClick = () => {
    if (dniInput.trim()) {
      onBuscarDni(dniInput.trim());
    }
  };

  const renderPropietarioNuevoYMascotaNueva = () => (
    <>
      <Alert variant="info">
        No se encontró ningún cliente con ese DNI. Se dará de alta como cliente nuevo.
      </Alert>
      <fieldset className="mb-3">
        <legend className="h6">Datos del cliente nuevo</legend>
        <Form.Group className="mb-2">
          <Form.Label>Nombre</Form.Label>
          <Form.Control
            required
            onChange={(e) => onPropietarioNuevoChange({ campo: 'nombre', valor: e.target.value })}
          />
          <Form.Control.Feedback type="invalid">El nombre es obligatorio.</Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-2">
          <Form.Label>Apellidos</Form.Label>
          <Form.Control
            required
            onChange={(e) => onPropietarioNuevoChange({ campo: 'apellidos', valor: e.target.value })}
          />
          <Form.Control.Feedback type="invalid">Los apellidos son obligatorios.</Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-2">
          <Form.Label>Teléfono</Form.Label>
          <Form.Control
            onChange={(e) => onPropietarioNuevoChange({ campo: 'telefono', valor: e.target.value })}
          />
        </Form.Group>
        <Form.Group className="mb-2">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            onChange={(e) => onPropietarioNuevoChange({ campo: 'email', valor: e.target.value })}
          />
        </Form.Group>
        <Form.Group className="mb-2">
          <Form.Label>Dirección</Form.Label>
          <Form.Control
            onChange={(e) => onPropietarioNuevoChange({ campo: 'direccion', valor: e.target.value })}
          />
        </Form.Group>
      </fieldset>
      <fieldset className="mb-3">
        <legend className="h6">Datos de la mascota nueva</legend>
        <Form.Group className="mb-2">
          <Form.Label>Nombre</Form.Label>
          <Form.Control
            required
            onChange={(e) => onMascotaNuevaChange({ campo: 'nombre', valor: e.target.value })}
          />
          <Form.Control.Feedback type="invalid">El nombre es obligatorio.</Form.Control.Feedback>
        </Form.Group>
        <Form.Group className="mb-2">
          <Form.Label>Especie</Form.Label>
          <Form.Control
            required
            onChange={(e) => onMascotaNuevaChange({ campo: 'especie', valor: e.target.value })}
          />
          <Form.Control.Feedback type="invalid">La especie es obligatoria.</Form.Control.Feedback>
        </Form.Group>
      </fieldset>
    </>
  );

  const renderPropietarioInactivo = () => (
    <Alert variant="warning">
      Este cliente está dado de baja. No se puede crear una cita nueva para él en este momento.
    </Alert>
  );

  const renderPropietarioActivo = () => (
    <>
      <Alert variant="success">
        Cliente encontrado: {resultadoBusqueda.nombre} {resultadoBusqueda.apellidos}
      </Alert>
      <Form.Group className="mb-3">
        <Form.Check
          inline
          type="radio"
          label="Mascota ya registrada"
          name="modoMascota"
          checked={modoMascota === 'existente'}
          onChange={() => onModoMascotaChange('existente')}
        />
        <Form.Check
          inline
          type="radio"
          label="Mascota nueva"
          name="modoMascota"
          checked={modoMascota === 'nueva'}
          onChange={() => onModoMascotaChange('nueva')}
        />
      </Form.Group>

      {modoMascota === 'existente' && (
        <ListGroup className="mb-3">
          {mascotasDelPropietario?.map((mascota) => (
            <ListGroup.Item
              key={mascota.id_mascota}
              action
              onClick={() => onMascotaSeleccionada(mascota.id_mascota)}
            >
              {mascota.nombre} ({mascota.especie})
            </ListGroup.Item>
          ))}
        </ListGroup>
      )}

      {modoMascota === 'nueva' && (
        <fieldset className="mb-3">
          <legend className="h6">Datos de la mascota nueva</legend>
          <Form.Group className="mb-2">
            <Form.Label>Nombre</Form.Label>
            <Form.Control
              required
              onChange={(e) => onMascotaNuevaChange({ campo: 'nombre', valor: e.target.value })}
            />
            <Form.Control.Feedback type="invalid">El nombre es obligatorio.</Form.Control.Feedback>
          </Form.Group>
          <Form.Group className="mb-2">
            <Form.Label>Especie</Form.Label>
            <Form.Control
              required
              onChange={(e) => onMascotaNuevaChange({ campo: 'especie', valor: e.target.value })}
            />
            <Form.Control.Feedback type="invalid">La especie es obligatoria.</Form.Control.Feedback>
          </Form.Group>
        </fieldset>
      )}
    </>
  );

  const renderResultado = () => {
    if (resultadoBusqueda === undefined) return null;
    if (resultadoBusqueda === null) return renderPropietarioNuevoYMascotaNueva();

    return (
      <>
        <div className="mb-2">
          <Link to={`/clientes/${resultadoBusqueda.id_propietario}`}>
            Ver ficha completa
          </Link>
        </div>
        {resultadoBusqueda.activo ? renderPropietarioActivo() : renderPropietarioInactivo()}
      </>
    );
  };

  return (
    <div className="mb-4">
      <Form.Group className="mb-3">
        <Form.Label>DNI del cliente</Form.Label>
        <div className="d-flex gap-2">
          <Form.Control
            value={dniInput}
            onChange={(e) => setDniInput(e.target.value)}
            placeholder="12345678Z"
          />
          <Button onClick={handleBuscarClick} disabled={buscando}>
            {buscando ? <Spinner size="sm" animation="border" /> : 'Buscar'}
          </Button>
        </div>
      </Form.Group>

      {renderResultado()}
    </div>
  );
}

export default PropietarioYMascotaForm;
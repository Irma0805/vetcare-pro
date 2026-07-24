import Table from 'react-bootstrap/Table';
import { Link } from 'react-router';

function MascotasAsociadasTable({ mascotas }) {
  return (
    <Table striped hover responsive>
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Especie</th>
        </tr>
      </thead>
      <tbody>
        {mascotas.map((mascota) => (
          <tr key={mascota.id_mascota}>
            <td>
              <Link to={`/mascotas/${mascota.id_mascota}`}>
                {mascota.nombre}
              </Link>
            </td>
            <td>{mascota.especie}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
}

export default MascotasAsociadasTable;
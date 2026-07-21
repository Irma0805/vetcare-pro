import { useState, useEffect } from 'react'
import { Table, Spinner, Alert, Button } from 'react-bootstrap'
import { getVeterinarios } from '../../api/veterinarios'

const TAMANO_PAGINA = 10

function VeterinariosPage() {
  const [veterinarios, setVeterinarios] = useState([])
  const [pagina, setPagina] = useState(1)
  const [loading, setLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    let ignore = false

    async function cargarVeterinarios() {
      setLoading(true)
      setErrorMessage('')
      try {
        const datos = await getVeterinarios(pagina)
        if (!ignore) {
          setVeterinarios(datos)
        }
      } catch (error) {
        if (!ignore) {
          setErrorMessage(
            error.response?.data?.detail || 'No se pudo cargar el listado de veterinarios.'
          )
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    cargarVeterinarios()

    return () => {
      ignore = true
    }
  }, [pagina])

  const hayPaginaSiguiente = veterinarios.length === TAMANO_PAGINA

  return (
    <>
      <h1>Veterinarios</h1>

      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

      {loading ? (
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      ) : veterinarios.length === 0 ? (
        <p>No hay veterinarios que mostrar.</p>
      ) : (
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Nombre</th>
              <th>Apellidos</th>
              <th>Especialidad</th>
            </tr>
          </thead>
          <tbody>
            {veterinarios.map((veterinario) => (
              <tr key={veterinario.id_veterinario}>
                <td>{veterinario.nombre}</td>
                <td>{veterinario.apellidos}</td>
                <td>{veterinario.especialidad || '—'}</td>
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

export default VeterinariosPage
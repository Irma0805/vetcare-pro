import { useState, useEffect } from 'react'
import { useParams } from 'react-router'
import { Spinner, Alert } from 'react-bootstrap'
import { obtenerFichaCliente } from '../../api/propietarios'
import InformacionContactoCard from '../../components/molecules/InformacionContactoCard/InformacionContactoCard'
import MascotasAsociadasTable from '../../components/molecules/MascotasAsociadasTable/MascotasAsociadasTable'

function FichaClientePage() {
  const { id } = useParams()
  const [ficha, setFicha] = useState(null)
  const [loading, setLoading] = useState(true)
  const [errorMessage, setErrorMessage] = useState('')

  useEffect(() => {
    let ignore = false

    async function cargarFicha() {
      setLoading(true)
      setErrorMessage('')
      try {
        const datos = await obtenerFichaCliente(id)
        if (!ignore) {
          setFicha(datos)
        }
      } catch (error) {
        if (!ignore) {
          setErrorMessage(
            error.response?.data?.detail || 'No se pudo cargar la ficha del cliente.'
          )
        }
      } finally {
        if (!ignore) {
          setLoading(false)
        }
      }
    }

    cargarFicha()

    return () => {
      ignore = true
    }
  }, [id])

  return (
    <>
      <h1 className="mb-3">Detalle del Cliente</h1>

      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

      {loading ? (
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      ) : (
        ficha && (
          <>
            <InformacionContactoCard propietario={ficha} />
            <h2 className="mb-3">Mascotas Asociadas</h2>
            <MascotasAsociadasTable mascotas={ficha.mascotas} />
          </>
        )
      )}
    </>
  )
}

export default FichaClientePage
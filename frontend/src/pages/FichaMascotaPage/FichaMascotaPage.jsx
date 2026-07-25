import { useState, useEffect } from 'react'
import { useParams } from 'react-router'
import { Spinner, Alert } from 'react-bootstrap'
import { obtenerFichaMascota } from '../../api/mascotas'
import DatosMascotaCard from '../../components/molecules/DatosMascotaCard/DatosMascotaCard'

function FichaMascotaPage() {
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
        const datos = await obtenerFichaMascota(id)
        if (!ignore) {
          setFicha(datos)
        }
      } catch (error) {
        if (!ignore) {
          setErrorMessage(
            error.response?.data?.detail || 'No se pudo cargar la ficha de la mascota.'
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
      <h1 className="mb-3">Detalle de la Mascota</h1>

      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

      {loading ? (
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Cargando...</span>
        </Spinner>
      ) : (
        ficha && <DatosMascotaCard mascota={ficha} />
      )}
    </>
  )
}

export default FichaMascotaPage
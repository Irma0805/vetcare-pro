import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router'
import { Form, Button, Alert, Spinner } from 'react-bootstrap'
import { getVeterinarios } from '../../api/veterinarios'
import { buscarPropietarioPorDni, obtenerFichaCliente } from '../../api/propietarios'
import { crearCita } from '../../api/citas'
import PropietarioYMascotaForm from '../../components/organisms/PropietarioYMascotaForm/PropietarioYMascotaForm'

const PAGINA_INICIAL = 1

function CrearCitaPage() {
  const navigate = useNavigate()

  // Veterinarios para el selector
  const [veterinarios, setVeterinarios] = useState([])
  const [veterinarioId, setVeterinarioId] = useState('')

  // Búsqueda de propietario
  const [resultadoBusqueda, setResultadoBusqueda] = useState(undefined) // undefined = aún no buscado
  const [buscando, setBuscando] = useState(false)
  const [mascotasDelPropietario, setMascotasDelPropietario] = useState(null)

  // Datos acumulados según el modo (nuevo/existente)
  const [propietarioNuevo, setPropietarioNuevo] = useState({})
  const [modoMascota, setModoMascota] = useState('existente')
  const [mascotaSeleccionadaId, setMascotaSeleccionadaId] = useState(null)
  const [mascotaNueva, setMascotaNueva] = useState({})

  // Resto de campos de la cita
  const [fechaHora, setFechaHora] = useState('')
  const [motivoConsulta, setMotivoConsulta] = useState('')

  // Envío
  const [validated, setValidated] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let ignore = false

    async function cargarVeterinarios() {
      try {
        const datos = await getVeterinarios(PAGINA_INICIAL)
        if (!ignore) setVeterinarios(datos)
      } catch {
        // Fallo silencioso a propósito: el selector queda vacío y el
        // checkValidity() nativo bloqueará el envío por campo requerido.
      }
    }

    cargarVeterinarios()
    return () => { ignore = true }
  }, [])

  const handleBuscarDni = async (dni) => {
    setBuscando(true)
    setErrorMessage('')
    setMascotasDelPropietario(null)
    setMascotaSeleccionadaId(null)
    setModoMascota('existente')
    try {
      const resultado = await buscarPropietarioPorDni(dni)
      setResultadoBusqueda(resultado)
      setPropietarioNuevo({ dni })

      if (resultado && resultado.activo) {
        const ficha = await obtenerFichaCliente(resultado.id_propietario)
        setMascotasDelPropietario(ficha.mascotas)
      }
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail || 'No se pudo buscar el cliente. Inténtalo de nuevo.'
      )
    } finally {
      setBuscando(false)
    }
  }

  const handlePropietarioNuevoChange = ({ campo, valor }) => {
    setPropietarioNuevo((prev) => ({ ...prev, [campo]: valor }))
  }

  const handleMascotaNuevaChange = ({ campo, valor }) => {
    setMascotaNueva((prev) => ({ ...prev, [campo]: valor }))
  }

  const construirBloquePropietario = () => {
    if (resultadoBusqueda && resultadoBusqueda.activo) {
      return { propietario_id: resultadoBusqueda.id_propietario, propietario_nuevo: null }
    }
    return { propietario_id: null, propietario_nuevo: propietarioNuevo }
  }

  const construirBloqueMascota = () => {
    const propietarioEsExistente = resultadoBusqueda && resultadoBusqueda.activo
    if (propietarioEsExistente && modoMascota === 'existente') {
      return { mascota_id: mascotaSeleccionadaId, mascota_nueva: null }
    }
    return { mascota_id: null, mascota_nueva: mascotaNueva }
  }

  const handleSubmit = async (event) => {
    const form = event.currentTarget
    event.preventDefault()

    if (form.checkValidity() === false) {
      event.stopPropagation()
      setValidated(true)
      return
    }

    if (resultadoBusqueda === undefined) {
      setErrorMessage('Busca un cliente por DNI antes de continuar.')
      return
    }
    if (resultadoBusqueda !== null && !resultadoBusqueda.activo) {
      setErrorMessage('No se puede crear una cita para un cliente dado de baja.')
      return
    }
    if (resultadoBusqueda && resultadoBusqueda.activo && modoMascota === 'existente' && !mascotaSeleccionadaId) {
      setErrorMessage('Selecciona una mascota de la lista, o elige "Mascota nueva".')
      return
    }

    const payload = {
      ...construirBloquePropietario(),
      ...construirBloqueMascota(),
      veterinario_id: Number(veterinarioId),
      fecha_hora: new Date(fechaHora).toISOString(),
      motivo_consulta: motivoConsulta,
    }

    setErrorMessage('')
    setLoading(true)
    try {
      await crearCita(payload)
      navigate('/citas')
    } catch (error) {
      setErrorMessage(
        error.response?.data?.detail || 'No se pudo crear la cita. Inténtalo de nuevo.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <h1 className="mb-3">Nueva cita</h1>

      {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}

      <Form noValidate validated={validated} onSubmit={handleSubmit}>
        <PropietarioYMascotaForm
          resultadoBusqueda={resultadoBusqueda}
          buscando={buscando}
          mascotasDelPropietario={mascotasDelPropietario}
          modoMascota={modoMascota}
          onModoMascotaChange={setModoMascota}
          onBuscarDni={handleBuscarDni}
          onPropietarioNuevoChange={handlePropietarioNuevoChange}
          onMascotaSeleccionada={setMascotaSeleccionadaId}
          onMascotaNuevaChange={handleMascotaNuevaChange}
        />

        <Form.Group className="mb-3" controlId="veterinario">
          <Form.Label>Veterinario</Form.Label>
          <Form.Select
            value={veterinarioId}
            onChange={(e) => setVeterinarioId(e.target.value)}
            required
          >
            <option value="">Selecciona un veterinario</option>
            {veterinarios.map((vet) => (
              <option key={vet.id_veterinario} value={vet.id_veterinario}>
                {vet.nombre} {vet.apellidos}
              </option>
            ))}
          </Form.Select>
          <Form.Control.Feedback type="invalid">
            Debes seleccionar un veterinario.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="fechaHora">
          <Form.Label>Fecha y hora</Form.Label>
          <Form.Control
            type="datetime-local"
            value={fechaHora}
            onChange={(e) => setFechaHora(e.target.value)}
            required
          />
          <Form.Control.Feedback type="invalid">
            La fecha y hora son obligatorias.
          </Form.Control.Feedback>
        </Form.Group>

        <Form.Group className="mb-3" controlId="motivoConsulta">
          <Form.Label>Motivo de la consulta</Form.Label>
          <Form.Control
            as="textarea"
            value={motivoConsulta}
            onChange={(e) => setMotivoConsulta(e.target.value)}
            required
          />
          <Form.Control.Feedback type="invalid">
            El motivo de consulta es obligatorio.
          </Form.Control.Feedback>
        </Form.Group>

        <Button variant="primary" type="submit" disabled={loading}>
          {loading ? <Spinner size="sm" animation="border" /> : 'Crear cita'}
        </Button>
      </Form>
    </>
  )
}

export default CrearCitaPage
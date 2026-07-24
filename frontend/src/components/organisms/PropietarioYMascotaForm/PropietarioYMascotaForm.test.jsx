import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import PropietarioYMascotaForm from './PropietarioYMascotaForm'

const propsBase = {
  resultadoBusqueda: undefined,
  buscando: false,
  mascotasDelPropietario: null,
  modoMascota: 'existente',
  onModoMascotaChange: vi.fn(),
  onBuscarDni: vi.fn(),
  onPropietarioNuevoChange: vi.fn(),
  onMascotaSeleccionada: vi.fn(),
  onMascotaNuevaChange: vi.fn(),
}

function renderConRouter(props) {
  return render(
    <MemoryRouter>
      <PropietarioYMascotaForm {...propsBase} {...props} />
    </MemoryRouter>
  )
}

describe('PropietarioYMascotaForm', () => {
  it('llama a onBuscarDni con el DNI escrito al pulsar Buscar', async () => {
    const user = userEvent.setup()
    const onBuscarDni = vi.fn()

    renderConRouter({ onBuscarDni })

    await user.type(screen.getByPlaceholderText('12345678Z'), '12345678Z')
    await user.click(screen.getByRole('button', { name: 'Buscar' }))

    expect(onBuscarDni).toHaveBeenCalledWith('12345678Z')
  })

  it('muestra el formulario de cliente y mascota nuevos cuando no se encuentra el DNI', () => {
    renderConRouter({ resultadoBusqueda: null })

    expect(screen.getByText(/No se encontró ningún cliente/)).toBeInTheDocument()
    expect(screen.getByText('Datos del cliente nuevo')).toBeInTheDocument()
    expect(screen.getByText('Datos de la mascota nueva')).toBeInTheDocument()
  })

  it('muestra un aviso de bloqueo cuando el propietario está inactivo', () => {
    renderConRouter({
      resultadoBusqueda: { id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: false },
    })

    expect(screen.getByText(/Este cliente está dado de baja/)).toBeInTheDocument()
    expect(screen.queryByText('Mascota ya registrada')).not.toBeInTheDocument()
  })

  it('muestra el enlace a la ficha completa cuando el propietario está inactivo', () => {
    renderConRouter({
      resultadoBusqueda: { id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: false },
    })

    expect(screen.getByRole('link', { name: 'Ver ficha completa' })).toHaveAttribute('href', '/clientes/1')
  })

  it('muestra la lista de mascotas y permite seleccionar una cuando el propietario está activo', async () => {
    const user = userEvent.setup()
    const onMascotaSeleccionada = vi.fn()

    renderConRouter({
      resultadoBusqueda: { id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: true },
      mascotasDelPropietario: [{ id_mascota: 5, nombre: 'Toby', especie: 'Perro' }],
      onMascotaSeleccionada,
    })

    await user.click(screen.getByText('Toby (Perro)'))

    expect(onMascotaSeleccionada).toHaveBeenCalledWith(5)
  })

  it('muestra los campos de mascota nueva cuando el propietario está activo y se elige "Mascota nueva"', () => {
    renderConRouter({
      resultadoBusqueda: { id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: true },
      modoMascota: 'nueva',
    })

    expect(screen.getByText('Datos de la mascota nueva')).toBeInTheDocument()
  })

  it('muestra el enlace a la ficha completa cuando el propietario está activo', () => {
    renderConRouter({
      resultadoBusqueda: { id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: true },
    })

    expect(screen.getByRole('link', { name: 'Ver ficha completa' })).toHaveAttribute('href', '/clientes/1')
  })
})
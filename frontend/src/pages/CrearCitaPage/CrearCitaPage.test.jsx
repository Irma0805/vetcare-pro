import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { getVeterinarios } from '../../api/veterinarios'
import { buscarPropietarioPorDni, obtenerFichaCliente } from '../../api/propietarios'
import { crearCita } from '../../api/citas'
import CrearCitaPage from './CrearCitaPage'

const mockedUsedNavigate = vi.fn()

vi.mock('react-router', async () => {
  const actual = await vi.importActual('react-router')
  return {
    ...actual,
    useNavigate: () => mockedUsedNavigate,
  }
})

vi.mock('../../api/veterinarios', () => ({
  getVeterinarios: vi.fn(),
}))

vi.mock('../../api/propietarios', () => ({
  buscarPropietarioPorDni: vi.fn(),
  obtenerFichaCliente: vi.fn(),
}))

vi.mock('../../api/citas', () => ({
  crearCita: vi.fn(),
}))

const veterinariosMock = [
  { id_veterinario: 1, nombre: 'Laura', apellidos: 'Fernández Ruiz' },
]

describe('CrearCitaPage', () => {
    beforeEach(() => {
    vi.clearAllMocks()
    getVeterinarios.mockResolvedValue(veterinariosMock)
  })

  it('busca un propietario y muestra el formulario de cliente nuevo si no existe', async () => {
    const user = userEvent.setup()
    buscarPropietarioPorDni.mockResolvedValue(null)

    render(<CrearCitaPage />)

    await user.type(screen.getByPlaceholderText('12345678Z'), '00000000A')
    await user.click(screen.getByRole('button', { name: 'Buscar' }))

    expect(await screen.findByText(/No se encontró ningún cliente/)).toBeInTheDocument()
    expect(buscarPropietarioPorDni).toHaveBeenCalledWith('00000000A')
  })

  it('busca un propietario activo, trae su ficha y permite seleccionar una mascota', async () => {
    const user = userEvent.setup()
    buscarPropietarioPorDni.mockResolvedValue({
      id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: true,
    })
    obtenerFichaCliente.mockResolvedValue({
      mascotas: [{ id_mascota: 5, nombre: 'Toby', especie: 'Perro' }],
    })

    render(<CrearCitaPage />)

    await user.type(screen.getByPlaceholderText('12345678Z'), '12345678Z')
    await user.click(screen.getByRole('button', { name: 'Buscar' }))

    expect(await screen.findByText('Toby (Perro)')).toBeInTheDocument()
    expect(obtenerFichaCliente).toHaveBeenCalledWith(1)
  })


  it('busca un propietario inactivo y muestra el aviso de bloqueo, sin pedir su ficha', async () => {
  const user = userEvent.setup()
  buscarPropietarioPorDni.mockResolvedValue({
    id_propietario: 2, dni: '87654321X', nombre: 'Luis', apellidos: 'Pérez Sanz', activo: false,
  })

  render(<CrearCitaPage />)

  await user.type(screen.getByPlaceholderText('12345678Z'), '87654321X')
  await user.click(screen.getByRole('button', { name: 'Buscar' }))

  expect(await screen.findByText(/Este cliente está dado de baja/)).toBeInTheDocument()
  expect(obtenerFichaCliente).not.toHaveBeenCalled()
})

  it('crea la cita con un propietario y mascota existentes, y redirige a /citas', async () => {
    const user = userEvent.setup()
    buscarPropietarioPorDni.mockResolvedValue({
      id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: true,
    })
    obtenerFichaCliente.mockResolvedValue({
      mascotas: [{ id_mascota: 5, nombre: 'Toby', especie: 'Perro' }],
    })
    crearCita.mockResolvedValue({ id_cita: 99 })

    render(<CrearCitaPage />)

    await user.type(screen.getByPlaceholderText('12345678Z'), '12345678Z')
    await user.click(screen.getByRole('button', { name: 'Buscar' }))
    await user.click(await screen.findByText('Toby (Perro)'))

    await user.selectOptions(screen.getByLabelText('Veterinario'), '1')
    await user.type(screen.getByLabelText('Fecha y hora'), '2026-08-01T10:00')
    await user.type(screen.getByLabelText('Motivo de la consulta'), 'Revisión anual')

    await user.click(screen.getByRole('button', { name: 'Crear cita' }))

    await waitFor(() => {
      expect(crearCita).toHaveBeenCalledWith(
        expect.objectContaining({
          propietario_id: 1,
          mascota_id: 5,
          veterinario_id: 1,
          motivo_consulta: 'Revisión anual',
        })
      )
    })
    expect(mockedUsedNavigate).toHaveBeenCalledWith('/citas')
  })

  it('muestra un mensaje de error si la creación de la cita falla', async () => {
    const user = userEvent.setup()
    buscarPropietarioPorDni.mockResolvedValue({
      id_propietario: 1, dni: '12345678Z', nombre: 'Ana', apellidos: 'García', activo: true,
    })
    obtenerFichaCliente.mockResolvedValue({
      mascotas: [{ id_mascota: 5, nombre: 'Toby', especie: 'Perro' }],
    })
    crearCita.mockRejectedValue({
      response: { data: { detail: 'El veterinario no está disponible' } },
    })

    render(<CrearCitaPage />)

    await user.type(screen.getByPlaceholderText('12345678Z'), '12345678Z')
    await user.click(screen.getByRole('button', { name: 'Buscar' }))
    await user.click(await screen.findByText('Toby (Perro)'))
    await user.selectOptions(screen.getByLabelText('Veterinario'), '1')
    await user.type(screen.getByLabelText('Fecha y hora'), '2026-08-01T10:00')
    await user.type(screen.getByLabelText('Motivo de la consulta'), 'Revisión anual')

    await user.click(screen.getByRole('button', { name: 'Crear cita' }))

    expect(await screen.findByText('El veterinario no está disponible')).toBeInTheDocument()
    expect(mockedUsedNavigate).not.toHaveBeenCalled()
  })
})
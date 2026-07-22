import { render, screen } from '@testing-library/react'
import { getVeterinarios } from '../../api/veterinarios'
import VeterinariosPage from './VeterinariosPage'

vi.mock('../../api/veterinarios', () => ({
  getVeterinarios: vi.fn(),
}))

describe('VeterinariosPage', () => {
  it('muestra un indicador de carga mientras se obtienen los datos', () => {
    getVeterinarios.mockReturnValue(new Promise(() => {}))

    render(<VeterinariosPage />)

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('muestra el listado cuando la petición tiene éxito', async () => {
    getVeterinarios.mockResolvedValue([
      { id_veterinario: 1, nombre: 'Laura', apellidos: 'Fernández Ruiz', especialidad: 'Medicina general' },
      { id_veterinario: 2, nombre: 'Javier', apellidos: 'Ortega Fernández', especialidad: '' },
    ])

    render(<VeterinariosPage />)

    expect(await screen.findByText('Laura')).toBeInTheDocument()
    expect(screen.getByText('Fernández Ruiz')).toBeInTheDocument()
    expect(screen.getByText('—')).toBeInTheDocument()

    expect(screen.getByRole('button', { name: 'Anterior' })).toBeDisabled()
    expect(screen.getByRole('button', { name: 'Siguiente' })).toBeDisabled()
  })

  it('muestra un mensaje de error si la petición falla', async () => {
    getVeterinarios.mockRejectedValue({
      response: { data: { detail: 'No autorizado' } },
    })

    render(<VeterinariosPage />)

    expect(await screen.findByText('No autorizado')).toBeInTheDocument()
  })
})
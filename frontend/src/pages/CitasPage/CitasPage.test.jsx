import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router'
import { getCitas } from '../../api/citas'
import CitasPage from './CitasPage'

vi.mock('../../api/citas', () => ({
  getCitas: vi.fn(),
}))

describe('CitasPage', () => {
  it('muestra un indicador de carga mientras se obtienen los datos', () => {
    getCitas.mockReturnValue(new Promise(() => {}))

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    expect(screen.getByRole('status')).toBeInTheDocument()
  })

  it('muestra el listado cuando la petición tiene éxito', async () => {
    getCitas.mockResolvedValue([
      {
        id_cita: 1,
        fecha_hora: '2026-07-25T10:00:00+02:00',
        estado: 'agendada',
        mascota_nombre: 'Toby',
        veterinario_nombre: 'Laura',
        veterinario_apellidos: 'Fernández Ruiz',
      },
    ])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    expect(await screen.findByText('Toby')).toBeInTheDocument()
    expect(screen.getByText('Laura Fernández Ruiz')).toBeInTheDocument()
    expect(screen.getByText('agendada')).toBeInTheDocument()
  })

  it('muestra un mensaje de error si la petición falla', async () => {
    getCitas.mockRejectedValue({
      response: { data: { detail: 'No autorizado' } },
    })

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    expect(await screen.findByText('No autorizado')).toBeInTheDocument()
  })
})
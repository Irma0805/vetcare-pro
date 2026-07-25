import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { getCitas, cancelarCita } from '../../api/citas'
import CitasPage from './CitasPage'

vi.mock('../../api/citas', () => ({
  getCitas: vi.fn(),
  cancelarCita: vi.fn(),
}))

const CITA_AGENDADA = {
  id_cita: 1,
  fecha_hora: '2026-07-25T10:00:00+02:00',
  estado: 'agendada',
  mascota_nombre: 'Toby',
  veterinario_nombre: 'Laura',
  veterinario_apellidos: 'Fernández Ruiz',
}

const CITA_CANCELADA = {
  id_cita: 2,
  fecha_hora: '2026-07-26T12:00:00+02:00',
  estado: 'cancelada',
  mascota_nombre: 'Milo',
  veterinario_nombre: 'Ana',
  veterinario_apellidos: 'Gómez Sanz',
}

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
    getCitas.mockResolvedValue([CITA_AGENDADA])

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

  it('no muestra el menú de acciones en una cita que no está agendada', async () => {
    getCitas.mockResolvedValue([CITA_CANCELADA])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Milo')
    expect(screen.queryByRole('button', { name: /acciones/i })).not.toBeInTheDocument()
  })

  it('muestra un mensaje de error en el modal si la cancelación falla', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValue([CITA_AGENDADA])
    cancelarCita.mockRejectedValue({
      response: { data: { detail: 'La cita ya está cancelada' } },
    })

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Toby')
    await user.click(screen.getByRole('button', { name: /acciones/i }))
    await user.click(await screen.findByText('Cancelar cita'))
    await user.click(screen.getByRole('button', { name: /sí, cancelar cita/i }))

    expect(await screen.findByText('La cita ya está cancelada')).toBeInTheDocument()
  })

  it('cancela la cita y refresca el listado cuando la confirmación tiene éxito', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValueOnce([CITA_AGENDADA])
    cancelarCita.mockResolvedValue({ ...CITA_AGENDADA, estado: 'cancelada' })
    getCitas.mockResolvedValueOnce([CITA_CANCELADA])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Toby')
    await user.click(screen.getByRole('button', { name: /acciones/i }))
    await user.click(await screen.findByText('Cancelar cita'))
    await user.click(screen.getByRole('button', { name: /sí, cancelar cita/i }))

    expect(cancelarCita).toHaveBeenCalledWith(1)
    expect(screen.queryByText('¿Seguro que quieres cancelar')).not.toBeInTheDocument()
    await screen.findByText('cancelada')
  })
})
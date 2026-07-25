import { render, screen, waitForElementToBeRemoved } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { getCitas, cancelarCita, registrarDiagnostico } from '../../api/citas'
import CitasPage from './CitasPage'

vi.mock('../../api/citas', () => ({
  getCitas: vi.fn(),
  cancelarCita: vi.fn(),
  registrarDiagnostico: vi.fn(),
}))

const AHORA = new Date('2026-07-25T12:00:00Z')

const CITA_AGENDADA_FUTURA = {
  id_cita: 1,
  fecha_hora: '2026-08-01T10:00:00Z',
  estado: 'agendada',
  mascota_nombre: 'Toby',
  veterinario_nombre: 'Laura',
  veterinario_apellidos: 'Fernández Ruiz',
}

const CITA_AGENDADA_PASADA = {
  id_cita: 2,
  fecha_hora: '2026-07-20T10:00:00Z',
  estado: 'agendada',
  mascota_nombre: 'Milo',
  veterinario_nombre: 'Ana',
  veterinario_apellidos: 'Gómez Sanz',
}

const CITA_CANCELADA = {
  id_cita: 3,
  fecha_hora: '2026-07-26T12:00:00Z',
  estado: 'cancelada',
  mascota_nombre: 'Nala',
  veterinario_nombre: 'Ana',
  veterinario_apellidos: 'Gómez Sanz',
}

beforeEach(() => {
  vi.setSystemTime(AHORA)
})

afterEach(() => {
  vi.useRealTimers()
})

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
    getCitas.mockResolvedValue([CITA_AGENDADA_FUTURA])

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

  it('no muestra el menú de acciones en una cita cancelada', async () => {
    getCitas.mockResolvedValue([CITA_CANCELADA])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Nala')
    expect(screen.queryByRole('button', { name: /acciones/i })).not.toBeInTheDocument()
  })

  it('ofrece solo Cancelar cita para una cita agendada futura', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValue([CITA_AGENDADA_FUTURA])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Toby')
    await user.click(screen.getByRole('button', { name: /acciones/i }))

    expect(screen.getByText('Cancelar cita')).toBeInTheDocument()
    expect(screen.queryByText('Registrar diagnóstico')).not.toBeInTheDocument()
  })

  it('ofrece solo Registrar diagnóstico para una cita agendada pasada', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValue([CITA_AGENDADA_PASADA])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Milo')
    await user.click(screen.getByRole('button', { name: /acciones/i }))

    expect(screen.getByText('Registrar diagnóstico')).toBeInTheDocument()
    expect(screen.queryByText('Cancelar cita')).not.toBeInTheDocument()
  })

  it('muestra un mensaje de error en el modal si la cancelación falla', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValue([CITA_AGENDADA_FUTURA])
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
    getCitas.mockResolvedValueOnce([CITA_AGENDADA_FUTURA])
    cancelarCita.mockResolvedValue({ ...CITA_AGENDADA_FUTURA, estado: 'cancelada' })
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

  it('el botón de guardar diagnóstico está deshabilitado con el textarea vacío', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValue([CITA_AGENDADA_PASADA])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Milo')
    await user.click(screen.getByRole('button', { name: /acciones/i }))
    await user.click(await screen.findByText('Registrar diagnóstico'))

    expect(screen.getByRole('button', { name: /guardar diagnóstico/i })).toBeDisabled()
  })

  it('muestra un mensaje de error en el modal si registrar el diagnóstico falla', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValue([CITA_AGENDADA_PASADA])
    registrarDiagnostico.mockRejectedValue({
      response: { data: { detail: 'La cita aún no se ha realizado' } },
    })

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Milo')
    await user.click(screen.getByRole('button', { name: /acciones/i }))
    await user.click(await screen.findByText('Registrar diagnóstico'))
    await user.type(screen.getByLabelText('Diagnóstico'), 'Otitis leve en oído derecho')
    await user.click(screen.getByRole('button', { name: /guardar diagnóstico/i }))

    expect(await screen.findByText('La cita aún no se ha realizado')).toBeInTheDocument()
  })
it('registra el diagnóstico y refresca el listado cuando el guardado tiene éxito', async () => {
    const user = userEvent.setup()
    getCitas.mockResolvedValueOnce([CITA_AGENDADA_PASADA])
    registrarDiagnostico.mockResolvedValue({ ...CITA_AGENDADA_PASADA, diagnostico: 'Otitis leve' })
    getCitas.mockResolvedValueOnce([{ ...CITA_AGENDADA_PASADA, estado: 'cancelada' }])

    render(
      <MemoryRouter>
        <CitasPage />
      </MemoryRouter>
    )

    await screen.findByText('Milo')
    await user.click(screen.getByRole('button', { name: /acciones/i }))
    await user.click(await screen.findByText('Registrar diagnóstico'))
    await user.type(screen.getByLabelText('Diagnóstico'), 'Otitis leve')
    await user.click(screen.getByRole('button', { name: /guardar diagnóstico/i }))

    expect(registrarDiagnostico).toHaveBeenCalledWith(2, 'Otitis leve')
    await waitForElementToBeRemoved(() => screen.queryByLabelText('Diagnóstico'))
  })
})
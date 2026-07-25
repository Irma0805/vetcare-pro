import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { getTratamientos } from '../../../api/tratamientos'
import AsociarTratamientoModal from './AsociarTratamientoModal'

vi.mock('../../../api/tratamientos', () => ({
  getTratamientos: vi.fn(),
}))

const CITA = {
  id_cita: 5,
  mascota_nombre: 'Toby',
}

const TRATAMIENTOS = [
  { id_tratamiento: 1, nombre: 'Antiparasitario', tipo_tratamiento: 'Preventivo', descripcion: 'Tratamiento antiparasitario', tarifa_por_kg: '2.00' },
  { id_tratamiento: 2, nombre: 'Cura de herida', tipo_tratamiento: 'Curativo', descripcion: 'Cura de herida superficial', tarifa_por_kg: '3.00' },
]

describe('AsociarTratamientoModal', () => {
  it('muestra un mensaje de error si no se puede cargar el catálogo', async () => {
    getTratamientos.mockRejectedValue(new Error('fallo de red'))

    render(<AsociarTratamientoModal show onHide={vi.fn()} cita={CITA} onAsociar={vi.fn()} />)

    expect(await screen.findByText('No se pudo cargar el catálogo de tratamientos.')).toBeInTheDocument()
  })

  it('muestra errores de validación si se envía vacío', async () => {
    const user = userEvent.setup()
    getTratamientos.mockResolvedValue(TRATAMIENTOS)
    const onAsociar = vi.fn()

    render(<AsociarTratamientoModal show onHide={vi.fn()} cita={CITA} onAsociar={onAsociar} />)

    await screen.findByText('Antiparasitario — 2.00 €/kg')
    await user.click(screen.getByRole('button', { name: 'Asociar tratamiento' }))

    expect(await screen.findByText('Debes seleccionar un tratamiento.')).toBeInTheDocument()
    expect(onAsociar).not.toHaveBeenCalled()
  })

  it('muestra un mensaje de error si la asociación falla', async () => {
    const user = userEvent.setup()
    getTratamientos.mockResolvedValue(TRATAMIENTOS)
    const onAsociar = vi.fn().mockRejectedValue({
      response: { data: { detail: 'El tratamiento indicado no existe' } },
    })
    const onHide = vi.fn()

    render(<AsociarTratamientoModal show onHide={onHide} cita={CITA} onAsociar={onAsociar} />)

    await screen.findByText('Antiparasitario — 2.00 €/kg')
    await user.selectOptions(screen.getByLabelText('Tratamiento'), '1')
    await user.type(screen.getByLabelText('Fecha de inicio'), '2026-07-20')
    await user.type(screen.getByLabelText('Fecha de fin'), '2026-07-25')
    await user.type(screen.getByLabelText('Dosis'), '5 ml cada 8 horas')
    await user.click(screen.getByRole('button', { name: 'Asociar tratamiento' }))

    expect(await screen.findByText('El tratamiento indicado no existe')).toBeInTheDocument()
    expect(onHide).not.toHaveBeenCalled()
  })

  it('muestra el valor calculado y cierra el modal al pulsar Cerrar cuando la petición tiene éxito', async () => {
    const user = userEvent.setup()
    getTratamientos.mockResolvedValue(TRATAMIENTOS)
    const onAsociar = vi.fn().mockResolvedValue({
      id_citas_tratamientos: 10,
      id_cita: 5,
      id_tratamiento: 1,
      fecha_inicio: '2026-07-20',
      fecha_fin: '2026-07-25',
      dosis: '5 ml cada 8 horas',
      seguimiento: null,
      valor_tratamiento: '24.00',
    })
    const onHide = vi.fn()

    render(<AsociarTratamientoModal show onHide={onHide} cita={CITA} onAsociar={onAsociar} />)

    await screen.findByText('Antiparasitario — 2.00 €/kg')
    await user.selectOptions(screen.getByLabelText('Tratamiento'), '1')
    await user.type(screen.getByLabelText('Fecha de inicio'), '2026-07-20')
    await user.type(screen.getByLabelText('Fecha de fin'), '2026-07-25')
    await user.type(screen.getByLabelText('Dosis'), '5 ml cada 8 horas')
    await user.click(screen.getByRole('button', { name: 'Asociar tratamiento' }))

    expect(onAsociar).toHaveBeenCalledWith({
      id_tratamiento: 1,
      fecha_inicio: '2026-07-20',
      fecha_fin: '2026-07-25',
      dosis: '5 ml cada 8 horas',
      seguimiento: null,
    })

    expect(await screen.findByText('Tratamiento asociado correctamente.')).toBeInTheDocument()
    expect(screen.getByText('24.00 €', { exact: false })).toBeInTheDocument()
    expect(onHide).not.toHaveBeenCalled()

    await user.click(screen.getByRole('button', { name: 'Cerrar' }))

    await waitFor(() => {
      expect(onHide).toHaveBeenCalled()
    })
  })

  it('muestra el aviso de valor no calculado cuando la mascota no tiene peso registrado', async () => {
    const user = userEvent.setup()
    getTratamientos.mockResolvedValue(TRATAMIENTOS)
    const onAsociar = vi.fn().mockResolvedValue({
      id_citas_tratamientos: 11,
      id_cita: 5,
      id_tratamiento: 1,
      fecha_inicio: '2026-07-20',
      fecha_fin: '2026-07-25',
      dosis: '5 ml cada 8 horas',
      seguimiento: null,
      valor_tratamiento: null,
    })

    render(<AsociarTratamientoModal show onHide={vi.fn()} cita={CITA} onAsociar={onAsociar} />)

    await screen.findByText('Antiparasitario — 2.00 €/kg')
    await user.selectOptions(screen.getByLabelText('Tratamiento'), '1')
    await user.type(screen.getByLabelText('Fecha de inicio'), '2026-07-20')
    await user.type(screen.getByLabelText('Fecha de fin'), '2026-07-25')
    await user.type(screen.getByLabelText('Dosis'), '5 ml cada 8 horas')
    await user.click(screen.getByRole('button', { name: 'Asociar tratamiento' }))

    expect(await screen.findByText('No calculado (la mascota no tiene peso registrado)')).toBeInTheDocument()
  })
})
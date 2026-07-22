import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CrearVeterinarioModal from './CrearVeterinarioModal'

describe('CrearVeterinarioModal', () => {
  it('muestra errores de validación si se envía vacío', async () => {
    const user = userEvent.setup()
    const onCrear = vi.fn()

    render(<CrearVeterinarioModal show onHide={vi.fn()} onCrear={onCrear} />)

    await user.click(screen.getByRole('button', { name: 'Crear veterinario' }))

    expect(await screen.findByText('El nombre es obligatorio.')).toBeInTheDocument()
    expect(screen.getByText('Los apellidos son obligatorios.')).toBeInTheDocument()
    expect(onCrear).not.toHaveBeenCalled()
  })

  it('muestra un mensaje de error si la creación falla', async () => {
    const user = userEvent.setup()
    const onCrear = vi.fn().mockRejectedValue({
      response: { data: { detail: 'Ya existe un veterinario con esos datos' } },
    })
    const onHide = vi.fn()

    render(<CrearVeterinarioModal show onHide={onHide} onCrear={onCrear} />)

    await user.type(screen.getByLabelText('Nombre'), 'Laura')
    await user.type(screen.getByLabelText('Apellidos'), 'Fernández Ruiz')
    await user.click(screen.getByRole('button', { name: 'Crear veterinario' }))

    expect(await screen.findByText('Ya existe un veterinario con esos datos')).toBeInTheDocument()
    expect(onHide).not.toHaveBeenCalled()
  })

  it('crea el veterinario y cierra el modal cuando la petición tiene éxito', async () => {
    const user = userEvent.setup()
    const onCrear = vi.fn().mockResolvedValue()
    const onHide = vi.fn()

    render(<CrearVeterinarioModal show onHide={onHide} onCrear={onCrear} />)

    await user.type(screen.getByLabelText('Nombre'), 'Laura')
    await user.type(screen.getByLabelText('Apellidos'), 'Fernández Ruiz')
    await user.click(screen.getByRole('button', { name: 'Crear veterinario' }))

    expect(onCrear).toHaveBeenCalledWith({
      nombre: 'Laura',
      apellidos: 'Fernández Ruiz',
      especialidad: '',
    })

    await waitFor(() => {
      expect(onHide).toHaveBeenCalled()
    })
  })
})
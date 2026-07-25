import { describe, it, expect } from 'vitest'
import { renderConRouter, screen } from '../../../test/test-utils'
import DatosMascotaCard from './DatosMascotaCard'

const mascotaCompleta = {
  nombre: 'Toby',
  especie: 'Perro',
  raza: 'Labrador',
  fecha_nacimiento: '2020-05-12',
  peso: 12.5,
  activo: true,
  propietario: {
    id_propietario: 7,
    nombre: 'María',
    apellidos: 'López García',
  },
}

describe('DatosMascotaCard', () => {
  it('muestra los datos completos de la mascota, el badge Activo y el enlace al propietario', () => {
    renderConRouter(<DatosMascotaCard mascota={mascotaCompleta} />)

    expect(screen.getByText('Toby')).toBeInTheDocument()
    expect(screen.getByText('Perro')).toBeInTheDocument()
    expect(screen.getByText('Labrador')).toBeInTheDocument()
    expect(screen.getByText('Activo')).toBeInTheDocument()

    const enlacePropietario = screen.getByRole('link', { name: 'María López García' })
    expect(enlacePropietario).toHaveAttribute('href', '/clientes/7')
  })

  it('muestra los textos de reserva cuando raza, fecha de nacimiento y peso no están registrados', () => {
    const mascotaSinDatos = {
      ...mascotaCompleta,
      raza: null,
      fecha_nacimiento: null,
      peso: null,
    }

    renderConRouter(<DatosMascotaCard mascota={mascotaSinDatos} />)

    expect(screen.getByText('No especificada')).toBeInTheDocument()
    expect(screen.getByText('No registrada')).toBeInTheDocument()
    expect(screen.getByText('no registrado')).toBeInTheDocument()
  })

  it('muestra el badge Inactivo cuando la mascota está dada de baja', () => {
    const mascotaInactiva = { ...mascotaCompleta, activo: false }

    renderConRouter(<DatosMascotaCard mascota={mascotaInactiva} />)

    expect(screen.getByText('Inactivo')).toBeInTheDocument()
  })

  it('el botón Editar está deshabilitado', () => {
    renderConRouter(<DatosMascotaCard mascota={mascotaCompleta} />)

    expect(screen.getByRole('button', { name: 'Editar' })).toBeDisabled()
  })
})
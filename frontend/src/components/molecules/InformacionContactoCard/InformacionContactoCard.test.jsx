import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import InformacionContactoCard from './InformacionContactoCard';

const propietarioCompleto = {
  nombre: 'Carlos Javier',
  apellidos: 'Méndez Rodríguez',
  dni: '12345678Z',
  telefono: '+34 612 345 678',
  email: 'c.mendez@example.com',
  direccion: 'Calle de la Victoria, 42',
};

describe('InformacionContactoCard', () => {
  it('muestra los datos de contacto del propietario', () => {
    render(<InformacionContactoCard propietario={propietarioCompleto} />);

    expect(screen.getByText('Carlos Javier')).toBeInTheDocument();
    expect(screen.getByText('Méndez Rodríguez')).toBeInTheDocument();
    expect(screen.getByText('12345678Z')).toBeInTheDocument();
    expect(screen.getByText('+34 612 345 678')).toBeInTheDocument();
    expect(screen.getByText('c.mendez@example.com')).toBeInTheDocument();
    expect(screen.getByText('Calle de la Victoria, 42')).toBeInTheDocument();
  });

  it('muestra un guion en los campos opcionales vacíos', () => {
    const propietarioSinOpcionales = {
      nombre: 'Ana',
      apellidos: 'García',
      dni: '87654321X',
      telefono: null,
      email: null,
      direccion: null,
    };

    render(<InformacionContactoCard propietario={propietarioSinOpcionales} />);

    expect(screen.getAllByText('—')).toHaveLength(3);
  });

  it('muestra el botón "Editar Ficha" deshabilitado', () => {
    render(<InformacionContactoCard propietario={propietarioCompleto} />);

    expect(screen.getByRole('button', { name: 'Editar Ficha' })).toBeDisabled();
  });
});